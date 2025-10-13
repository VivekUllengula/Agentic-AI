import os
import json
from google import genai
from dotenv import load_dotenv
import gradio as gr
from bs4 import BeautifulSoup
import requests

# -----------------------------
# Simple website scraper
# -----------------------------
class Website:
    def __init__(self, url):
        self.url = url
        self.title = "" 
        self.body = ""
        self.text = ""
        self.links = []

    def get_text(self):
        if not self.url.startswith("http"):
            return
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            self.body = response.content
            soup = BeautifulSoup(self.body, "html.parser")
            self.title = soup.title.string if soup.title else "No Title"
            if soup.body:
                for irrelevant in soup.body(["script", "style", "img", "input", "button"]):
                    irrelevant.decompose()
                self.text = soup.body.get_text(separator="\n", strip=True)
            else:
                self.text = ""
            links = [link.get("href") for link in soup.find_all("a")]
            self.links = [link for link in links if link]
        except Exception as e:
            self.title = "No Title"
            self.body = ""
            self.text = ""
            self.links = []

    def get_content(self):
        return f"Title: {self.title}\n\nWebpage Contents:\n{self.text}"


# -----------------------------
# Load API key
# -----------------------------
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
model = os.getenv("GOOGLE_MODEL_NAME")
gemini = genai.Client(api_key=api_key)

# -----------------------------
# Prompts
# -----------------------------
link_system_prompt = (
    "You are provided with a list of links found on a webpage. "
    "You are able to decide which of the links would be most relevant to include in a brochure about the company, "
    "such as links to an About page, or a Company page, or Careers/Jobs pages.\n"
    "You should respond in JSON as in this example:\n"
    "{\n"
    '    "links": [\n'
    '        {"type": "about page", "url": "https://full.url/goes/here/about"},\n'
    '        {"type": "careers page", "url": "https://another.full.url/careers"}\n'
    "    ]\n"
    "}\n"
)

system_prompt = (
    "You are an assistant that analyzes the contents of several relevant pages from a company website "
    "and creates a short brochure about the company for prospective customers, investors and recruits. "
    "Include details of company culture, customers and careers/jobs if you have the information."
)

# -----------------------------
# Helper functions
# -----------------------------
def get_links_user_prompt(website):
    user_prompt = f"Here are the list of links on the website of {website.url} - "
    user_prompt += "please decide which of these are relevant web links for a brochure about the company, respond with the full https URL in JSON format. "
    user_prompt += "Do not include Terms of Service, Privacy, email links.\n"
    user_prompt += "Links (some might be relative links):\n"
    user_prompt += "\n".join(website.links)
    return user_prompt


def get_links(url):
    website = Website(url)
    website.get_text()
    response = gemini.models.generate_content(
        model=model,
        contents=get_links_user_prompt(website), 
        config={
            "max_output_tokens": 500,
            "system_instruction": link_system_prompt,
        },
    )
    try:
        return json.loads(response.text)
    except Exception:
        return {"links": []}


def get_all_details(url):
    website = Website(url)
    website.get_text()
    result = "Landing page:\n"
    result += website.get_content()

    links = get_links(url)
    for link in links.get("links", []):
        subsite = Website(link["url"])
        subsite.get_text()
        result += f"\n\n{link['type']}\n"
        result += subsite.get_content()

    return result


def get_brochure_user_prompt(url):
    user_prompt = "You are looking at a company’s website.\n"
    user_prompt += "Here are the contents of its landing page and other relevant pages; use this information to build a short brochure of the company.\n"
    user_prompt += get_all_details(url)
    user_prompt = user_prompt[:5000]  # truncate if too long
    return user_prompt


# -----------------------------
# Generate brochure function
# -----------------------------
def generate_brochure(url):
    prompt = get_brochure_user_prompt(url)
    response = gemini.models.generate_content(
        model=model,
        contents=prompt,  
        config={
            "max_output_tokens": 1000,
            "system_instruction": system_prompt,
        },
    )
    return response.text


# -----------------------------
# Gradio interface
# -----------------------------
view = gr.Interface(
    fn=generate_brochure,
    inputs=[gr.Textbox(label="Landing page URL including http:// or https://")],
    outputs=[gr.Markdown(label="Brochure:")],
    flagging_mode="never",
)

view.launch(share=True)

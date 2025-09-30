from google import genai
import os
from dotenv import load_dotenv
import gradio as gr
from bs4 import BeautifulSoup
import requests

class Website:
    def __init__(self,url):
        self.url = url
        self.body = ""
        self.title = ""
        self.url = []

    def get_text(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.body = soup.get_text(separator="\n", strip=True)
        self.title = soup.title.string if soup.title else "No Title Found"
        self.urls = [a['href'] for a in soup.find_all('a', href=True)]

    def get_content(self):
        return f"Title: {self.title}\n\nBody: {self.body}"
    
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
model_name = os.getenv("GOOGLE_MODEL_NAME", "gemini-2.5-flash")

gemini = genai.Client(api_key=api_key, model_name=model_name)

def generate_brochure_stream(url):

    #First get the main site content

    main_site = Website(url)
    main_site.get_text()

    #Next using LLM to filter relevant urls

    prompt_urls = f"""
    I have a website with the following main text:

    {main_site.get_content()}

    And the following links found on the page:
    {main_site.urls}

    Please return **only the URLs that are relevant** to the main content of the website, in a Python list format.
    """

    response = gemini.generate_text(prompt=prompt_urls, max_output_tokens=500)

    try:

        relevant_urls = eval(response.text)
        if not isinstance(relevant_urls, list):
            relevant_urls = []
    except:
        relevant_urls = []

    #Third step - Collect content from relevant urls
    all_content = main_site.get_content()

    for u in relevant_urls:
        try:
            sub_site = Website(u)
            sub_site.get_text()
            all_content += "\n\n" + sub_site.get_content()
        except Exception as e:
            print(f"Error fetching {u}: {e}")

    prompt_brochure = f"Create a detailed brochure for the following content:\n\n{all_content}"

    def stream_response():
        for chunk in gemini.stream_text(prompt=prompt_brochure, max_output_tokens=1000):
            yield chunk.text
    return stream_response

iface = gr.Interface(
    fn=generate_brochure_stream,
    inputs="text",
    outputs=gr.Textbox(
        label="AI Response",
        lines=6,         # starting height
        max_lines=30,    # grows until 30 lines, then scrolls
        interactive=False   # output only (user can’t edit)
    )
)

iface.launch( share=True)
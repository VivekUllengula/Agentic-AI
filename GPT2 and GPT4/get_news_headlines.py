#Steps
#Idenity Import
#Load GPT2Tokenizer and GPT2Model
# Get the news article (article)
# Get the possible Headlines (Candidate)
# Get Tokens for news article (article)
# Convert to tensor and send to model
# Get the full embedding for articles
# Get the mean embedding for  articles from full embedding

from transformers import GPT2Tokenizer, GPT2Model
import torch
import torch.nn.functional as F

DATA_PATH = "data.txt"

#reading data from text file
def reading_file_data(DATA_PATH):
    with open(DATA_PATH, 'r') as f:
        content = f.read()
    local_vars = {}
    exec(content, {}, local_vars)
    return local_vars['article'], local_vars['headlines']

# Load the data
article, headlines = reading_file_data(DATA_PATH)

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2Model.from_pretrained("gpt2")


def get_mean_embeddings(input_text):
    # Get the Tokens for the Text
    model_input = tokenizer(input_text,  return_tensors="pt")

    #Load model with min features for embedding only

    with torch.no_grad():
        model_output = model(**model_input)
        mean_embeddings =  model_output.last_hidden_state.mean(dim=1)
    return mean_embeddings

article_embeddings = get_mean_embeddings(article)

results = []
for headline in headlines:
    headline_embeddings = get_mean_embeddings(headline)
    score = F.cosine_similarity(article_embeddings, headline_embeddings).item()
    results.append((headline, score))

results.sort(key= lambda x: x[1], reverse=True)

print("Top 4 Similar headlines are: \n")
 
for i in range(4):
    headline, score = results[i]
    print  (f"{i + 1} - {headline} - Score {score:.4f}")
print("\n")
print("All Headings as per Score\n")

for headline, score in results:
    print(f"{score:.4f} -> {headline} ")

import pandas as pd
from langchain_mistralai.embeddings import MistralAIEmbeddings
import json
import os
from dotenv import load_dotenv

import openai
from openai import OpenAI

env_loaded = load_dotenv()
print("Environment loaded:", env_loaded)



client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)


# Set the current working directory to the script's directory
script_dir = os.path.dirname(__file__)
os.chdir(script_dir)



#api_key = os.getenv('MISTRAL_API')




def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding




#print(api_key)

#embeddings = MistralAIEmbeddings(model="mistral-embed", mistral_api_key= api_key)

json_path = os.path.join("data", "articles_data.json")

#print(json_path)

# Read the JSON file
with open(json_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Prepare a list to collect the data for the DataFrame
data_list = []

# Iterate through the JSON data and compute embeddings
for parent, article_list in data.items():
    # Compute the title embedding
    
    for article in article_list:
        
        title_doc = article['metadata']['Title']
                
        content = str(parent) + '\n' + article['page_content']
        url = article['metadata']['URL']
        last_modified=article['metadata']['last_modified']
        attach_link=article['metadata']['attach_link']
        
        
        # Compute the content embedding
        content_vector = get_embedding(content)
        title_vector = get_embedding(title_doc)
        
        # Append the data to the list
        data_list.append({
            'url': url,
            'title': title_doc,
            'content': content,
            'last_modified':last_modified,
            'attach_link':attach_link,
            'title_vector': title_vector,
            'content_vector': content_vector
        })

# Convert the list to a DataFrame
df = pd.DataFrame(data_list)

df.index.name = 'id'

# Export the DataFrame to a CSV file
csv_path = os.path.join("data", "articles_with_open_ai_embeddings.csv")
df.to_csv(csv_path, index=True)

print(f"Data has been successfully saved to {csv_path}")



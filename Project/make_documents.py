import pandas as pd
from langchain_mistralai.embeddings import MistralAIEmbeddings
import json
import os
from dotenv import load_dotenv

api_key = os.getenv('MISTRAL_API')

embeddings = MistralAIEmbeddings(model="mistral-embed", mistral_api_key= api_key)

json_path = os.path.join("data", "articles_data (1).json")

# Read the JSON file
with open(json_path, 'r') as file:
    data = json.load(file)

# Prepare a list to collect the data for the DataFrame
data_list = []

# Iterate through the JSON data and compute embeddings
for title, article_list in data.items():
    # Compute the title embedding
    title_vector = embeddings.embed_query(title)
    
    for article in article_list:
        content = str(title) + '\n' + article['page_content']
        url = article['metadata']['URL']
        parent = article['metadata']['Parent']
        
        # Compute the content embedding
        content_vector = embeddings.embed_query(content)
        
        # Append the data to the list
        data_list.append({
            'url': url,
            'title': title,
            'content': content,
            'title_vector': title_vector,
            'content_vector': content_vector
        })

# Convert the list to a DataFrame
df = pd.DataFrame(data_list)

# Export the DataFrame to a CSV file
csv_path = os.path.join("data", "articles_with_embeddings_mistral.csv")
df.to_csv(csv_path, index=True)

print(f"Data has been successfully saved to {csv_path}")

import openai
from dotenv import load_dotenv
from openai import OpenAI
import os


env_loaded = load_dotenv()
print("Environment loaded:", env_loaded)



client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding


text = "This is a test"

embedding = get_embedding(text)
print(embedding)
print(len(embedding))
print(type(embedding))

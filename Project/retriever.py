from Project.vector_pipeline import connect_db
from prompts import custom_answer_prompt_template_reform, summary_prompt, ques_check_prompt
import psycopg2
import os
from dotenv import load_dotenv
from langchain_mistralai.embeddings import MistralAIEmbeddings
from langchain_mistralai import ChatMistralAI
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
import requests
import random
import re
env_loaded = load_dotenv()
import openai
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)




def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

webhook_url = os.getenv('SLACK_WEB_HOOK')
#api_key = os.getenv('MISTRAL_API')
groq_api = os.getenv('GROQ_API')

#embeddings = MistralAIEmbeddings(model="mistral-embed", mistral_api_key= api_key)

ques_check = PromptTemplate(template=ques_check_prompt, input_variables=['query'])
answer_prompt = PromptTemplate(template=custom_answer_prompt_template_reform, input_variables=['query'])

summarize_prompt = PromptTemplate(template=summary_prompt, input_variables=['chat_history'])

chat = ChatGroq(temperature=0, groq_api_key = groq_api, model_name="Mixtral-8x7b-32768")

# Define the regular expressions for English and French questions
english_pattern = r'English:\s*(.*?)(?=French:|$)'
french_pattern = r'French:\s*(.*)'

def ques_check(query):
    formatted_prompt =  ques_check_prompt.format(query=query)
    answer = chat.invoke(formatted_prompt).content
    no_pattern = r'no\s*(.*)'

    match = re.search(no_pattern, answer.lower(), re.DOTALL)
    
    if match:
        return False
    else:
        return True

def chat_history_to_string(chat_history):
    chat_string = ""
    for entry in chat_history:
        role = entry['role'].capitalize()
        content = entry['content']
        chat_string += f"{role}: {content}\n"
    return chat_string.strip()  # To remove the trailing newline

def summarizer(chat_history):
    
    chat_log = chat_history_to_string(chat_history)
    formatted_prompt = summarize_prompt.format(chat_history=chat_log)
    
    summary = chat.invoke(formatted_prompt).content
    
    ticket_number = random.randint(1,100)
    
    return f"Ticket Number: {ticket_number} \n {summary}"

def send_to_slack(chat_history):
    
    summary = summarizer(chat_history)
    
    payload = {
        "text": summary
    }
    response = requests.post(webhook_url, json=payload)
    if response.status_code != 200:
        raise ValueError(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")
    return response
    

def reform(query, llm):
    formatted_prompt = answer_prompt.format(query=query)
    text = llm.invoke(formatted_prompt).content
    
    english_match = re.search(english_pattern, text, re.DOTALL)
    english_question = english_match.group(1).strip() if english_match else None
    
    # Extract French question
    french_match = re.search(french_pattern, text, re.DOTALL)
    french_question = french_match.group(1).strip() if french_match else None
    
    return english_question, french_question


    
def rerag(query, collection_name, cursor=connect_db()[1], top_k=5):
    
    if ques_check(query):
    
        english_question, french_question = reform(query, chat)
        
        english_results = get_common_results(english_question, collection_name, cursor, top_k)
        
        french_results = get_common_results(french_question, collection_name, cursor, top_k)
        
        # Use a set to track seen content IDs
        seen_ids = set()
        combined_results = []

        # Add unique English results to the combined list
        for row in english_results:
            if row[0] not in seen_ids:
                combined_results.append(row)
                seen_ids.add(row[0])

        # Add unique French results to the combined list
        for row in french_results:
            if row[0] not in seen_ids:
                combined_results.append(row)
                seen_ids.add(row[0])
        
        
        return format_results(combined_results)
    
    else:
        
        return query

    
    
    
def query_neon(query, collection_name, cursor, vector_name="title_vector", top_k=5):
    try:
        # Create an embedding vector from the user query
        embedded_query = get_embedding(query)
        # Convert the embedded_query to PostgreSQL compatible format
        embedded_query_pg = "[" + ",".join(map(str, embedded_query)) + "]"

        # Create the SQL query
        query_sql = f"""
        SELECT id, url, title, content,last_modified,attach_link
        FROM {collection_name}
        ORDER BY {vector_name} <=> '{embedded_query_pg}'
        LIMIT {top_k};
        """
        # Execute the query
        cursor.execute(query_sql)
        results = cursor.fetchall()

        return results

    except (psycopg2.Error) as e:
        # Roll back the transaction if an error occurs
        cursor.execute("ROLLBACK;")
        print(f"Error executing SQL query: {e}")
        return []
    
def get_common_results(query, collection_name, cursor, top_k=5):
    # Query for content vector
    results_content = query_neon(query, collection_name, cursor, vector_name="content_vector", top_k=top_k)
    
    # Query for title vector
    results_title = query_neon(query, collection_name, cursor, vector_name="title_vector", top_k=top_k)
    
    # Find common tuples based on id
    content_ids = {row[0] for row in results_content}
    common_results = [row for row in results_title if row[0] in content_ids]
    
    return common_results if common_results else results_content


def format_results(results):
    formatted_string = ""
    for i, result in enumerate(results, start=1):
        doc_id, url, title, content, last_modified,attach_link = result
        formatted_string += f"*Document {i}:*\nTitle: {title}\nContent: {content}\nURL: {url}\nLast Modified: {last_modified}\nAttach Link: {attach_link}\n "
    return formatted_string
    
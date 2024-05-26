from vector_pipeline import connect_db, table_exists,create_table_if_not_exists,load_csv_to_db
from retriever import format_results, get_common_results
from langchain.prompts import PromptTemplate
from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
import os

env_loaded = load_dotenv()
print("Environment loaded:", env_loaded)

script_dir = os.path.dirname(__file__)
os.chdir(script_dir)

api_key = os.getenv('MISTRAL_API_KEY')

query = "How do i enrol?"

csv_file_path = os.path.join("data", "articles_with_embeddings_mistral_new.csv")

connection, cursor = connect_db()





results = get_common_results(query, 'edu', cursor=cursor)

context = format_results(results)

custom_answer_prompt_template = """ 
<s>[INST] Using the context below:
context: {context}
Answer the question: {query}

Follow the guidelines:


[/INST]

"""

answer_prompt = PromptTemplate(template=custom_answer_prompt_template, input_variables=['context', 'query'])

formatted_prompt = answer_prompt.format(query=query, context=context)

system_prompt_template = """
You are a helpful, friendly chat assitant to help students with their admin related queries
"""

llm = ChatMistralAI(api_key=api_key, streaming= True, system = system_prompt_template)


astream = llm.astream(formatted_prompt)

print(llm.invoke(formatted_prompt))


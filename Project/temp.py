from vector_pipeline import connect_db
from retriever import format_results, get_common_results
from langchain.prompts import PromptTemplate
from langchain_mistralai import ChatMistralAI



query = "How do i enrol?"

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

llm = ChatMistralAI(api_key='jEoYKB36Y0ClSdn2n1cuLziCuyqntQzf', streaming= True, system = system_prompt_template)


astream = llm.astream(formatted_prompt)


print(llm.invoke(formatted_prompt))


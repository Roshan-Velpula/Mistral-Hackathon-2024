from vector_pipeline import connect_db
import psycopg2
import os
from dotenv import load_dotenv
from langchain_mistralai.embeddings import MistralAIEmbeddings

api_key = os.getenv('MISTRAL_API')

embeddings = MistralAIEmbeddings(model="mistral-embed", mistral_api_key= api_key)


def query_neon(query, collection_name, cursor, vector_name="title_vector", top_k=5):
    try:
        # Create an embedding vector from the user query
        embedded_query = embeddings.embed_query(query)
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
    
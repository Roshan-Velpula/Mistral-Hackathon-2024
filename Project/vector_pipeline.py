import os
import psycopg2
import io
from dotenv import load_dotenv

# Set the current working directory to the script's directory
script_dir = os.path.dirname(__file__)
os.chdir(script_dir)

env_loaded = load_dotenv()
print("Environment loaded:", env_loaded)

NEON_DB = os.getenv('DATABASE_URL')

csv_file_path = os.path.join('data','articles_with_open_ai_embeddings.csv' )

# Function to connect to the database
def connect_db():
    connection = psycopg2.connect(NEON_DB)
    return connection, connection.cursor()

# Function to check if a table exists
def table_exists(cursor, table_name):
    check_table_sql = f'''
    SELECT EXISTS (
        SELECT 1
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        AND table_name = '{table_name}'
    );
    '''
    cursor.execute(check_table_sql)
    return cursor.fetchone()[0]

# Function to create the table if it doesn't exist
def create_table_if_not_exists(cursor, connection):
    if not table_exists(cursor, 'edu'):
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS public.edu (
            id INTEGER NOT NULL,
            title TEXT,
            content TEXT,
            url TEXT,
            last_modified TEXT,
            attach_link TEXT,
            title_vector vector(1536),
            content_vector vector(1536)
        );

        ALTER TABLE public.edu ADD PRIMARY KEY (id);
        '''
        cursor.execute(create_table_sql)
        connection.commit()
        
def process_file(csv_file_path):
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            yield line

# Function to load CSV data into the table
def load_csv_to_db(cursor, connection, csv_file_path):
    modified_lines = io.StringIO(''.join(list(process_file(csv_file_path))))
    copy_command = '''
    COPY public.edu (id, url, title, content,last_modified,attach_link, title_vector, content_vector)
    FROM STDIN WITH (FORMAT CSV, HEADER true, DELIMITER ',');
    '''
    
    cursor.copy_expert(copy_command, modified_lines)
    connection.commit()
    


#connection, cursor = connect_db()

#create_table_if_not_exists(cursor, connection)

#load_csv_to_db(cursor, connection, csv_file_path)
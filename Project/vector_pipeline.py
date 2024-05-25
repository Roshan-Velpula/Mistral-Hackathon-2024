import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the database connection string
NEON_DB = os.getenv('NEON_DATABASE')
if not NEON_DB:
    NEON_DB = os.getenv("DATABASE_URL")
    if not NEON_DB:
        raise ValueError("Please provide a valid connection string either in the code or in the .env file as DATABASE_URL.")

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
            title_vector vector(1024),
            content_vector vector(1024),
            vector_id INTEGER
        );

        ALTER TABLE public.edu ADD PRIMARY KEY (id);
        '''
        cursor.execute(create_table_sql)
        connection.commit()

# Function to load CSV data into the table
def load_csv_to_db(cursor, connection, csv_file_path):
    copy_command = '''
    COPY public.edu (id, url, title, content, title_vector, content_vector, vector_id)
    FROM STDIN WITH (FORMAT CSV, HEADER true, DELIMITER ',');
    '''
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        cursor.copy_expert(copy_command, file)
    connection.commit()

from imports import os, load_dotenv

load_dotenv()
print("Environment variables loaded.")

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DB = os.getenv('MYSQL_DB')

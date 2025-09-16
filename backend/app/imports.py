# External imports
import os
import mysql.connector
from flask import Flask, Blueprint, jsonify, request
from flask_cors import CORS
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from dotenv import load_dotenv

# Internal imports
# These should be imported as needed in each file, e.g.:
# from config import GOOGLE_CLIENT_ID, MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB
# from db import get_db_connection, initialize_database
# from auth import auth_bp

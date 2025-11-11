# External imports
import os
import mysql.connector
from flask import Flask, Blueprint, jsonify, request
from flask_cors import CORS
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from dotenv import load_dotenv


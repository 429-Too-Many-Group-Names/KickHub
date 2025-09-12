import os
import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from dotenv import load_dotenv

load_dotenv()
print("Environment variables loaded.")
app = Flask(__name__)
CORS(app) # Enables CORS for all routes

# Load environment variables
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DB = os.getenv('MYSQL_DB')

# --- MySQL Database Setup ---
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            ssl_disabled=True # Disable SSL to work with localhost. Use SSL in production.
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def initialize_database():
    """Initializes the database by creating the `users` table if it doesn't exist."""
    conn = get_db_connection()
    if conn is None:
        print("Failed to connect to the database. Cannot initialize.")
        return

    cursor = conn.cursor()
    try:
        # Create the users table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                google_id VARCHAR(255) UNIQUE NOT NULL,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL
            )
        """)
        conn.commit()
        print("Database initialized successfully.")
    except mysql.connector.Error as err:
        print(f"Error initializing database: {err}")
    finally:
        cursor.close()
        conn.close()

# --- Google Auth Endpoint ---
@app.route('/api/auth/google', methods=['POST'])
def google_auth():
    """
    Receives and verifies the Google ID token from the frontend.
    Creates or updates a user in the MySQL database.
    """
    token = request.json.get('token')
    if not token:
        return jsonify({"error": "Missing token"}), 400

    try:
        # Specify the GOOGLE_CLIENT_ID that your app uses.
        # This will verify the token's signature, expiry, and audience.
        idinfo = id_token.verify_oauth2_token(
            token, google_requests.Request(), GOOGLE_CLIENT_ID)
        
        # Get user info from the token payload
        google_id = idinfo['sub']
        name = idinfo.get('name', 'User')
        email = idinfo['email']

        # Check if user already exists in the database
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE google_id = %s", (google_id,))
        user = cursor.fetchone()

        if user:
            # User exists, update their details if necessary (e.g., name, email)
            cursor.execute("""
                UPDATE users SET name = %s, email = %s WHERE google_id = %s
            """, (name, email, google_id))
            conn.commit()
            print(f"User {name} updated.")
            user_info = {'name': name, 'email': email, 'google_id': google_id}
        else:
            # New user, create a new record
            cursor.execute("""
                INSERT INTO users (google_id, name, email) VALUES (%s, %s, %s)
            """, (google_id, name, email))
            conn.commit()
            print(f"New user {name} created.")
            user_info = {'name': name, 'email': email, 'google_id': google_id}

        cursor.close()
        conn.close()
        
        return jsonify({"message": "User authenticated successfully", "user": user_info}), 200

    except ValueError:
        # Invalid token, e.g., signature is invalid, token is expired, etc.
        return jsonify({"error": "Invalid Google ID token"}), 401
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An internal error occurred"}), 500

if __name__ == '__main__':
    initialize_database()
    print("Starting Flask server...")
    app.run(debug=True, port=5000)
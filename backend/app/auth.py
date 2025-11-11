from imports import Blueprint, jsonify, request, id_token, google_requests
from functools import wraps
from config import GOOGLE_CLIENT_ID
from db import get_db_connection

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Missing token'}), 401
        try:
            idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), GOOGLE_CLIENT_ID)
            # Optionally, attach user info to request context
        except Exception:
            return jsonify({'error': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated_function

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/auth/google', methods=['POST'])
def google_auth():
    token = request.json.get('token')
    print(token)
    if not token:
        return jsonify({"error": "Missing token"}), 400

    try:
        idinfo = id_token.verify_oauth2_token(
            token, google_requests.Request(), GOOGLE_CLIENT_ID)
        
        google_id = idinfo['sub']
        name = idinfo.get('name', 'User')
        email = idinfo['email']

        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE google_id = %s", (google_id,))
        user = cursor.fetchone()

        if user:
            cursor.execute("""
                UPDATE users SET name = %s, email = %s WHERE google_id = %s
            """, (name, email, google_id))
            conn.commit()
            print(f"User {name} updated.")
            user_info = {'name': name, 'email': email, 'google_id': google_id}
        else:
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
        return jsonify({"error": "Invalid Google ID token"}), 401
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An internal error occurred"}), 500

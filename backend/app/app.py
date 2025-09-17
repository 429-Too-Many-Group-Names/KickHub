from imports import Flask, CORS
from db import initialize_database
from auth import auth_bp
from shopping_cart import cart_bp

app = Flask(__name__)
CORS(app)
app.register_blueprint(auth_bp)
app.register_blueprint(cart_bp)

if __name__ == '__main__':
    initialize_database()
    print("Starting Flask server...")
    app.run(debug=True, port=5000)
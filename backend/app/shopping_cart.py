from imports import Blueprint, jsonify, request, id_token, google_requests
from auth import login_required
from db import get_db_connection

cart_bp = Blueprint('cart', __name__, url_prefix='/api/cart')

@cart_bp.route('/', methods=['GET'])
# @login_required
def get_user():
    conn = get_db_connection()
    data = {"item": "apple", "quantity": 3}
    return jsonify(data)
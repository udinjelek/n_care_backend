from flask import request, jsonify
from app.config import Config
def extract_bearer_token():
    bearer_token = request.headers.get('Authorization')
    if not bearer_token:
        return None
    return bearer_token.replace('Bearer ', '')

def validate_bearer_token():
    bearer_token = extract_bearer_token()
    if not bearer_token:
        return jsonify({'error': 'Bearer token is missing'}), 401
    
    # Check if the extracted token matches the expected token
    if bearer_token != Config.BEARER_TOKEN:
        return jsonify({'error': 'Invalid Bearer token'}), 401

    # Token is valid
    return None, 200
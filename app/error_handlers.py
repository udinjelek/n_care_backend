from flask import jsonify

def handle_database_error(error):
    """Error handler for database-related errors."""
    return jsonify({'error': str(error)}), 500

from flask import Blueprint, jsonify, request
from app.utils.database import get_db_connection
from app.error_handlers import handle_database_error
from app.helper._json_transformer import transform_to_json_send
import sqlite3
users_bp = Blueprint('users', __name__)

@users_bp.route('/api/users')
def get_users():
    try:
        # Connect to SQLite database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Execute the query to fetch all users
        cursor.execute('SELECT * FROM users')
        dataQuery = cursor.fetchall()

        # Close the connection to the database
        conn.close()

        # Convert the query result to a JSON format
        data_json = [dict(row) for row in dataQuery]

        json_send = transform_to_json_send(data_json)
        return jsonify(json_send)
    except sqlite3.Error as e:
        # If a SQLite database error occurs, return an error response
        return handle_database_error('SQLite database error occurred: {}'.format(str(e)))
    except Exception as e:
        # If a generic exception occurs, raise it with a different message
        raise Exception('An unexpected error occurred: {}'.format(str(e)))

@users_bp.route('/api/users_id', methods=['GET'])
def get_user_by_id():
    try:
        # Get the user ID from the request parameters
        user_id = request.args.get('userid')

        # Connect to SQLite database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Execute the query to fetch the user by ID
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        dataQuery = cursor.fetchone()

        # Close the connection to the database
        conn.close()

        if dataQuery:
            # Convert the user data to a dictionary
            data_json = dict(dataQuery)
            # Return the user data as JSON response
            json_send = transform_to_json_send(data_json)
            return jsonify(json_send)
        else:
            # If user not found, return a 404 error response
            return jsonify({'error': 'User not found'}), 404
    except sqlite3.Error as e:
        # If a SQLite database error occurs, return an error response
        return handle_database_error('SQLite database error occurred: {}'.format(str(e)))
    except Exception as e:
        # If a generic exception occurs, raise it with a different message
        raise Exception('An unexpected error occurred: {}'.format(str(e)))

@users_bp.route('/api/login', methods=['GET'])
def get_user_login():
    try:
        username = request.args.get('username')
        password = request.args.get('password')

        # Connect to SQLite database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Execute the query to fetch the user by ID
        cursor.execute('SELECT password , id FROM users WHERE username = ? limit 1', (username,))
        dataQuery = cursor.fetchone()

        print(dataQuery)
        # Close the connection to the database
        conn.close()

        if dataQuery:
            
            if ( password == dataQuery[0] ):
                return jsonify({'status': True, 'login':'success', 'userid' : dataQuery[1] })
            else:
                return jsonify({'status': True, 'login':'failed' , 'userid' : -1})
        else:
            # If user not found, return a 404 error response
            return jsonify({'error': 'User not found'}), 404
    except sqlite3.Error as e:
        # If a SQLite database error occurs, return an error response
        return handle_database_error('SQLite database error occurred: {}'.format(str(e)))
    except Exception as e:
        # If a generic exception occurs, raise it with a different message
        raise Exception('An unexpected error occurred: {}'.format(str(e)))
    

@users_bp.route('/api/load-dev-mode-user', methods=['GET'])
def get_load_dev_mode_user():
    try:
        # Connect to SQLite database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Execute the query to fetch the user by ID
        cursor.execute('select name, password, username ,  status  from users where is_admin = 0')
        dataQuery_nonadmin = cursor.fetchall()

        cursor.execute('select name, password, username ,  status  from users where is_admin = 1')
        dataQuery_admin = cursor.fetchall()

        # Close the connection to the database
        conn.close()

        # Convert the query result to a list of dictionaries
        data_json_nonadmin = [dict(row) for row in dataQuery_nonadmin]
        data_json_admin = [dict(row) for row in dataQuery_admin]
        
        # Combine the JSON responses into a single dictionary
        combined_json = {'non_admin_users': data_json_nonadmin, 'admin_users': data_json_admin}
        json_send_combined = transform_to_json_send(combined_json)
        return jsonify(json_send_combined)

    except sqlite3.Error as e:
        # If a SQLite database error occurs, return an error response
        return handle_database_error('SQLite database error occurred: {}'.format(str(e)))
    except Exception as e:
        # If a generic exception occurs, raise it with a different message
        raise Exception('An unexpected error occurred: {}'.format(str(e)))
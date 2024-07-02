from flask import Blueprint, jsonify, request
from app.utils.database import mysql_get_db_connection
from app.error_handlers import handle_database_error
from app.helper._json_transformer import transform_to_json_send
import mysql.connector
from datetime import date
satnusapersada_bp = Blueprint('satnusapersada', __name__)

@satnusapersada_bp.route('/api/po', methods=['GET'])
def get_po():
    try:
        # Connect to SQLite database
        conn = mysql_get_db_connection()
        cursor = conn.cursor()

        # Execute the query to fetch all users
        cursor.execute('SELECT * FROM table_po')
        dataQuery = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        # # Close the connection to the database
        conn.close()
        def custom_converter(value):
            if isinstance(value, date):
                return value.strftime('%Y-%m-%d')
            return value

        data_json = [
            {column: custom_converter(value) for column, value in zip(column_names, row)}
            for row in dataQuery
        ]
        # # Convert the query result to a JSON format
        # data_json = [dict(zip(column_names, row)) for row in dataQuery]
        print(dataQuery)
        json_send = transform_to_json_send(data_json)
        return jsonify(json_send)
        
    except mysql.connector.Error as e:
        # If a SQLite database error occurs, return an error response
        return handle_database_error('SQLite database error occurred: {}'.format(str(e)))
    except Exception as e:
        # If a generic exception occurs, raise it with a different message
        raise Exception('An unexpected error occurred: {}'.format(str(e)))

@satnusapersada_bp.route('/api/po', methods=['POST'])
def post_po():
    try:
        # Connect to SQLite database
        conn = mysql_get_db_connection()
        cursor = conn.cursor()

        # Execute the query to fetch all users
        cursor.execute('SELECT * FROM table_po')
        dataQuery = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        # # Close the connection to the database
        conn.close()
        def custom_converter(value):
            if isinstance(value, date):
                return value.strftime('%Y-%m-%d')
            return value

        data_json = [
            {column: custom_converter(value) for column, value in zip(column_names, row)}
            for row in dataQuery
        ]
        # # Convert the query result to a JSON format
        # data_json = [dict(zip(column_names, row)) for row in dataQuery]
        print(dataQuery)
        json_send = transform_to_json_send(data_json)
        return jsonify(json_send)
        
    except mysql.connector.Error as e:
        # If a SQLite database error occurs, return an error response
        return handle_database_error('SQLite database error occurred: {}'.format(str(e)))
    except Exception as e:
        # If a generic exception occurs, raise it with a different message
        raise Exception('An unexpected error occurred: {}'.format(str(e)))
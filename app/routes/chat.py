from flask import Blueprint, jsonify, request
from app.utils.socket_events import socketio 
from app.utils.database import get_db_connection
from app.error_handlers import handle_database_error
from app.helper._json_transformer import transform_to_json_send
import sqlite3
from app.utils.auth_utils import validate_bearer_token
from datetime import datetime
from flask_socketio import emit


# Create a Blueprint object for chat routes
chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/api/sidebar_chat', methods=['GET'])
def get_sidebar_chat():
    try:
        # Get the user ID from the request parameters
        self_id = request.args.get('self_id')
        # Connect to database
       
        conn = get_db_connection()
        cursor = conn.cursor()

        # ambil data user
        cursor.execute('''
                    SELECT name, username, status, is_admin , photo_url from users where id = :self_id
        ''', {'self_id': self_id})
        dataSelf = cursor.fetchone()

        # set id menjadi id_user yg dipakai
        id_used = self_id
        # check apakah data user adalah admin
        if dataSelf[3] == 1:
            # jika iya, maka, set id_user menjadi id admin
            id_used = 0
        
        # Execute the query to fetch all chat messages
        cursor.execute('''
                WITH LatestMessages AS (
                    SELECT
                        "timestamp",
                        CASE
                            WHEN sender_id_alias = :id_used THEN receive_id
                            WHEN receive_id = :id_used THEN sender_id_alias
                        END AS object_chat,
                        sender_id_alias,
                        receive_id,
                        message,
                        ROW_NUMBER() OVER (
                            PARTITION BY CASE
                                        WHEN sender_id_alias = :id_used THEN receive_id
                                        WHEN receive_id = :id_used THEN sender_id_alias
                                    END
                            ORDER BY "timestamp" DESC
                        ) AS row_num
                    FROM chat_message cm
                    WHERE sender_id_alias = :id_used OR receive_id = :id_used
                    ORDER BY "timestamp" DESC
                )
                SELECT
                    lm.object_chat as userid,
                    users.name,
                    SUBSTRING(lm.message, 1, 20) || '...' as latestMessage,
                    lm."timestamp",
                    false as isRead,
                    users.photo_url as photoUrl
                FROM LatestMessages lm
                left join users 
                on object_chat = users.id
                WHERE lm.row_num = 1;
        ''', {'id_used': id_used})

        dataQuery = cursor.fetchall()

        
        
        # Close the connection to the database
        conn.close()

        # Convert the query result to a list of dictionaries
        data_json_sidebar = [dict(row) for row in dataQuery]
        data_json_self = dict(dataSelf)
        combined_json = {'sidebar': data_json_sidebar, 'self': data_json_self}
        
        

        # Return the JSON response
        json_send = transform_to_json_send(combined_json)
        return jsonify(json_send)
    except sqlite3.Error as e:
        # If a SQLite database error occurs, return an error response
        return handle_database_error('SQLite database error occurred: {}'.format(str(e)))
    except Exception as e:
        # If a generic exception occurs, raise it with a different message
        raise Exception('An unexpected error occurred: {}'.format(str(e)))

@chat_bp.route('/api/chat_history', methods=['GET'])
def get_chat_history():
    try:
        # Get the user ID from the request parameters
        self_id = request.args.get('self_id')
        target_id = request.args.get('target_id')

        error_response, status_code = validate_bearer_token()
        if error_response:
            return error_response, status_code
        # Connect to SQLite database
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT is_admin FROM users WHERE id = ? limit 1', (self_id,))
        selfIsAdmin = cursor.fetchone()
        selfIsAdmin = selfIsAdmin[0]
        
        cursor.execute('SELECT is_admin FROM users WHERE id = ? limit 1', (target_id,))
        targetIsAdmin = cursor.fetchone()
        targetIsAdmin = targetIsAdmin[0]



        #  jika user adalah bukan admin, maka query di masking, dimana nama target admin di sembunyikan dan di rename dengan nama "customer care"
        if selfIsAdmin == 0 :
            # Execute the query to fetch all chat messages
            cursor.execute('''
                select     case 
                                WHEN admin_sender.is_admin = -1 THEN 'Customer Care'
                                ELSE cm.sender_firstname
                           END AS sender_name_used ,
                           admin_sender.is_admin sender_admin, 
                           admin_receive.is_admin receive_admin , 
                           cm.*  
                from chat_message cm
                left join      users admin_receive
                on admin_receive.id = cm.receive_id 
                left join      users admin_sender
                on admin_sender.id = cm.sender_id_alias 
                where ( cm.sender_id_alias = :self_id) 
                or    ( cm.receive_id = :self_id)
                order by cm.id;
            ''', {'self_id': self_id})
        
        #  jika user adalah admin, maka query di masking, dimana nama target admin di sembunyikan dan di rename dengan nama "customer care"
        else:
            # Execute the query to fetch all chat messages
            cursor.execute('''
                select     case 
                                WHEN admin_sender.is_admin = -1 THEN 'CS (' || cm.sender_firstname || ')' 
                                ELSE cm.sender_firstname
                           END AS sender_name_used ,
                           admin_sender.is_admin sender_admin, 
                           admin_receive.is_admin receive_admin , 
                           cm.*  
                from chat_message cm
                left join      users admin_receive
                on admin_receive.id = cm.receive_id 
                left join      users admin_sender
                on admin_sender.id = cm.sender_id_alias 
                where ( cm.sender_id_alias = :target_id ) 
                or    ( cm.receive_id = :target_id )
                order by cm.id;
            ''', {'target_id': target_id})
        dataQuery = cursor.fetchall()

        # Close the connection to the database
        conn.close()

        # Convert the query result to a list of dictionaries
        data_json = [dict(row) for row in dataQuery]
        
        # Return the JSON response
        json_send = transform_to_json_send(data_json)

        return jsonify(json_send)
        # return jsonify(dataQueryuser)
    except sqlite3.Error as e:
        # If a SQLite database error occurs, return an error response
        return handle_database_error('SQLite database error occurred: {}'.format(str(e)))
    except Exception as e:
        # If a generic exception occurs, raise it with a different message
        raise Exception('An unexpected error occurred: {}'.format(str(e)))

@chat_bp.route('/api/send_message', methods=['POST'])
def set_send_message():
    try:
        data = request.get_json()
        # Get the user ID from the request parameters
        self_id = data.get('self_id')
        target_id = data.get('target_id')
        message = data.get('message')
        # Connect to SQLite database
        conn = get_db_connection()
        cursor = conn.cursor()
        
          # ambil data user
        cursor.execute('''
                    SELECT name, username, status, is_admin , photo_url from users where id = :self_id
        ''', {'self_id': self_id})
        dataSelf = cursor.fetchone()

        # set id menjadi id_user yg dipakai
        id_used = self_id
        # check apakah data user adalah admin
        if dataSelf[3] == 1:
            # jika iya, maka, set id_user menjadi id admin
            id_used = 0
        
        # mapping variable for query purpose
        sender_id = self_id
        sender_id_alias = id_used
        receive_id = target_id
        timestamp = convertCurentTimeToNumber()
        message = message
        caption = 'no caption'
        sender_firstname = dataSelf[0]
        sender_username = dataSelf[1]

        data_to_insert = (sender_id, sender_id_alias, receive_id, timestamp, message, caption, sender_firstname, sender_username)
        sql_insert = '''INSERT INTO chat_message (sender_id, sender_id_alias, receive_id, timestamp, message, caption, sender_firstname, sender_username) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''

        
        # Execute the SQL INSERT statement
        cursor.execute(sql_insert, data_to_insert)
        # Commit changes to the database
        conn.commit()
        # Close the connection to the database
        conn.close()
        
        
        # Convert the query result to a list of dictionaries
        data_json = 'success'
        
        socketio.emit('new_message', {'sender_id': sender_id,
                                      'sender_id_alias': sender_id_alias,
                                      'receive_id': receive_id,
                                      'message': message,
                                      'sender_firstname': sender_firstname
                                      })


        # Return the JSON response
        json_send = transform_to_json_send(data_json)
        return jsonify(json_send)
    except sqlite3.Error as e:
        # If a SQLite database error occurs, return an error response
        return handle_database_error('SQLite database error occurred: {}'.format(str(e)))
    except Exception as e:
        # If a generic exception occurs, raise it with a different message
        raise Exception('An unexpected error occurred: {}'.format(str(e)))
    

def convertCurentTimeToNumber():
    current_datetime = datetime.now()
    datetime_in_decimal = float(current_datetime.timestamp())  
    return datetime_in_decimal

def convertTextDatetimeToNumber(text_date_time):
    # Convert the decimal timestamp to a datetime object
    datetime_obj = datetime.fromtimestamp(text_date_time)
    # Format the datetime object as "YYYY-MM-DD HH:MM:SS"
    formatted_datetime = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_datetime
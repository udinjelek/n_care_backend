from flask_socketio import emit
from app import socketio

def register_socket_events(socketio):
    @socketio.on('connect')
    def handle_connect():
        print('Client connected')

    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')

    @socketio.on('message')
    def handle_message(data):
        emit('new_message', data, broadcast=True)
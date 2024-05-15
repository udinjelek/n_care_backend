from flask import Flask, jsonify, send_file, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from app.config import Config 
import os

app = Flask(__name__)
app.config.from_object(Config)  # Load configurations from config.py

CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*",transports=['websocket'])


# Register the blueprints
from app.routes.users import users_bp
from app.routes.chat import chat_bp
app.register_blueprint(users_bp)
app.register_blueprint(chat_bp)

# Import and register SocketIO events
from app.utils.socket_events import register_socket_events
register_socket_events(socketio)

# Route to serve uploaded files
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    # Mendapatkan path lengkap file berdasarkan nama file
    file_path = os.path.join(app.root_path, f'upload\\', filename)
    
    if os.path.exists(file_path):
        # Mengirim file ke browser sebagai attachment
        return send_file(file_path, as_attachment=True)
    else:
        # Jika file tidak ditemukan, kirim pesan error
        # return file_path # pake buat trace
        error_message = 'File not found.'
        return render_template('error.html', error_message=error_message), 404
    
@app.route('/')
def hello_world():
    error_message = 'Path Not Valid.'
    return render_template('error.html', error_message=error_message), 404
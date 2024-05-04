from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from app.config import Config 

app = Flask(__name__)
app.config.from_object(Config)  # Load configurations from config.py
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*") # Initialize SocketIO

# Register the blueprints
from app.routes.users import users_bp
from app.routes.chat import chat_bp
app.register_blueprint(users_bp)
app.register_blueprint(chat_bp)

# Import and register SocketIO events
from app.utils.socket_events import register_socket_events
register_socket_events(socketio)
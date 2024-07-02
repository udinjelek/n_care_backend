# app/config.py
class Config:
    # API_ENDPOINT = 'http://127.0.0.1/'
    API_ENDPOINT = 'http://127.0.0.1:5001/'
    # API_ENDPOINT = 'https://care-chat-api.polaris.my.id/'
    BEARER_TOKEN = 'your_bearer_token_here..'
    UPLOAD_FOLDER = 'app/upload'
    GLOBAL_FILE = 'download'
    

DATABASE_CONFIG = {
    'host': '203.175.8.149',
    'user': 'polc6219_user',
    'password': 'notuser999',
    'database': 'polc6219_trial',
    'port': '3306'
}


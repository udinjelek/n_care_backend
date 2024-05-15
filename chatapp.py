# from app import app

# if __name__ == "__main__":
#     app.run(debug=True, port=5001)

from app import app

if __name__ == "__main__":
    app.run(host='care-chat-api.polaris.my.id', port=5001)
    # app.run(host='0.0.0.0', port=5001)
    # app.run(host='0.0.0.0')
    # app.run(host='192.168.31.117', port=5001)
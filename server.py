from flask import Flask, request, jsonify
import os
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')
socketio = SocketIO(app, cors_allowed_origins="*")
@app.route('/')
def index():
    return "Chat Server is running!"

@socketio.on('message')
def handle_message(data):
    print(f"Message received: {data}")
    send(data, broadcast=True)

@socketio.on('connect')
def handle_connect():
    print("Client connected")

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000)

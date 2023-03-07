from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json as JSON
    
app = Flask(__name__)

socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('gamepad3.html')

@socketio.on('connect')
def test_connect():
    print('Client connected')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on('info')
def my_event(message):
    print(message)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
from aiohttp import request
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json as JSON
from colorama import Fore
    
app = Flask(__name__)

socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('gamepad3.html')

@socketio.on('connect')
def test_connect():
    print(Fore.GREEN + 'Client connected')
@socketio.on('disconnect')
def test_disconnect():
    print(Fore.RED + 'Client disconnected')

@socketio.on('info')
def my_event(message):
    print(str(message))

if __name__ == '__main__':
    print(Fore.RED + 'Server started')
    socketio.run(app, debug=False, host='0.0.0.0')
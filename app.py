from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json as JSON
from colorama import Fore
import os
    
app = Flask(__name__)

socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('gamepad3.html')

@socketio.on('connect')
def test_connect():
    print(Fore.GREEN + 'Client connected' + Fore.RESET)
@socketio.on('disconnect')
def test_disconnect():
    print(Fore.RED + 'Client disconnected' + Fore.RESET)

@socketio.on('info')
def my_event(message):
    os.system('clear')
    print(str(message))

if __name__ == '__main__':
    print(Fore.RED + 'Server started' + Fore.RESET)
    socketio.run(app, debug=False, host='0.0.0.0')
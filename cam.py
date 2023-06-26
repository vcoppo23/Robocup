from flask import Flask, render_template
from flask_socketio import SocketIO, emit ## SocketIO is a python library that allows socket use for flask servers
from colorama import Fore ## Just so messages are different colors

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('cams.html')

@socketio.on('connect')
def test_connect():
    print(Fore.GREEN + 'Client connected' + Fore.RESET)
    

@socketio.on('disconnect')
def test_disconnect():
    print(Fore.RED + 'Client disconnected' + Fore.RESET)

if __name__ == '__main__':
    print(Fore.RED + 'Server started' + Fore.RESET)
    socketio.run(app, debug=False, host='0.0.0.0')



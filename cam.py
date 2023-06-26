from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit ## SocketIO is a python library that allows socket use for flask servers
from colorama import Fore ## Just so messages are different colors
import cv2

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

def get_frame(cam_num):
    cam = cv2.VideoCapture(cam_num)
    cam.set(3,320)
    cam.set(4,240)
    cam.set(cv2.CAP_PROP_FPS, 30)

    while True:
        ret,frame = cam.read()
        if ret:
            alpha = 30
            beta = 1
            frame = cv2.convertScaleAbs(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), alpha, beta)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes() + b'\r\n\r\n')

@app.route('/video_feed0')
def video_feed0():
    return Response(get_frame(0), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed1')
def video_feed1():
    return Response(get_frame(1), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed2')
def video_feed2():
    return Response(get_frame(2), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed3')
def video_feed3():
    return Response(get_frame(3), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    print(Fore.RED + 'Server started' + Fore.RESET)
    socketio.run(app, debug=False, host='0.0.0.0')



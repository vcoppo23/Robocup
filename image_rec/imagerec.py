#create flask server
from flask import Flask, request, jsonify, render_template, Response
import numpy as np
import cv2
from keras.models import load_model

app = Flask(__name__)

model = load_model("converted_keras/keras_Model.h5", compile=False)

# Load the labels
class_names = open("converted_keras/labels.txt", "r").readlines()

# Load the webcam
camera = cv2.VideoCapture(0)

@app.route('/')
def index():
    return render_template('imagerec.html')

def gen_frames():
    while True:
        # Grab the webcamera's image.
        ret, image = camera.read()

        if not ret:
            break
        else:

            # Resize the raw image into (224-height,224-width) pixels
            image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
            

            # Show the image in a window
            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            #cv2.imshow("Webcam Image", image)

            # Make the image a numpy array and reshape it to the models input shape.
            image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

            # Normalize the image array
            image = (image / 127.5) - 1

            # Predicts the model
            prediction = model.predict(image)
            index = np.argmax(prediction)
            class_name = class_names[index]
            confidence_score = prediction[0][index]

            # Print prediction and confidence score
            print("Class:", class_name[2:], end="")
            print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
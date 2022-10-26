from flask import Flask, render_template, request
import inputTest

app = Flask(__name__)

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/result', methods=['POST', 'GET'])
def result():
    name = request.form['Name']
    return render_template('result.html', name=name), inputTest.main()

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=8000)

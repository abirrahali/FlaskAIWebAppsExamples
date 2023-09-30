
# Importing the necessary Libraries
from flask_cors import cross_origin
from flask import Flask, render_template, request
from main import text_to_speech

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
@cross_origin()
def homepage():
    if request.method == 'POST':
        text = request.form['speech']
        gender = request.form['voices']
        text_to_speech(text, gender)
        return render_template('base.html')
    else:
        return render_template('base.html')


if __name__ == "__main__":
    app.run(port=8000, debug=True)
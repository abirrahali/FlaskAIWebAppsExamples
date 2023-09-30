from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from chat import get_response, bot_name
from BERT import answer_question

app = Flask(__name__)
CORS(app)



messages = []
USER = "You"

@app.get('/')
def index_get():
    return render_template("base.html", messages=reversed(messages))



@app.post('/')
def index_post():
    if request.method == "POST":
        text = request.form['text']
        context = request.form['context']
        print(context)

        new_message = {"name": USER, "msg": text}
        messages.append(new_message)

        response = answer_question(text, context)
        
        new_message = {"name": bot_name, "msg": response}
        messages.append(new_message)

        return index_get()


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    # POST request
    if request.method == 'POST':
        print(request.data)
        print(request.get_json())  # parse as JSON

        text = request.get_json().get("message")
        context = request.get_json().get("message")


        response = answer_question(text, context)
        message = {'answer': response}
        return jsonify(message)


if __name__ == '__main__':
    app.run(debug=True)

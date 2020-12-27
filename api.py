from flask import Flask, request, render_template
app = Flask(__name__)

from scan_with_picture import scan_with_picture

@app.route("/imageBase64", methods=["POST"])
def textTospeech():

    imageURL = request.form['text']
    scan_with_picture(imageURL)
    return "empty response is given"


@app.route("/speak", methods=["GET"])
def speak():
    global textAns
    print("speak")
    engine = pyttsx3.init() 
    engine.say(str(textAns))
    engine.runAndWait()
    textAns = ""
    return "hey"

@app.route("/get_report", methods=["GET"])
def confirm():
    # question = request.form['text']
    # answer = chat(question)
    return {"reports" : reports}


@app.route("/send_and_receive", methods=["POST"])
def send_answer():
    question = request.form['text']
    answer = chat(question)
    return answer

@app.route('/')
def home():
    return  render_template('index.html')

# @app.route('/checking', methods=["GET"])
# def doctors():
#     print("it works")
#     return "render"

# @app.route('/lab', methods=["GET"])
# def lab():
#     return  render_template('laboratory.html')

# @app.route('/instructions', methods=["GET"])
# def instructions():
#     return  render_template('instructions.html')

   
    
if __name__ == '__main__':
    app.run(debug=True, port = 5051)

from flask import Flask, request, render_template
app = Flask(__name__)

from picture import scan_with_picture
from pdf import *


@app.route("/imageBase64", methods=["POST"])
def imageBase64():

    imageURL = request.form['text']
    msgs = scan_with_picture(imageURL) 
    return {"msgs" : msgs}


@app.route("/pdfBase64Upload", methods=["POST"])
def pdfBase64():
    pdfURL = request.form['text']
    convertBase64ToPdf(pdfURL)
    return "response from pdfBase64"


@app.route("/pdfBase64GetData", methods=["POST"])
def pdfBase64GetData():
    msgs =  scan_with_pdf()
    print(len(msgs),"length",msgs)
    return {"msgs" : msgs}

@app.route('/')
def home():
    return  render_template('index.html')


    
if __name__ == '__main__':
    app.run(debug=True, port = 5051)

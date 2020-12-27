from flask import Flask, request, render_template
app = Flask(__name__)

from scan_with_picture import scan_with_picture
from code_test import *

@app.route("/imageBase64", methods=["POST"])
def textTospeech():

    imageURL = request.form['text']
    scan_with_picture(imageURL)
    return "response from imageBase64"

@app.route("/pdfBase64", methods=["POST"])
def pdfBase64():

    pdfURL = request.form['text']
    convertBase64ToPdf(pdfURL)
    scan_with_pdf()
    return "response from pdfBase64"
    

@app.route('/')
def home():
    return  render_template('index.html')


    
if __name__ == '__main__':
    app.run(debug=True, port = 5051)

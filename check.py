import base64

def check(pdfURL):
    comma = pdfURL.find(",")
    pdfURL = pdfURL[comma+1:]

    with open('new.pdf', 'wb') as theFile:
        theFile.write(base64.b64decode(pdfURL))

import cv2
import numpy as np
from pyzbar.pyzbar import decode
import time
import minecart
import glob
import xlwt
import base64


def convertBase64ToPdf(pdfURL):
    comma = pdfURL.find(",")
    pdfURL = pdfURL[comma+1:]

    with open('generated.pdf', 'wb') as theFile:
        theFile.write(base64.b64decode(pdfURL))

def scan_with_pdf():
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet("Sheet 1")
    style = xlwt.easyxf('font: bold 1')

    pdffile = open('generated.pdf', 'rb')
    doc = minecart.Document(pdffile)

    page = doc.get_page(0)  # getting a single page

    count = 0
    # iterating through all pages
    for page in doc.iter_pages():
        im = page.images[0].as_pil()  # requires pillow
        count = count + 1
        name = str(count) + '.jpg'
        im.save(name)

    # time.sleep(4)

    for x in range(count):
        image = cv2.imread(str(x+1)+".jpg")
        barcodes = decode(image)
        print("decoded=> ",len(barcodes))

        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type

            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(image, text, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            if barcodeData not in found:
                csv.write("{},{}\n".format(datetime.datetime.now(), barcodeData))
                csv.flush()

            print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
        print("\n")
    workbook.save("example.xls")

    cv2.imshow('Result', image)
    if cv2.waitKey(0):
        cv2.destroyAllWindows()
        # break
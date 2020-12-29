
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import time
import minecart
import glob
import xlwt
import base64
import csv
import argparse
import datetime

from pdf2image import convert_from_path, convert_from_bytes
import fitz


def convertBase64ToPdf(pdfURL):
    comma = pdfURL.find(",")
    pdfURL = pdfURL[comma+1:]
    print("\n =>",pdfURL[:40],"\n")
    with open('generated.pdf', 'wb') as theFile:
        theFile.write(base64.b64decode(pdfURL))


def scan_with_pdf():
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet("Sheet 1")
    style = xlwt.easyxf('font: bold 1')

    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output", type=str, default="barcodes_pdfs.csv",
                    help="Path to output csv file")
    args = vars(ap.parse_args())
    csv = open(args["output"], "w")
    # page = doc.get_page(0)  # getting a single page
    csv.write("{},{},{}\n".format("Date", "Barcode Data","Barcode Type"))

        
    pages = convert_from_path('my.pdf', 500)

    count = 0
    for page in pages:
        count += 1
        page.save(str(count)+'.jpg', 'JPEG')


    for x in range(count):
        image = cv2.imread(str(x+1)+".jpg")
        # image = cv2.imread("my.png")
        barcodes = decode(image)
        print("decoded=> ",len(barcodes))

        found = set()

        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type

            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(image, text, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            if barcodeData not in found:
                csv.write("{},{},{}\n".format(datetime.datetime.now(), barcodeData,barcodeType))
                csv.flush()

            print("[INFO] Found {} barcode: {} ".format(barcodeType, barcodeData))
        print("\n")
    workbook.save("example.xls")

    # cv2.imshow('Result', image)
    # if cv2.waitKey(0):
    #     cv2.destroyAllWindows()
        # break
# scan_with_pdf()


# pdffile = open('2222.pdf', 'rb')
# doc = minecart.Document(pdffile)

# count = 0
# for page in doc.iter_pages():
#     print("checking",page.images[0],"\n",page.images[0].as_pil())
#     im = page.images[0].as_pil()  # requires pillow
#     count = count + 1
#     name = str(count) + '.jpg'
#     im.save(name)


# def pdf2jpeg(pdf_input_path, jpeg_output_path):
# args = ["pef2jpeg", # actual value doesn't matter
#         "-dNOPAUSE",
#         "-sDEVICE=jpeg",
#         "-r144",
#         "-sOutputFile=" + "/home/wajahat/Desktop/qr-and-barcode-detector-translator/",
#         "b.pdf"]

# encoding = locale.getpreferredencoding()
# args = [a.encode(encoding) for a in args]

# ghostscript.Ghostscript(*args)

# import tempfile
# from pdf2image import convert_from_path, convert_from_bytes


# from pdf2image import convert_from_path
# pages = convert_from_path('2222.pdf', 500)

# count = 1
# for page in pages:
#     page.save(str(count)+'.jpg', 'JPEG')
#     count += 1


# doc = fitz.open("b.pdf")
# count = 0
# for i in range(len(doc)):
#     for img in doc.getPageImageList(i):
#         xref = img[0]
#         pix = fitz.Pixmap(doc, xref)
#         print("length",xref,img,"\n",pix)
#         if pix.n < 5:       # this is GRAY or RGB
#             count += 1
#             pix.writePNG("%s.png" % (count)) 
#         else:               # CMYK: convert to RGB first
#             count += 1
#             pix1 = fitz.Pixmap(fitz.csRGB, pix)
#             pix1.writePNG("%s.png" % (count))
#             pix1 = None
#         pix = None


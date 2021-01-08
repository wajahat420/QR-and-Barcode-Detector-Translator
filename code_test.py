
import cv2 as cv
from pyzbar.pyzbar import decode
import base64
import csv  
import datetime

from pdf2image import convert_from_path, convert_from_bytes

def convertBase64ToPdf(pdfURL):
    comma = pdfURL.find(",")
    pdfURL = pdfURL[comma+1:]
    print("\n =>",pdfURL[:40],"\n")
    with open('generated.pdf', 'wb') as theFile:
        theFile.write(base64.b64decode(pdfURL))


def scan_with_pdf():

    pages = convert_from_path('test1.pdf', 500)

    count = 0
    for page in pages:
        count += 1
        page.save(str(count)+'.jpg', 'JPEG')


    for x in range(count):
        image = cv.imread(str(x+1)+".jpg")
        image = cv.resize(image, (1664,2296), interpolation = cv.INTER_AREA)

        imageSplittedInRows = []
        start = 500

        for i in range(6):
            imgCropped = image[start:start + 155,:]
            start += 155
            imageSplittedInRows.append(imgCropped)

        print("decoded=> ",len(imageSplittedInRows))

        data = []
        for image in imageSplittedInRows:
            
            barcodes = decode(image)
            count = 0
            for barcode in barcodes:
                (x, y, w, h) = barcode.rect
                cv.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

                barcodeData = barcode.data.decode("utf-8")
                if count == 0:
                    if x < 900:  # it is an opration
                        data.append({
                            "operation" : barcodeData,
                            "operator" : ""
                        })
                    else:  # it is an operator
                        data.append({
                            "operation" : "",
                            "operator" : barcodeData
                        })
                else:
                    if x < 900: # it is an opration
                        data[len(data) - 1]["operation"] = barcodeData
                    else:
                        data[len(data) - 1]["operator"] = barcodeData

                count += 1
                if count == 2:
                    count = 0

        with open('barcodes_pdfs.csv', mode='w',newline="") as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["DATE", "OPERATION","OPERATOR"])
            for obj in data:
                print(obj)
                writer.writerow([datetime.datetime.now(),obj["operation"], obj["operator"]])
scan_with_pdf()
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


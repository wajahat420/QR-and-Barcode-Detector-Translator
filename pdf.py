
import cv2 as cv
from pyzbar.pyzbar import decode
import base64
import csv  
import datetime

from pdf2image import convert_from_path, convert_from_bytes

bothMissing = []
operatorMissing  =[]
operationMissing = []
moreThanTwo = []
data = []

def convertBase64ToPdf(pdfURL):
    comma = pdfURL.find(",")
    pdfURL = pdfURL[comma+1:]
    print("\n =>",pdfURL[:40],"\n")
    with open('generated.pdf', 'wb') as theFile:
        theFile.write(base64.b64decode(pdfURL))

def getScannedData(imgsArr, counter):
    global bothMissing, operatorMissing, operationMissing, data
    for image in imgsArr:
        # print("=>",data)
        barcodes = decode(image)
        # print("check",len(barcodes))

        print(len(barcodes),counter)
        oneFound = False
        if len(barcodes) == 0:
                bothMissing.append(counter)
        elif len(barcodes)  > 2:
            moreThanTwo.append(counter)
        else: 
            # checkingCounter = 0
            # cv.imshow('col1', image)
            # cv.waitKey(0)    

            internalCount = 0
            for barcode in barcodes:
                    barcodeData = barcode.data.decode("utf-8")
                    if len(barcodes) == 1:
                        if barcode.rect.left > 200: # means opearation is present and operator is missing
                            operationMissing.append(counter)
                        else:
                            operatorMissing.append(counter)
                            
                    else:
                        barcodeData = barcode.data.decode("utf-8")
                        # print("left",counter,"\n")
                        if barcode.rect.left > 200: # means opearator is present and operator is missing
                            if internalCount == 0:
                                # print("if 1")
                                data.append({"operator":barcodeData, "operation" : ""})
                            else:
                                # print("else 2")
                                data[len(data)-1]["operator"] = barcodeData
                                data[len(data)-1]["s.no"] = counter
                                internalCount  = -1
                        else: 
                            if internalCount == 0:
                                # print("if 2")
                                data.append({"operation":barcodeData, "operator" : ""})
                            else:
                                # print("else 2")
                                data[len(data)-1]["operation"] = barcodeData
                                data[len(data)-1]["s.no"] = counter
                                internalCount = -1
                    internalCount += 1

        counter += 1
def scan_with_pdf():

    pages = convert_from_path('generated.pdf', 300)
    pagesArr  = []
    count = 0
    for page in pages:
        count += 1
        pagesArr.append(page)
        page.save(str(count)+'.jpg', 'JPEG')

    for x in range(count):
        image = cv.imread(str(x+1)+".jpg")
        # image = cv.imread(pagesArr[x])
        column1 = image[690:,220:1340] 
        column2 = image[690:,1290:] 

        col1_array = []
        col2_array = []
        totalRows = 12
        betweenDist = 210
        start = 0

        for i in range(totalRows):
            col1 = column1[start: start+betweenDist ,:]
            col2 = column2[start: start+betweenDist, :]
            if i != 0:
                col1 = column1[start-12: start+betweenDist ,:]
                col2 = column2[start-12 :start+betweenDist, :]
        
            start += betweenDist    
            col1_array.append(col1)
            col2_array.append(col2)
            cv.imshow('col'+str(i), col2)
        cv.waitKey(0)

        col1 =  getScannedData(col1_array, counter=0)
        col2 =  getScannedData(col2_array, counter=12)

        print("both",bothMissing)
        print("operator",operatorMissing)
        print("operation",operationMissing)
        print("moreThanTwo",moreThanTwo)
        print("data",len(data))
        # operatorData =  getOperatorData(imageSplittedInRows["operatorImgs"])
        # print(len(operationData))
        with open('barcodes_image.csv', mode='w',newline="") as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["DATE", "OPERATION","OPERATOR"])
            
            for obj in data:
                    # print("operator : ",operatorData[i],"operation : ",operationData[i])
                    
                    # if operatorData[i] == "":
                    #     print(str(i+1)+" row Operator Missing")
                    # elif  operationData[i] == "":
                    #     print(str(i+1)+" row Operation Missing")
                    # else:
                    print(obj)
                    writer.writerow([obj["s.no"],obj["operation"], obj["operation"],datetime.datetime.now()])

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


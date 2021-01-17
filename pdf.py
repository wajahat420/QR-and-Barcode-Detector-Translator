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
header = ""

def convertBase64ToPdf(pdfURL):
    comma = pdfURL.find(",")
    pdfURL = pdfURL[comma+1:]
    print("\n =>",pdfURL[:40],"\n")
    with open('generated.pdf', 'wb') as theFile:
        theFile.write(base64.b64decode(pdfURL))

def getScannedData(imgsArr, counter):
    global bothMissing, operatorMissing, operationMissing, data, header
    for image in imgsArr:
        # print("=>",data)
        barcodes = decode(image)

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
                                data[len(data)-1]["header"] = header
                                internalCount  = -1
                        else: 
                            if internalCount == 0:
                                # print("if 2")
                                data.append({"operation":barcodeData, "operator" : ""})
                            else:
                                # print("else 2")
                                data[len(data)-1]["operation"] = barcodeData
                                data[len(data)-1]["s.no"] = counter
                                data[len(data)-1]["header"] = header

                                internalCount = -1
                    internalCount += 1
        counter += 1
        bothMissing.sort()
        operationMissing.sort()
        operatorMissing.sort()
        moreThanTwo.sort()

def emprtyAllArrays():
    global bothMissing, moreThanTwo, operationMissing, operatorMissing, data
    bothMissing = []
    moreThanTwo  =[]
    operatorMissing = []
    operationMissing = []
    data = []
    header = ""

def scan_with_pdf():
    global header
    pages = convert_from_path('generated.pdf', 300)
    pagesArr  = []
    count = 0
    msgs = []
    emprtyAllArrays()

    for page in pages:
        count += 1
        pagesArr.append(page)
        page.save(str(count)+'.jpg', 'JPEG')
    for x in range(count):
        image = cv.imread(str(x+1)+".jpg")
        column1 = image[690:,220:1340] 
        column2 = image[690:,1290:] 

        headerImg = image[:660,:]
        header = decode(headerImg)[0].data.decode("utf-8")
        print("header ==",header)
        # cv.imshow('col', header)
        # cv.waitKey(0)

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


        col1 =  getScannedData(col1_array, counter=0)
        col2 =  getScannedData(col2_array, counter=12)

        print("both",bothMissing)
        print("operator",operatorMissing)
        print("operation",operationMissing)
        print("moreThanTwo",moreThanTwo)
        print("data",len(data))
        if len(bothMissing) != 0 or len(operationMissing) != 0 or len(operatorMissing) != 0 or len(moreThanTwo) != 0:
            msgs.append("Page-"+str(x+1)+" Errors bolow:")
        for i in bothMissing:
            msgs.append("Error: Both Missing in "+str(i+1)+" row")
        for i in operationMissing:
            msgs.append("Error: Operation Missing in "+str(i+1)+" row")
        for i in operatorMissing:
            msgs.append("Error: Operator Missing in "+str(i+1)+" row")
        for i in moreThanTwo:
            msgs.append("Error: More than two barcodes exists in "+str(i+1)+" row")  
        # msgs.extend(tempMsgs)
        # print("length of msgs: ",len(msgs),msgs)
  
    with open('barcodes_pdf.csv', mode='w',newline="") as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["S.no","OPERATION","OPERATOR","HEADER","DATE"])
        
        for obj in data:
                # print(obj)
                writer.writerow([obj["s.no"],obj["operation"], obj["operator"],obj["header"],datetime.datetime.now()])
    


    return msgs




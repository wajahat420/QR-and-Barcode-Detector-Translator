from pyzbar.pyzbar import decode
import cv2 as cv
import datetime
import base64
import numpy as np
import csv
import pytesseract
from pytesseract import Output

bothMissing = []
operatorMissing  =[]    
operationMissing = []
moreThanTwo = []
data = []

def getScannedData(imgsArr, counter):
    global bothMissing, operatorMissing, operationMissing, data
    for image in imgsArr:
        # print("=>",data)
        barcodes = decode(image)
        # print("check",len(barcodes))

        print(len(barcodes))
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
                        print("left",barcode.rect.left,"\n")
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
def emprtyAllArrays():
    global bothMissing, moreThanTwo, operationMissing, operatorMissing, data
    bothMissing = []
    moreThanTwo  =[]
    operatorMissing = []
    operationMissing = []
    data = []

def scan_with_picture(imgURL=''):
    emprtyAllArrays()
    global bothMissing, operatorMissing, operationMissing, data
    comma = imgURL.find(",")
    imgURL = imgURL[comma+1:]
    imgURL = bytes(imgURL, 'utf-8')

    buf_decode = base64.b64decode(imgURL)
    buf_arr = np.fromstring(buf_decode, dtype=np.uint8)

    image =  cv.imdecode(buf_arr, cv.IMREAD_UNCHANGED)

 
    # image = cv.imread("finalMnD.png")
    
    height, width = image.shape[:2]
    # if height > 2000:
    #     image = cv.resize(image, (1200,1900) , interpolation = cv.INTER_AREA)
    # height, width = image.shape[:2]

      # end finding  
    column1 = image[640:,200:1340] 
    column2 = image[640:,1290:] 
    # cv.imshow('col2', column2)
    # cv.imshow('col1', column1)
    # cv.waitKey(0)

    col1_array = []
    col2_array = []
    totalRows = 12
    betweenDist = 215
    start = 5

    for i in range(totalRows):
        col1 = column1[start-5: start+betweenDist ,:]
        col2 = column2[start-5: start+betweenDist, :]
        start += betweenDist    

        col1_array.append(col1)
        col2_array.append(col2)
        # cv.imshow('col'+str(i), col1)
    # cv.waitKey(0)

    col1 =  getScannedData(col1_array, counter=0)
    col2 =  getScannedData(col2_array, counter=12)

    print("both",bothMissing)
    print("operator",operatorMissing)
    print("operation",operationMissing)
    print("moreThanTwo",moreThanTwo)
    print("data",len(data))

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
    msgs = []
    for i in bothMissing:
        msgs.append("Error: Both Missing in "+str(i+1)+" row")
    for i in operationMissing:
        msgs.append("Error: Operation Missing in "+str(i+1)+" row")
    for i in operatorMissing:
        msgs.append("Error: Operator Missing in "+str(i+1)+" row")
    for i in moreThanTwo:
        msgs.append("Error: More than two barcodes exists in "+str(i+1)+" row")  

    return msgs
# scan_with_picture("")



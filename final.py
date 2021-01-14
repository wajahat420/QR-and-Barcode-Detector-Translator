from pyzbar.pyzbar import decode
import cv2 as cv
import datetime
import base64
import numpy as np
import csv
import pytesseract
from pytesseract import Output


def getOperationData(imgsArr):
      operations = []

      for image in imgsArr:    
            barcodes = decode(image)
            if len(barcodes) == 0:
                  operations.append("")
            for barcode in barcodes:
                  barcodeData = barcode.data.decode("utf-8")
                  operations.append(barcodeData)
      return operations  
# elif tempOperator.shape[0] == 0:
#       print(str(i)+"th Operator Missing, But Its Operation is available")
# else:
#       print(str(i)+"th Operation Missing, But Its Operator is available")


def getOperatorData(imgsArr):
      operators = []

      for image in imgsArr:
            # print("a",image.shape)
            barcodes = decode(image)
            if len(barcodes) == 0:
                  operators.append("")
            for barcode in barcodes:
                  barcodeData = barcode.data.decode("utf-8")
                  operators.append(barcodeData)
      return operators

bothMissing = []
operatorMissing  =[]
operationMissing = []

def getScannedData(imgsArr, counter):
    global bothMissing, operatorMissing, operationMissing
    data = [] 
    for image in imgsArr:
        barcodes = decode(image)
        # print(len(barcodes))
        oneFound = False
        if len(barcodes) == 0:
                bothMissing.append(counter)
        elif len(barcodes) ==1: 
            oneFound = True
        for barcode in barcodes:
                barcodeData = barcode.data.decode("utf-8")
                if oneFound:
                    if barcode.rect.left < 200: # means opearation is present and operator is missing
                        operatorMissing.append(counter)
                    else:
                        operationMissing.append(counter)


                else:
                    data.append(barcodeData)
                
        counter += 1
    return data

def scan_with_picture(imgURL=''):
    global bothMissing, operatorMissing, operationMissing
      # comma = imgURL.find(",")
      # imgURL = imgURL[comma+1:]
      # imgURL = bytes(imgURL, 'utf-8')

      # buf_decode = base64.b64decode(imgURL)
      # buf_arr = np.fromstring(buf_decode, dtype=np.uint8)

      # image =  cv.imdecode(buf_arr, cv.IMREAD_UNCHANGED)

 
    image = cv.imread("finalMnD.png")
    
    height, width = image.shape[:2]
    # if height > 2000:
    #     image = cv.resize(image, (1200,1900) , interpolation = cv.INTER_AREA)
    # height, width = image.shape[:2]


    #  finding first top barcodes of operation and operator to get their position
    barcodes = decode(image)

      # end finding  
    column1 = image[640:,:1340] 
    column2 = image[640:,1290:] 
    # cv.imshow('col2', column2)
    # cv.imshow('col1', column1)
    # print("works",tempOperator.shape)
    # cv.waitKey(0)

    # operation = image[operatorStartPos[0]-40:int(height*0.8),:int(width*0.6)] 
    # operator = image[operationStartPos[0]-40:int(height*0.8),int(width*0.45):]
    # imageSplittedInRows = {
    #     "operationImgs" : [],
    #     "operatorImgs" : []
    # }
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
    # operatorData =  getOperatorData(imageSplittedInRows["operatorImgs"])
    # print(len(operationData))
    with open('barcodes_image.csv', mode='w',newline="") as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["DATE", "OPERATION","OPERATOR"])
        
        for i in range(len(operationData)):
                print("operator : ",operatorData[i],"operation : ",operationData[i])
                
                if operatorData[i] == "":
                    print(str(i+1)+" row Operator Missing")
                elif  operationData[i] == "":
                    print(str(i+1)+" row Operation Missing")
                else:
                    writer.writerow([datetime.datetime.now(), operationData[i], operatorData[i]])

scan_with_picture("")



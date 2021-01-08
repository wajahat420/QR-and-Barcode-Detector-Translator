from pyzbar.pyzbar import decode
import cv2 as cv
import datetime
import base64
import numpy as np
import csv
import pytesseract
from pytesseract import Output

from pdf2image import convert_from_path, convert_from_bytes

def convertBase64ToPdf(pdfURL):
    comma = pdfURL.find(",")
    pdfURL = pdfURL[comma+1:]
    print("\n =>",pdfURL[:40],"\n")
    with open('generated.pdf', 'wb') as theFile:
        theFile.write(base64.b64decode(pdfURL))


def getOperationData(imgsArr):
      operations = []

      for image in imgsArr:    
            barcodes = decode(image)

            for barcode in barcodes:
                  barcodeData = barcode.data.decode("utf-8")
                  operations.append(barcodeData)
      return operations
               

def getOperatorData(imgsArr):
      operators = []

      for image in imgsArr:
            barcodes = decode(image)

            for barcode in barcodes:
                  barcodeData = barcode.data.decode("utf-8")
                  operators.append(barcodeData)
      return operators

def scan_with_pdf():
    global img, initial_start, data, all_y, index, iter_no

    pages = convert_from_path('test1.pdf', 500)

    count = 0
    for page in pages:
        count += 1
        page.save(str(count)+'.jpg', 'JPEG')

      

    for x in range(count):
        image = cv.imread(str(x+1)+".jpg")  
        image = cv.resize(image, (1100,1900) , interpolation = cv.INTER_AREA)

        height, width = image.shape[:2]
        if height > 2500:
            image = cv.resize(image, (1200,1900) , interpolation = cv.INTER_AREA)
        
        #  finding first top barcodes of operation and operator to get their position
        barcodes = decode(image)
        operationStartPos = [barcodes[0].rect.top,barcodes[0].rect.left] # 0 index = top, 1 index = left
        operatorStartPos = [0,0]  # 0 index = top, 1 index = left
        margin = 80       #  operator must be atleast 80 pixels farther from operation
        operationEndPos = [barcodes[0].rect.top,barcodes[0].rect.left] 
        operatorEndPos = [0,0]

        for barcode in barcodes:
                barcodeData = barcode.data.decode("utf-8")
                top = barcode.rect.top
                left = barcode.rect.left

                if left > operationStartPos[1] + margin : #checking it is opeartor or not
                    if operatorStartPos[0] == 0 :
                            operatorStartPos[0] = top
                            operatorStartPos[1]  =left
                            # operatorEndPos[0] = top
                            # operatorEndPos[1]  =left

                    elif top < operatorStartPos[0]:
                            operatorStartPos[0] = top
                            operatorStartPos[1]  =left
                    # else:
                    #     operatorEndPos[0] = top
                    #     operatorEndPos[1]  =left
                else:
                    if top < operationStartPos[0]:
                            operationStartPos[0] = top
                            operationStartPos[1] = left
                    # else:
                    #     operationEndPos[0] = top
                    #     operationEndPos[1]  =left
                print("data",barcodeData,"top",top,"left",left)

        print("operationStartPos",operationStartPos,"operationEndPos",operationEndPos)
        print("operatorStartPos",operatorStartPos,"operatorEndPos",operatorEndPos)
                                             
        # end finding  
        operator = image[operatorStartPos[0]-40:int(height*0.82),int(width*0.55):] 
        operation = image[operationStartPos[0]-40:int(height*0.82),:int(width*0.65)]

        imageSplittedInRows = {
                "operationImgs" : [],
                "operatorImgs" : []
        }
        totalRows = 6

        # try:
        operationDistance = int(operation.shape[0] / totalRows)
        operatorDistance = int(operator.shape[0] / totalRows)
        start1 = 0
        for i in range(totalRows):
            tempOperation = operation[start: start+operationDistance ,:]
            tempOperator = operator[start: start+operatorDistance, :]

            imageSplittedInRows["operationImgs"].append(tempOperation)
            imageSplittedInRows["operatorImgs"].append(tempOperator)

            start += dividedDistance
            cv.imshow('img'+str(i), tempOperation)
        cv.waitKey(0)
        operatorData =  getOperatorData(imageSplittedInRows["operatorImgs"])
        operationData =  getOperationData(imageSplittedInRows["operationImgs"])
        print("")
        # with open('barcodes_image.csv', mode='w',newline="") as file:
        #     writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        #     writer.writerow(["DATE", "OPERATION","OPERATOR"])

        #     for i in range(len(operatorData)):
        #         print("operator : ",operatorData[i],"operation : ",operationData[i])
        #         writer.writerow([datetime.datetime.now(), operationData[i], operatorData[i]])

        #         if operatorData[i] == "":
        #                 print(str(i)+"th operator missing")
        #         elif  operationData[i] == "":
                        # print(str(i)+"th operation missing")
        # except:
        #     print("Errors Are Coming Kindly Resolve")

    
scan_with_pdf()



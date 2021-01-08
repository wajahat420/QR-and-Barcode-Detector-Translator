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

            for barcode in barcodes:
                  barcodeData = barcode.data.decode("utf-8")
                  operations.append(barcodeData)
      return operations
               

def getOperatorData(imgsArr):
      operators = []

      for image in imgsArr:
            # print("a",image.shape)
            barcodes = decode(image)
            for barcode in barcodes:
                  barcodeData = barcode.data.decode("utf-8")
                  operators.append(barcodeData)
      return operators

def scan_with_picture(imgURL=''):
      global img, initial_start, data, all_y, index, iter_no

      # comma = imgURL.find(",")
      # imgURL = imgURL[comma+1:]
      # imgURL = bytes(imgURL, 'utf-8')

      # buf_decode = base64.b64decode(imgURL)
      # buf_arr = np.fromstring(buf_decode, dtype=np.uint8)

      # image =  cv.imdecode(buf_arr, cv.IMREAD_UNCHANGED)

 
      image = cv.imread("actual.jpg")
      
      height, width = image.shape[:2]
      # if height > 2000:
      #       image = cv.resize(image, (1100,1700) , interpolation = cv.INTER_AREA)
      print(image.shape)


      #  finding first top barcodes of operation and operator to get their position
      barcodes = decode(image)
      operationStartPos = [barcodes[0].rect.top,barcodes[0].rect.left] # 0 index = top, 1 index = left
      operatorStartPos = [0,0]  # 0 index = top, 1 index = left
      margin = 80       #  operator must be atleast 80 pixels farther from operation
      print("length",len(barcodes))

      for barcode in barcodes:
            barcodeData = barcode.data.decode("utf-8")
            top = barcode.rect.top
            left = barcode.rect.left  
            print(barcodeData,left,top)

            if left > operationStartPos[1] + margin : #checking it is opeartor or not
                  if operatorStartPos[0] == 0 or top < operatorStartPos[0]:
                        operatorStartPos[0] = top 
                        operatorStartPos[1]  =left
                  # print("abc")
            else:
                  if top < operationStartPos[0]:
                        operationStartPos[0] = top
                        operationStartPos[1] = left
                                          
      # end finding  
      operation = image[operatorStartPos[0]-40:int(height*0.9),:int(width*0.6)] 
      operator = image[operationStartPos[0]-40:int(height*0.9),int(width*0.55):]
      imageSplittedInRows = {
            "operationImgs" : [],
            "operatorImgs" : []
      }
      totalRows = 10

      # try:
      operationDistance = int(operation.shape[0] / totalRows)
      start1 = 0
      operatorDistance = int(operator.shape[0] / totalRows) -1
      start2 = 0
      for i in range(totalRows):
            tempOperation = operation[start1: start1+operationDistance ,:]
            tempOperator = operator[start1: start1+operationDistance, :]
            # print(tempOperation.shape[0])

            if tempOperator.shape[0] != 0 and tempOperation.shape[0] != 0:
                  imageSplittedInRows["operationImgs"].append(tempOperation)
                  imageSplittedInRows["operatorImgs"].append(tempOperator)
                  start1 += operationDistance
                  # start2 += operatorDistance
                  
                  cv.imshow('img'+str(i), tempOperator)
                  # print("works",tempOperator.shape)
      
      cv.waitKey(0)
      operationData =  getOperationData(imageSplittedInRows["operationImgs"])
      operatorData =  getOperatorData(imageSplittedInRows["operatorImgs"])
      print("")
      with open('barcodes_image.csv', mode='w',newline="") as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["DATE", "OPERATION","OPERATOR"])

            for i in range(len(operationData)):
                  print("operator : ",operatorData[i],"operation : ",operationData[i])
                  writer.writerow([datetime.datetime.now(), operationData[i], operatorData[i]])

                  if operatorData[i] == "":
                        print(str(i)+"th operator missing")
                  elif  operationData[i] == "":
                        print(str(i)+"th operation missing")

scan_with_picture("")



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

def scan_with_picture(imgURL=''):
      global img, initial_start, data, all_y, index, iter_no

      # comma = imgURL.find(",")
      # imgURL = imgURL[comma+1:]
      # imgURL = bytes(imgURL, 'utf-8')

      # buf_decode = base64.b64decode(imgURL)
      # buf_arr = np.fromstring(buf_decode, dtype=np.uint8)

      # image =  cv.imdecode(buf_arr, cv.IMREAD_UNCHANGED)

 
      image = cv.imread("3.jpg")
      
      height, width = image.shape[:2]
      if height > 2000:
            image = cv.resize(image, (1200,1900) , interpolation = cv.INTER_AREA)
      height, width = image.shape[:2]


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
            # print(barcodeData,"left",left,"top",top)

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
      operation = image[operatorStartPos[0]-40:int(height*0.8),:int(width*0.6)] 
      operator = image[operationStartPos[0]-40:int(height*0.8),int(width*0.45):]
      imageSplittedInRows = {
            "operationImgs" : [],
            "operatorImgs" : []
      }
      totalRows = 6

      operationDistance = int(operation.shape[0] / totalRows)
      start1 = 0
      operatorDistance = int(operator.shape[0] / totalRows) 
      start2 = 0
      for i in range(totalRows):
            tempOperation = operation[start1: start1+operationDistance ,:]
            tempOperator = operator[start2: start2+operatorDistance, :]
            print(tempOperation.shape,tempOperator.shape)

            if tempOperator.shape[0] != 0 and tempOperation.shape[0] != 0:
                  imageSplittedInRows["operatorImgs"].append(tempOperator)
                  imageSplittedInRows["operationImgs"].append(tempOperation)

            start2 += operatorDistance
            start1 += operationDistance
            cv.imshow('img'+str(i), tempOperator)
                  # print("works",tempOperator.shape)
      
      cv.waitKey(0)
      operationData =  getOperationData(imageSplittedInRows["operationImgs"])
      operatorData =  getOperatorData(imageSplittedInRows["operatorImgs"])
      print(len(operationData))
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



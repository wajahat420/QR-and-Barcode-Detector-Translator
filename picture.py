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
      d = pytesseract.image_to_data(image, output_type=Output.DICT)
      n_boxes = len(d['level'])

      for i in range(n_boxes):
            if d["text"][i] == "Operation":
                  (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                  cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                  operation = image[y:int(height*0.9),:int(width*0.65)]

            elif d["text"][i] == "Emp.Stick":
                  (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                  cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                  operator = image[y:int(height*0.9),int(width*0.55):]


      imageSplittedInRows = {
            "operationImgs" : [],
            "operatorImgs" : []
      }

      dividedDistance = int(operator.shape[0] / 10)
      start = 0
      for i in range(10):
            tempOperation = operation[start: start+dividedDistance ,:]
            tempOperator = operator[start: start+dividedDistance, :]

            imageSplittedInRows["operationImgs"].append(operation)
            imageSplittedInRows["operatorImgs"].append(operator)

            start += dividedDistance
            # cv.imshow('img', tempOperator)
      # cv.waitKey(0)
      operatorData =  getOperatorData(imageSplittedInRows["operatorImgs"])
      operationData =  getOperationData(imageSplittedInRows["operationImgs"])

      with open('barcodes_image.csv', mode='w',newline="") as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["DATE", "OPERATION","OPERATOR"])

            for i in range(len(operatorData)):
                  print("operator : ",operatorData[i],"operation : ",operationData[i])
                  writer.writerow([datetime.datetime.now(), operationData[i], operatorData[i]])

                  if operatorData[i] == "":
                        print(str(i)+"th operator missing")
                  elif  operationData[i] == "":
                        print(str(i)+"th operation missing")

scan_with_picture("")



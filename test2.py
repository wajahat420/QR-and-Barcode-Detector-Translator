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

      # gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
      # (thresh, blackAndWhiteImage) = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)

      image = cv.imread("2.jpg")
      print(image.shape)

      height, width = image.shape[:2]
      if height > 2000:
            image = cv.resize(image, (1200,1900) , interpolation = cv.INTER_AREA)
      height, width = image.shape[:2]

      image =  image[:,:int(width*0.5)]  #int(width*0.48)
      cv.imshow("Threshold", image) 
      cv.waitKey(0)  
      cv.destroyAllWindows()
      barcodes = decode(image)
      print("length= ",len(barcodes))

      operation = [barcodes[0].rect.top,barcodes[0].rect.left] # 0 index = top, 1 index = left
      operator = [0,0]  # 0 index = top, 1 index = left
      margin = 80

      # print(operation)
      for barcode in barcodes:
            barcodeData = barcode.data.decode("utf-8")
            top = barcode.rect.top
            left = barcode.rect.left
            # print(operation[1])
            if left > operation[1] + margin : #checking it is opeartor or not
                  if operator[0] == 0:
                        operator[0] = top
                        operator[1]  =left
                  elif top < operator[0]:
                        operator[0] = top
                        operator[1] = left

            else:
                  if top < operation[0]:
                        operation[0] = top
                        operation[1] = left
            print("barcode",barcodeData,"top",top,"left",left)
            
      print("operation",operation)
      print("operator",operator)

          
scan_with_picture("")



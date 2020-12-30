from pyzbar.pyzbar import decode
import cv2 as cv
import datetime
import base64
import numpy as np
import csv

frequency = 2500
duration = 1000

def scan_with_picture(imgURL):

    comma = imgURL.find(",")
    imgURL = imgURL[comma+1:]
    imgURL = bytes(imgURL, 'utf-8')

    buf_decode = base64.b64decode(imgURL)
    buf_arr = np.fromstring(buf_decode, dtype=np.uint8)

    image =  cv.imdecode(buf_arr, cv.IMREAD_UNCHANGED)

    imageSplittedInRows = []
    start = 450
    for i in range(10):
        imgCropped = image[start:start + 165,:]
        start += 165
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
  
    with open('barcodes_image.csv', mode='w',newline="") as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["DATE", "OPERATION","OPERATOR"])
        for obj in data:
            print(obj)
            writer.writerow([datetime.datetime.now(),obj["operation"], obj["operator"]])

        # cv.imshow("image", image)
        # cv.waitKey(0)
        # cv.destroyAllWindows()

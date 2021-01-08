from pyzbar.pyzbar import decode
import cv2 as cv
import datetime
import base64
import numpy as np
import csv

img = ""
initial_start = 200
data = []
all_y = []
index = 0
iter_no = 1


def scan_with_picture(imgURL=''):
    global img, initial_start, data, all_y, index, iter_no

    if imgURL != "" :
        comma = imgURL.find(",")
        imgURL = imgURL[comma+1:]
        imgURL = bytes(imgURL, 'utf-8')

        buf_decode = base64.b64decode(imgURL)
        buf_arr = np.fromstring(buf_decode, dtype=np.uint8)

        image =  cv.imdecode(buf_arr, cv.IMREAD_UNCHANGED)
        img = image

    image = img

    image = cv.imread("actual.jpg")
    imageSplittedInRows = []
    start = initial_start

    for i in range(10):
        imgCropped = image[start:start + 165,:]
        start += 165
        imageSplittedInRows.append(imgCropped)

    # print("decoded=> ",len(imageSplittedInRows))

    for image in imageSplittedInRows:
        
        barcodes = decode(image)
        # print("lenght",len(barcodes))
        count = 0
        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            cv.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

            barcodeData = barcode.data.decode("utf-8")

            if iter_no == 2 :
                pass
                # for obj in data:
                #     if x < 700 and obj["operation"] != barcodeData:

                # if y not in all_y and x < 700: # it is an opration
                #     data[index]["operation"] = barcodeData
                # else:
                #     data[index]["operator"] = barcodeData

            elif count == 0:
                # print("A")
                if x < 700:  # it is an opration
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
                # print("B")
                if x < 700: # it is an opration
                    data[len(data) - 1]["operation"] = barcodeData
                else:
                    data[len(data) - 1]["operator"] = barcodeData
            # if y not in all_y:
            #     all_y.append(y)

            count += 1
            if count == 2:
                count = 0
    # print("y =",len(all_y))
    with open('barcodes_image.csv', mode='w',newline="") as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["DATE", "OPERATION","OPERATOR"])
        counter = 0

        for obj in data:
            # print(obj,len(data))
            if obj["operation"] == "" or obj["operator"] == "":
                initial_start += 50
                iter_no = 2
                index = counter
                scan_with_picture()
            writer.writerow([datetime.datetime.now(),obj["operation"], obj["operator"]])
            counter += 1

        # cv.imshow("image", image)
        # cv.waitKey(0)
        # cv.destroyAllWindows()
scan_with_picture("")
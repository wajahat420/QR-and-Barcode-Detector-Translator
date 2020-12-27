import cv2
import numpy as np
from pyzbar.pyzbar import decode
import time
import minecart
import glob
import xlwt

workbook = xlwt.Workbook()
sheet = workbook.add_sheet("Sheet 1")
style = xlwt.easyxf('font: bold 1')

pdffile = open('wagecard.pdf', 'rb')
doc = minecart.Document(pdffile)

page = doc.get_page(0)  # getting a single page

count = 1
# iterating through all pages
for page in doc.iter_pages():
    im = page.images[0].as_pil()  # requires pillow
    name = str(count) + '.jpg'
    count = count + 1
    im.save(name)

time.sleep(10)
# path = r'C:\Users\saad9\Desktop\FYP\CodeScanner'
# file location
path = glob.glob("*.jpg")
cv_img = []
for multiple_files in path:
    img = cv2.imread(multiple_files)
    cv_img.append(img)
# img = cv2.imread('2.jpg')
resized_image = cv2.resize(img, (768, 800))
# img = cv2.imread('1.png')
# cap = cv2.VideoCapture(0)
# cap.set(3, 640)
# cap.set(4, 480)

with open('myDatafile.txt') as f:
    myDatalist = f.read().splitlines()
# print(myDatalist)

while True:
    data_array = []
    # succes= img.read()
    # code = decode(img)
    for barcode in decode(img):
        # print(barcode.data)
    # print(barcode.rect)
        myData = barcode.data.decode('utf-8')
        # print(myData)
        scanned_data = data_array.append(myData)
        print(scanned_data)

        if myData in myDatalist:
            # myOutput = 'Authorized'
            myColor = (0, 0, 255)   
        else:
            # myOutput = 'Un-Authorized'
            myColor = (0, 255, 255)
        # for bounding area
        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True, myColor, 5)

        pts2 = barcode.rect
        cv2.putText(img, myData, (pts2[0], pts2[1]),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, myColor, 2)
        
    
    workbook.save("example.xls")

    cv2.imshow('Result', resized_image)
    cv2.waitKey(1) 
    cv2.destroyAllWindows()

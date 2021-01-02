import cv2
import numpy as np

font = cv2.FONT_HERSHEY_COMPLEX

img = cv2.imread("actual.jpg", cv2.IMREAD_GRAYSCALE)
# resizeImg = cv2.resize(img, (1500,950) , interpolation = cv2.INTER_AREA)
height, width = img.shape[:]

img = img[850:,:int(width*0.7)]
_, threshold = cv2.threshold(img, 240, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# count = 1
for cnt in contours:
      approx = cv2.approxPolyDP(cnt, 0.05*cv2.arcLength(cnt, False), True)
      
      x = approx.ravel()[0]
      y = approx.ravel()[1]

      if len(approx) == 4:
            # if approx[0][0][0] > approx[1][0][0] + 30:
            cv2.drawContours(img, [approx], 0, (0,255,0), 5)
            # print("number = ",approx)
            # cv2.putText(img, "Rectangle", (x, y), font, 1, (0))
            # count += 1

cv2.imshow("shapes", img)
# cv2.imshow("Threshold", threshold)
cv2.waitKey(0)
cv2.destroyAllWindows()
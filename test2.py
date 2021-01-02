# Python program to illustrate HoughLine 
# method for line detection 
import cv2 
import numpy as np 
  
# Reading the required image in  
# which operations are to be done.  
# Make sure that the image is in the same  
# directory in which this python program is 
img = cv2.imread('actual.jpg') 
img = img[600:,:]

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
print(edges)
lines = cv2.HoughLines(edges,2,np.pi/2,30)
# print("lines",lines)
for line in lines:
      for rho,theta in line:
            if theta >= 1.57:
                  a = np.cos(theta)
                  b = np.sin(theta)
                  x0 = a*rho
                  y0 = b*rho
                  x1 = int(x0 + 1000*(-b))
                  y1 = int(y0 + 1000*(a))
                  x2 = int(x0 - 1000*(-b))
                  y2 = int(y0 - 1000*(a))
                  
                  # print(rho, "theeta = ",theta)
                  print('(',x0,y0,')','(',x1,y1,')','(',x2,y2,')')
                  cv2.line(img,(x2-200,y2-200),(x2,y2),(0,0,255),2)

   
# cv2.imshow("lines", lines)
cv2.imshow("img", img)
# cv2.imshow("edges", edges)

# cv2.imshow("Threshold", threshold)
cv2.waitKey(0)
cv2.destroyAllWindows()
# All the changes made in the input image are finally 
# written on a new image houghlines.jpg
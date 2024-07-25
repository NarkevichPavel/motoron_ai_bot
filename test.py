import cv2

img = cv2.imread('images/AQAD1doxG-ZqqEh-.png')

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img = cv2.Canny(img, 600, 600)

cv2.imshow('result', img)
cv2.waitKey(delay=0)

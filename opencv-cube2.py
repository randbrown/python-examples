import cv2
import numpy as np

def findcube(filename):
    img = cv2.imread(filename)

    # H = [0,255] 
    # S = [0,255] 
    # L = [0,255] 
    # img = cv2.inRange(img, (H[0], L[0], S[0]),  (H[1], L[1], S[1]))


    hue = [21.043165467625897, 61.98269008923929]
    sat = [128.41726618705036, 255.0]
    val = [20.774129310230173, 255.0]
    out = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    out = cv2.inRange(out, (hue[0], sat[0], val[0]),  (hue[1], sat[1], val[1]))
    masked = cv2.bitwise_and(img, img, mask = out)
    img = masked

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    gray = np.float32(gray)
    # dst = cv2.cornerHarris(gray,2,3,0.04)
    dst = cv2.cornerHarris(gray,2,3,0.04)

    #result is dilated for marking the corners, not important
    dst = cv2.dilate(dst,None)

    # Threshold for an optimal value, it may vary depending on the image.
    #img[dst>0.01*dst.max()]=[0,255,0]
    img[dst>0.01*dst.max()]=[0,255,0]

    cv2.namedWindow(filename, cv2.WINDOW_NORMAL)
    cv2.imshow(filename,img)


findcube('pics/cube_distance.jpg')
findcube('pics/powercubes.jpg')
findcube('pics/powercube.jpg')
findcube('pics/cube_obstructed.jpg')


cv2.waitKey(0)
cv2.destroyAllWindows()
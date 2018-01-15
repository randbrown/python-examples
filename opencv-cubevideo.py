import cv2
import numpy as np
import time

cv2.namedWindow("Original Image",cv2.WINDOW_NORMAL)
cv2.namedWindow("Gray Converted Image",cv2.WINDOW_NORMAL)
cv2.namedWindow("Noise Removed Image",cv2.WINDOW_NORMAL)
cv2.namedWindow("Image after Thresholding",cv2.WINDOW_NORMAL)
cv2.namedWindow("Image after applying Canny",cv2.WINDOW_NORMAL)
cv2.namedWindow("Dilation", cv2.WINDOW_NORMAL)
# cv2.namedWindow("Blur", cv2.WINDOW_NORMAL)
cv2.namedWindow("Shape", cv2.WINDOW_NORMAL)
cv2.namedWindow("Corners", cv2.WINDOW_NORMAL)

def processFrame(img):
    if(img is None):
        return

    cv2.imshow("Original Image",img)

    img = cv2.resize(img, (320, 240))

    # img[np.where((img < [10,10,10]).all(axis = 2))] = [0,33,166]
    #img[np.where((img > [180,180,180]).all(axis = 2))] = [255,255,0]
    # img[np.where((img > [150,150,150]).all(axis = 2))] = [0,255,255]
    # # out = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
    # # #out = cv2.inRange(out, (100, 100, 100),  (255,255,255))
    # # c = cv2.inRange(out, (0, 0, 0), (100, 100, 100))
    # # masked = cv2.bitwise_and(img, img, mask = out)
    # cv2.imshow("White masked",img)

    # hue = [21.043165467625897, 61.98269008923929]
    # sat = [128.41726618705036, 255.0]
    # val = [20.774129310230173, 255.0]
    # out = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # out = cv2.inRange(out, (hue[0], sat[0], val[0]),  (hue[1], sat[1], val[1]))
    # masked = cv2.bitwise_and(img, img, mask = out)
    # img = masked

    hue = [21.043165467625897, 61.98269008923929]
    sat = [128.41726618705036, 255.0]
    val = [20.774129310230173, 255.0]
    out = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    out = cv2.inRange(out, (hue[0], sat[0], val[0]),  (hue[1], sat[1], val[1]))
    masked = cv2.bitwise_and(img, img, mask = out)
    img = masked

    # RGB to Gray scale conversion
    img_gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    
    cv2.imshow("Gray Converted Image",img_gray)

    # Noise removal with iterative bilateral filter(removes noise while preserving edges)
    # noise_removal = cv2.bilateralFilter(img_gray,9,75,75)
    noise_removal = cv2.bilateralFilter(img_gray,9,75,75)
    cv2.imshow("Noise Removed Image",noise_removal)
    # Thresholding the image
    ret,thresh_image = cv2.threshold(noise_removal,0,255,cv2.THRESH_OTSU)
    cv2.imshow("Image after Thresholding",thresh_image)

    # Applying Canny Edge detection
    canny_image = cv2.Canny(thresh_image,250,255)
    #canny_image = cv2.Canny(thresh_image,500,255)
    # Creating a Named window to display image
    cv2.imshow("Image after applying Canny",canny_image)
    canny_image = cv2.convertScaleAbs(canny_image)

    # dilation to strengthen the edges
    kernel = np.ones((3,3), np.uint8)
    # Creating the kernel for dilation
    dilated_image = cv2.dilate(canny_image,kernel,iterations=1)
    cv2.imshow("Dilation", dilated_image)
    
    dilated_image = cv2.dilate(canny_image,kernel,iterations=1)
    cv2.imshow("Dilation", dilated_image)
    # dilated_image = cv2.medianBlur(dilated_image, 9)
    # cv2.imshow("Blur", dilated_image)

    #cv2.waitKey(0)
    #contours_img, contours, h = cv2.findContours(dilated_image, 1, 2)
    contours_img, contours, h = cv2.findContours(dilated_image, cv2.RETR_EXTERNAL, 2) #seems best, only outside contours
    # contours_img, contours, h = cv2.findContours(dilated_image, cv2.RETR_LIST, 2) # not good
    #contours_img, contours, h = cv2.findContours(dilated_image, cv2.RETR_TREE, 2)
    # contours_img, contours, h = cv2.findContours(dilated_image, cv2.RETR_CCOMP, 2) #ok
    #import pdb; pdb.set_trace()
    contours= sorted(contours, key = cv2.contourArea, reverse = True)[:1]
    pt = (10, 3 * img.shape[0] // 4)
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        print (len(approx))
        shapename = 'Unknown'
        textcolor = (255,255,255)
        numCorners = len(approx)
        if numCorners == 4:
            shapename="Square"
            textcolor = [0,255,0]
        elif numCorners == 5:
            shapename="Cube (maybe)"
            textcolor = [0,255,0]
        elif numCorners ==6 :
            shapename="Cube"
            textcolor = [0,255,0]
        elif numCorners == 7:
            shapename="Cube"
            textcolor = [0,255,0]
        elif numCorners > 7:
            shapename="Blob"
            textcolor = [255,0,0]
        
        shapename = shapename + ' ' + str(len(contours)) + ' ' + str(len(approx))
        print (shapename)
        cv2.drawContours(img,[cnt],-1,(255,0,0),3)
        rect = cv2.boundingRect(cnt)
        if(rect is not None):
            x,y,w,h = rect
            center = (x+w//2, y+h//2)
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
            cv2.circle(img, center, 8, (0, 0, 255), -1)
            pt2 = (10, 4 * img.shape[0] // 4)
            cv2.putText(img, str(center[0]) + ', ' + str(center[1]), pt2 ,cv2.FONT_HERSHEY_PLAIN, 3,textcolor, 2)
        cv2.putText(img,shapename, pt ,cv2.FONT_HERSHEY_PLAIN, 3,textcolor, 2)

    cv2.imshow('Shape',img)

    #corners    = cv2.goodFeaturesToTrack(thresh_image,6,0.06,25)
    #corners    = cv2.goodFeaturesToTrack(contours_img,6,0.06,25)
    corners    = cv2.goodFeaturesToTrack(contours_img,6,0.06,12)
    if corners is not None:
        corners    = np.float32(corners)
        for    item in    corners:
            x,y    = item[0]
            cv2.circle(img,(x,y),10,255,-1)
    cv2.imshow("Corners",img)
    cv2.waitKey(1)

cap = cv2.VideoCapture('videos/IMG_3567.MOV')
#cap = cv2.VideoCapture('videos/IMG_3568.MOV')
#cap = cv2.VideoCapture('videos/IMG_3569.MOV')

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if frame is None:
        break;
    processFrame(frame)

cv2.waitKey()
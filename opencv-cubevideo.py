import cv2
import numpy as np
import time

cv2.namedWindow("Original Image",cv2.WINDOW_NORMAL)
cv2.namedWindow("Canny",cv2.WINDOW_NORMAL)
cv2.namedWindow("Shape",cv2.WINDOW_NORMAL)

def analyzeContour(img, cnt, idx):
    img_annotated = img.copy()
    pt = (10, 3 * img.shape[0] // 4)
    hull = cv2.convexHull(cnt)
    approx = cv2.approxPolyDP(hull,0.01*cv2.arcLength(hull,True),True)
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
    
    shapename = shapename + ' ' + str(len(approx))
    print (shapename)
    # cv2.drawContours(img_annotated,[hull],-1,(255,0,0),3)
    #rect = cv2.boundingRect(hull)
    rect = cv2.minAreaRect(hull)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    rect = box
    cv2.drawContours(img_annotated,[box],0,(0,0,255),2)
    M = cv2.moments(cnt)
    center = (int(M['m10']/M['m00']), int(M['m01']/M['m00']))
    # cv2.rectangle(img_annotated,(x,y),(x+w,y+h),(0,255,0),3)
    cv2.circle(img_annotated, center, 8, (0, 0, 255), -1)
    pt2 = (10, 4 * img_annotated.shape[0] // 4)
    cv2.putText(img_annotated, str(center[0]) + ', ' + str(center[1]), pt2 ,cv2.FONT_HERSHEY_PLAIN, 3,textcolor, 2)
    cv2.putText(img_annotated,shapename, pt ,cv2.FONT_HERSHEY_PLAIN, 3,textcolor, 2)
    cv2.imshow('Shape', img_annotated)

def processFrame(img):
    if(img is None):
        return

    img = cv2.resize(img, (320, 240))
    cv2.imshow("Original Image",img)
    img_annotated = img.copy()
    hue = [25.0, 55.0]
    sat = [150.0, 255.0]
    val = [40.0, 255.0]
    out = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    out = cv2.inRange(out, (hue[0], sat[0], val[0]),  (hue[1], sat[1], val[1]))
    masked = cv2.bitwise_and(img, img, mask = out)
    img = masked
    # RGB to Gray scale conversion
    img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    
    # Noise removal with iterative bilateral filter(removes noise while preserving edges)
    # noise_removal = cv2.bilateralFilter(img_gray,9,75,75)
    # noise_removal = cv2.bilateralFilter(img_gray,9,75,75)
    # cv2.imshow("Noise Removed Image",noise_removal)
    # # Thresholding the image
    # ret,thresh_image = cv2.threshold(noise_removal,0,255,cv2.THRESH_OTSU)
    # cv2.imshow("Image Thresholding",thresh_image)

    # Applying Canny Edge detection
    #img = cv2.Canny(img,250,255)
    #img = cv2.Canny(img,100,200)
    img = cv2.Canny(img,0,300)
    #canny_image = cv2.Canny(thresh_image,500,255)
    # Creating a Named window to display image
    cv2.imshow("Canny",img)
    img = cv2.convertScaleAbs(img)

    # dilation to strengthen the edges
    kernel = np.ones((3,3), np.uint8)
    # Creating the kernel for dilation
    img = cv2.dilate(img,kernel,iterations=1)
    #cv2.imshow("Dilation", img)
    
    # dilated_image = cv2.medianBlur(dilated_image, 9)
    # cv2.imshow("Blur", dilated_image)

    #cv2.waitKey(0)
    #contours_img, contours, h = cv2.findContours(dilated_image, 1, 2)
    #img, contours, h = cv2.findContours(img, cv2.RETR_EXTERNAL, 2) #seems best, only outside contours
    #cv2.imshow("findContours", img)
    # contours_img, contours, h = cv2.findContours(img, cv2.RETR_LIST, 2) # not good
    contours_img, contours, h = cv2.findContours(img, cv2.RETR_TREE, 2)
    #contours_img, contours, h = cv2.findContours(img, cv2.RETR_CCOMP, 2) #ok
    #import pdb; pdb.set_trace()
    contours= sorted(contours, key = cv2.contourArea, reverse = True)[:1]

    idx=0
    for cnt in contours:
        analyzeContour(img_annotated, cnt, idx)
        idx += 1

cap = cv2.VideoCapture('videos/IMG_3567.MOV')
#cap = cv2.VideoCapture('videos/IMG_3568.MOV')
#cap = cv2.VideoCapture('videos/IMG_3569.MOV')

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if frame is None:
        break;
    processFrame(frame)
    cv2.waitKey(1)

# frame = cv2.imread(r'C:\Users\rbrown\Downloads\2018FIRSTPOWERUP-360PhotosVideos\2018 Field 360-VR Photos and Videos\2018 FIRST Power Up 360 Field Images\Blue Grid 2.JPG')
#frame = cv2.imread(r'pics/CubesStacked.jpg')
# frame = cv2.imread(r'pics/cube_distance.jpg')
# processFrame(frame)

cv2.waitKey()
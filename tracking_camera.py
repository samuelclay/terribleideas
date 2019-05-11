import cv2
import numpy as np

cam = cv2.VideoCapture(0)
mouth_cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')
background_once = False

def show_webcam(cam=None, mirror=True):
    global background_once
    if not cam:
        cam = cv2.VideoCapture(0)
        
    ret_val, img = cam.read()
    if mirror: 
        img = cv2.flip(img, 1)

    img = cv2.resize(img, None, fx=0.5, fy=0.5)
    if not background_once:
        background_once = True
        cv2.imwrite('background.jpg', img)
    
    return img

def find_mouth_rects():
    img = show_webcam(cam)
    
    left_img = img[0:img.shape[1], 0:int(img.shape[0]*.95)]
    cv2.rectangle(img, (0, 0), (int(img.shape[0]*.95), int(img.shape[1]*.95)), (0,0,255), 3)
    right_img = img[0:img.shape[1], int(img.shape[0]):img.shape[0]*2]
    cv2.rectangle(img, (int(img.shape[0]), 0), (img.shape[0]*2, img.shape[1]), (255,0,0), 3)
    
    left_gray = cv2.cvtColor(left_img, cv2.COLOR_BGR2GRAY)
    right_gray = cv2.cvtColor(right_img, cv2.COLOR_BGR2GRAY)
    left_mouth_rects = mouth_cascade.detectMultiScale(left_gray, 1.7, 11)
    right_mouth_rects = mouth_cascade.detectMultiScale(right_gray, 1.7, 11)
    left_smile = []
    right_smile = []
    
    for (x,y,w,h) in left_mouth_rects:
        y = int(y - 0.15*h)
        left_img = img[y:y+h,x:x+w]
        rotated = rotate_bound(left_img, -90)
        cv2.imwrite('left_mouth.jpg', rotated)
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 3)
        
        left_smile = smile_cascade.detectMultiScale(
            left_gray,
            scaleFactor=1.16,
            minNeighbors=35,
            minSize=(25, 25),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        for (x2, y2, w2, h2) in left_smile:
            cv2.rectangle(img, (x2, y2), (x2+w2, y2+h2), (255, 0, 0), 2)
            cv2.putText(img,'Smile',(x,y-7), 3, 1.2, (0, 255, 0), 2, cv2.LINE_AA)
        
        # print(f" ---> Left: {y}")
        break
        
    for (x,y,w,h) in right_mouth_rects:
        y = int(y - 0.15*h)
        rotated = rotate_bound(img[y:y+h,x+int(img.shape[0]):x+int(img.shape[0])+w], 90)
        cv2.imwrite('right_mouth.jpg', rotated)
        cv2.rectangle(img, (x+int(img.shape[0]),y), (x+int(img.shape[0])+w,y+h), (0,255,0), 3)
        
        right_smile = smile_cascade.detectMultiScale(
            right_gray,
            scaleFactor=1.16,
            minNeighbors=35,
            minSize=(25, 25),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        for (x2, y2, w2, h2) in right_smile:
            cv2.rectangle(img, (x2+int(img.shape[0]), y2), (x2+w2+int(img.shape[0]), y2+h2), (255, 0, 0), 2)
            cv2.putText(img,'Smile',(x+int(img.shape[0]),y-7), 3, 1.2, (0, 255, 0), 2, cv2.LINE_AA)
        
        # print(f" ---> Right: {y}")
        break
    
    cv2.imshow('Mouth Detector', img)
    
    return img, left_mouth_rects, right_mouth_rects, left_smile, right_smile
    
def rotate_bound(image, angle):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
 
    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
 
    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
 
    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
 
    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))
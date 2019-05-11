import cv2
import sys
import numpy as np

def show_webcam(cam=None, mirror=False):
    if not cam:
        cam = cv2.VideoCapture(0)
        
    while True:
        ret_val, img = cam.read()
        if mirror: 
            img = cv2.flip(img, 1)
        img = cv2.resize(img, None, fx=0.5, fy=0.5)
        return img
        # cv2.imshow('my webcam', img)
        # if cv2.waitKey(1) == 27:
        #     break  # esc to quit
    # cv2.destroyAllWindows()

def main():
    img = show_webcam()
    # img = cv2.imread('/Users/sclay/Desktop/abe.jpg')
    img = cv2.resize(img, None, fx=0.1, fy=0.1)
    grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier('/usr/local/lib/python3.7/site-packages/cv2/data/haarcascade_frontalface_default.xml')
    detected_faces = face_cascade.detectMultiScale(grayimg)

    bb_top = img.shape[1]
    bb_left = img.shape[0]
    bb_bottom = 0
    bb_right = 0
    for (col, row, width, height) in detected_faces:
        print(" ---> Face: ", col, row, width, height)
        # _ = cv2.rectangle(img, (col, row), (col+width, row+height), (0,255,0), 2)
        if col < bb_left: bb_left = col
        if row < bb_top: bb_top = row
        if col+width > bb_right: bb_right = col+width
        if row+height > bb_bottom: bb_bottom = row+height

    crop_img = img[bb_top:bb_bottom, bb_left:bb_right]
    cv2.imshow('face', crop_img); cv2.waitKey(0); cv2.destroyAllWindows()

def objectTracker():
    major_ver, minor_ver, subminor_ver = cv2.__version__.split('.')
    cam = cv2.VideoCapture(0)
    
    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[1]
    
    if int(major_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        if tracker_type == 'GOTURN':
            tracker = cv2.TrackerGOTURN_create()
        if tracker_type == 'MOSSE':
            tracker = cv2.TrackerMOSSE_create()
        if tracker_type == "CSRT":
            tracker = cv2.TrackerCSRT_create()
            
    while True:
        # Read a new frame
        frame = show_webcam(cam)
         
        # Start timer
        timer = cv2.getTickCount()
 
        # Update tracker
        ok, bbox = tracker.update(frame)
 
        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
 
        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
 
        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
     
        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
 
        # Display result
        cv2.imshow("Tracking", frame)
 
        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27 : break
        
def multiTracker():
    cam = cv2.VideoCapture(0)

    tracker_type = 'multi'
    tracker = cv2.MultiTracker_create()
    init_once = False

    frame = show_webcam(cam)

    bbox1 = cv2.selectROI('tracking', frame)
    bbox2 = cv2.selectROI('tracking', frame)
    # bbox3 = cv2.selectROI('tracking', frame)

    while True:
        # Read a new frame
        frame = show_webcam(cam)
    
        # Start timer
        timer = cv2.getTickCount()
    
        if not init_once:
            ok = tracker.add(cv2.TrackerMIL_create(), frame, bbox1)
            ok = tracker.add(cv2.TrackerMIL_create(), frame, bbox2)
            # ok = tracker.add(cv2.TrackerMIL_create(), frame, bbox3)
            init_once = True
        
        # Update tracker
        ok, boxes = tracker.update(frame)

        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

        # Draw bounding box
        for newbox in boxes:
            p1 = (int(newbox[0]), int(newbox[1]))
            p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
            cv2.rectangle(frame, p1, p2, (200,0,0))

        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
 
        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);

        # Display result
        cv2.imshow("Tracking", frame)

        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27 : break

def mouthTracker():
    mouth_cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')
    cam = cv2.VideoCapture(0)
    if mouth_cascade.empty():
      raise IOError('Unable to load the mouth cascade classifier xml file')

    while True:
        frame = show_webcam(cam)
        # ds_factor = 0.5
        # frame = cv2.resize(frame, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        mouth_rects = mouth_cascade.detectMultiScale(gray, 1.7, 11)
        for (x,y,w,h) in mouth_rects:
            y = int(y - 0.15*h)
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 3)
            break

        cv2.imshow('Mouth Detector', frame)

        c = cv2.waitKey(1)
        if c == 27:
            break

if __name__ == '__main__':
    multiTracker()
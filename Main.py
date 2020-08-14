import os, cv2
import dlib
import imutils
import argparse

import numpy as np

from imutils import face_utils
from _utils import *


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(os.path.join(".","_data","shape_predictor_68_face_landmarks.dat"))

print("[INFO] camera sensor warming up...")


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

Width = int(cap.get(3))
Height = int(cap.get(4))
fps = cap.get(cv2.CAP_PROP_FPS)

"""
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('./save.avi', fourcc ,20.0, (Width,Height))
"""
tingting = TingTing()
objx = 0
objy = 0
counter = 0



while True:

    move = False
    ret, frame = cap.read()
    
    frame = imutils.resize(frame, width=400)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)
    

    for rect in rects:
        move = True
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        (x, y, w, h) = face_utils.rect_to_bb(rect)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        """
        objx = (2 * x + w)//2
        objy = (2 * y + h)//2
        """
        for (x, y) in shape:
            cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
        
        eye = shape[36:48]
        eye_max = np.max(eye, axis=0)
        eye_min = np.min(eye, axis=0)
        objx, objy = np.add(eye_max, eye_min) / 2

    if move:  # For Counter Initialization
        counter = 0
    else:             # If Not See The Face
        counter += 1
    
    if counter > 30: #If Camer can't see Face Over 30 Sec
        move = True # Moving to Center
        objx = tingting.Camera_X//2 #Camera Window Center
        objy = tingting.Camera_Y//2 # Camera Window Center

        cx, cy = tingting.make_object(objx, objy)

        """If counter > 30 and TingTing went to center"""
        if abs(tingting.centerX - cx) <2 and abs(tingting.centerY-cy) < 2:
            counter = 0
            move = False

   
    TingTing_frame = tingting.Make_Face(0, move, objx, objy)
    #out.write(frame) 
    TingTing_frame = cv2.flip(TingTing_frame, 1)
    cv2.imshow("TingTing", TingTing_frame)
    cv2.imshow("TingTing's See", frame)

        
            
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

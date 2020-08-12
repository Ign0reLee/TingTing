import os, cv2
import dlib
import imutils
import argparse

import numpy as np

from imutils import face_utils


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(os.path.join(".","shape_predictor_68_face_landmarks.dat"))

print("[INFO] camera sensor warming up...")

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
#cap.set(cv2.CAP_PROP_FPS, 25)

Width = int(cap.get(3))
print(type(Width), Width)
Height = int(cap.get(4))
print(type(Height), Height) 
fps = cap.get(cv2.CAP_PROP_FPS)
print(fps)


fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('./save.avi', fourcc ,20.0, (Width,Height))



while True:

    ret, frame = cap.read()
    
    frame = imutils.resize(frame, width=400)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)

    for rect in rects:

        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        (x, y, w, h) = face_utils.rect_to_bb(rect)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #cv2.imshow("Frame",frame)

        
        for (x, y) in shape:
            cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

    out.write(frame) 
    cv2.imshow("Frame", frame)
    cv2.resizeWindow("Frame",Width,Height)
        
        
        #key = cv2.waitKey(1) & 0xFF
        
            
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
out.release()
cv2.destroyAllWindows()

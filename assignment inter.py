#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import mediapipe as mp
import numpy as np
import os
from time import sleep
from threading import Thread
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


# In[2]:


def calculate_angle(a,b,c):
    a =np.array(a)
    b =np.array(b)
    c =np.array(c)
    radians =np.arctan2(c[1]-b[1],c[0]-b[0])-np.arctan2(a[1]-b[1],a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    if angle >180:
        angle =360-angle
    return angle    


# In[5]:


cap = cv2.VideoCapture(0)


counter = 0 
i=0.00
stage = "down"



with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        global i
        global h
        ret, frame = cap.read()
        

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      

        results = pose.process(image)
    

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        

        try:
            landmarks = results.pose_landmarks.landmark
            

            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            

            angle = calculate_angle(shoulder, elbow, wrist)
        
            if angle > 170:
                stage = "down"
                i=0
                
            if i>=1 and i<100:
                cv2.putText(image, 'Keep your knee bend ', (100,600), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2, cv2.LINE_AA)
            
            if i==100 and stage=='up':
                cv2.putText(image, 'Now you can lower your leg ', (100,600), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,0), 2, cv2.LINE_AA)
               
            if angle < 140 and stage =='down':
                i+=1
                print(i)
                if i==100:
                    stage="up"
                    counter +=1
                    print(counter)
                       
        except:
            pass
        

        
        cv2.rectangle(image, (0,0), (225,73), (245,117,16), -1)
        

        cv2.putText(image, 'REPS', (15,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter), 
                    (10,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        

        cv2.putText(image, 'Timer', (85,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, str((i/12.5)), 
                    (90,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        

        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                 )               
        
        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


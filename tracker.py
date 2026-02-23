import mediapipe as mp
import cv2
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


class HandTracker:
    def __init__(self):
        self.hands =  mp_hands.Hands(
            static_image_mode = False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        ) 
        

    def process(self,frame):
        frame.flags.writeable = False
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)
        frame.flags.writeable = True

        if not results.multi_hand_landmarks:
            return None
        hand = results.multi_hand_landmarks[0]
        vector = []

        for lm in hand.landmark:
            vector.append(lm.x)
            vector.append(lm.y)
            vector.append(lm.z)
        
        vector = np.array(vector, dtype=np.float32)    
        points = vector.reshape(21,3)

        wrist = points[0]
        points = points - wrist
        distances = np.linalg.norm(points, axis=1)
        max_distance = np.max(distances)
        points = points / max_distance

        normalized_vector = points.flatten()
        #print(normalized_vector)        
        self.draw_landmarks(frame, hand)
        
        return normalized_vector
    
    def draw_landmarks(self, frame, landmarks):
        mp_drawing.draw_landmarks(
            frame,
            landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style()
        )



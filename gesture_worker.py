import cv2
import numpy as np 
from PyQt6.QtCore import QThread, pyqtSignal
from camera import Camera
from tracker import HandTracker
from classifier import GestureClassifier
from action_mapper import ActionMapper
from collections import deque

class GestureWorker(QThread):
    frame_signal = pyqtSignal(np.ndarray)
    gesture_signal = pyqtSignal(int, float)

    def __init__(self):
        super().__init__()

        self.running = True
        self.camera = Camera()
        self.tracker = HandTracker()
        self.classifier = GestureClassifier("gesture_knn.pkl")
        self.actions = ActionMapper()
        self.platform = self.actions.check_platform()
        
    def run(self):
        history = deque(maxlen=10)
        frame_count = 0
        process_rate = 2
        try:
            while self.running:
                frame = self.camera.read()
                frame_count += 1

                if frame is None:
                    continue

                self.frame_signal.emit(frame)
                
                if frame_count % process_rate == 0:

                    landmarks = self.tracker.process(frame)
                    if landmarks is not None:
                        label, confidence = self.classifier.predict_with_probability(landmarks)
                        self.gesture_signal.emit(label,confidence)

                        if confidence >= 0.8:
                            history.append(label)
                            if (len(history) == history.maxlen and len(set(history)) == 1):
                                label = history[0]
                                self.actions.gesture_actions[label]()
                                history.clear()
                        else:
                            print(f"Low confidence: {confidence:.2f}, Ignored")
                        
                if self.camera.should_exit():
                    break

        finally:
            self.camera.release()
    def stop(self):
        self.running = False
        self.quit()
        self.wait()
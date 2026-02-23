import cv2 as cv


# Class encapsulating all camera logic
class Camera:
    def __init__(self):
        self.cap = cv.VideoCapture(0) # Opens the default webcam
        if not self.cap.isOpened():
            raise RuntimeError("Failed to open camera")


    def read(self):
        ret, frame = self.cap.read() # reads a frame from the camera

        if not ret:
            return None
        
        return frame
    
    def show(self, frame):
        cv.imshow('frame', frame) # Displays the frame in a window titled frame

    # Releases the camera hardware
    def release(self):
        self.cap.release()
        cv.destroyAllWindows()

    def should_exit(self):
        key = cv.waitKey(1) & 0xFF # Waits 1 millissecond for a key press
        return key == ord('q') or key == ord('Q') # If the key is q or Q, return True

    

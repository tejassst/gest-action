from camera import Camera
from tracker import HandTracker
from classifier import GestureClassifier
from action_mapper import gesture_actions
from collections import deque
import csv


def main():
    camera = Camera()
    tracker = HandTracker()
    classifier = GestureClassifier("gesture_knn.pkl")
    previous_label = None
    history = deque(maxlen=14)
    frame_count = 0
    process_rate = 2
    try:
        while True:
            frame = camera.read()
            frame_count += 1

            if frame is None:
                break
            if frame_count % process_rate == 0:
                landmarks = tracker.process(frame)
                camera.show(frame)
                
                if landmarks is not None:
                    """
                    # For saving data
                    label = 8

                    with open("data.csv", "a", newline="") as f:
                        writer = csv.writer(f)
                        writer.writerow([label] + landmarks.tolist())
                    """
                    """
                    if label != previous_label:
                        gesture_actions[label]()
                        previous_label = label"""
                    label, confidence = classifier.predict_with_probability(landmarks)
                    print("Predicted gesture: ", label, "Confidence: ", confidence)
                    if confidence >= 0.8:
                        history.append(label)
                        if (len(history) == history.maxlen and len(set(history)) == 1):
                            label = history[0]
                            previous_label = label
                            gesture_actions[label]()
                            history.clear()
                    else:
                        print(f"Low confidence: {confidence:.2f}, Ignored")
                    
            if camera.should_exit():
                break

    finally:
        camera.release()
        
if __name__ == "__main__":
    main()
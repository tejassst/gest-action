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
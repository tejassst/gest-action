# Quick Start Guide

Get up and running with Gest-Action in 5 minutes!

## Prerequisites

- Linux system with Hyprland window manager
- Python 3.11
- Working webcam
- Terminal access

## Installation Steps

### Step 1: Set Up Virtual Environment

```bash
# Navigate to project directory
cd gest-action

# Create virtual environment
python3 -m venv gesture-env

# Activate virtual environment
source gesture-env/bin/activate  # bash/zsh
# OR
source gesture-env/bin/activate.fish  # fish shell
```

### Step 2: Install Dependencies

```bash
pip install opencv-python mediapipe numpy pandas scikit-learn
```

### Step 3: Verify Model File

Check if `gesture_knn.pkl` exists in the project root:

```bash
ls gesture_knn.pkl
```

If it doesn't exist, you'll need to collect training data and train the model (see Step 4).

### Step 4: Run the Application

```bash
python main.py
```

A window should open showing your webcam feed. Try making different hand gestures!

Press **Q** to quit.

## First-Time Setup (No Pre-trained Model)

If you don't have a trained model, follow these steps:

### 1. Enable Data Collection

Edit `main.py` and uncomment the data collection section (around line 30):

```python
# Uncomment these lines:
label = 0  # Start with gesture 0

with open("data.csv", "a", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([label] + landmarks.tolist())
```

### 2. Collect Training Data

For each gesture (0-8):

```bash
# Edit label value in main.py to current gesture ID
# Then run:
python main.py

# Make the gesture repeatedly in front of camera
# Aim for 50-100 samples per gesture
# Move your hand around (different positions, angles, distances)
# Press Q when done

# Repeat for all 9 gestures (labels 0-8)
```

**Gesture Reference:**

- 0: 0 sign (thumb and index touching)
- 1: Index finger pointing up
- 2: Index and middle fingers up (peace sign)
- 3: Three fingers up
- 4: Four fingers up
- 5: All five fingers spread
- 6: Closed fist
- 7: Thumbs up
- 8: Thumbs down

### 3. Verify Data Quality

```bash
python check_data.py
```

You should see approximately equal counts for each label (50-100 each).

### 4. Train the Model

```bash
python train_knn.py
```

This creates `gesture_knn.pkl` and displays the accuracy.

### 5. Run the Application

Comment out the data collection code in `main.py`, then:

```bash
python main.py
```

## Testing Gestures

Once running, try these gestures:

1. **Show 1 finger** → Should switch to workspace 1
2. **Show 2 fingers** → Should switch to workspace 2
3. **Thumbs down** → Should close the active window ⚠️
4. **Closed fist** → Should cycle to the next window

## Troubleshooting

### Camera Not Working

```bash
# Test camera with OpenCV
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK' if cap.isOpened() else 'Camera Failed')"
```

If failed:

- Check camera permissions
- Try different camera index: change `cv.VideoCapture(0)` to `cv.VideoCapture(1)` in `camera.py`

### Hand Not Detected

- Ensure good lighting
- Keep hand centered in frame
- Try moving hand closer/farther from camera
- Check if hand landmarks are visible in the window

### Low Accuracy

- Collect more training data (100+ samples per gesture)
- Use consistent hand orientation during training
- Ensure good lighting during training and use
- Retrain the model

### Hyprland Commands Not Executing

```bash
# Test Hyprland manually
hyprctl dispatch workspace 1

# If this fails, Hyprland is not running properly
```

### Actions Triggering Too Often

In `main.py`, increase stability:

```python
history = deque(maxlen=20)  # Increase from 14 to 20
```

### Actions Not Triggering

In `main.py`, decrease stability:

```python
history = deque(maxlen=10)  # Decrease from 14 to 10
```

Or lower confidence threshold:

```python
if confidence >= 0.7:  # Lower from 0.8 to 0.7
```

## Performance Tips

### Reduce CPU Usage

```python
# In main.py, increase process rate
process_rate = 3  # Process every 3rd frame instead of every 2nd
```

### Improve Responsiveness

```python
# In main.py, decrease process rate
process_rate = 1  # Process every frame
```

### Reduce Latency

```python
# In main.py, reduce history length
history = deque(maxlen=8)  # Respond faster but less stable
```

## Customizing Gestures

### Change an Action

Edit `action_mapper.py`:

```python
gesture_actions = {
    0: lambda: subprocess.run(["hyprctl", "dispatch", "exec", "firefox"]),  # Changed to Firefox
    # ... rest of gestures
}
```

### Add a New Gesture

1. Decide on a new gesture ID (e.g., 9)
2. Collect training data with label=9
3. Retrain the model
4. Add to `action_mapper.py`:

```python
gesture_actions = {
    # ... existing gestures ...
    9: lambda: subprocess.run(["your", "command", "here"]),
}
```

## Safety Tips

⚠️ **Warning**: Gesture 8 (thumbs down) closes windows! Be careful when testing.

**Recommended Testing Order:**

1. Test workspace switching first (gestures 1, 2, 3)
2. Test window movement (gestures 4, 5, 6)
3. Test terminal launch (gesture 0)
4. Test window close last (gesture 8) with a disposable window

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for technical details
- Customize gestures in `action_mapper.py`
- Experiment with different hand positions and lighting
- Fine-tune confidence and stability parameters

## Getting Help

Common issues and solutions:

| Issue                | Solution                                              |
| -------------------- | ----------------------------------------------------- |
| ImportError          | Install missing package: `pip install <package-name>` |
| Camera error         | Check permissions, close other camera apps            |
| No hand detected     | Improve lighting, center hand in frame                |
| Low accuracy         | Collect more diverse training data                    |
| Commands not working | Verify Hyprland is running                            |

## Useful Commands

```bash
# Activate environment
source gesture-env/bin/activate

# Deactivate environment
deactivate

# Check installed packages
pip list

# Update a package
pip install --upgrade <package-name>

# Remove virtual environment
deactivate
rm -rf gesture-env
```

## Quick Reference Card

Print this and keep it handy:

```
┌─────────────────────────────────────────┐
│      GEST-ACTION GESTURE REFERENCE      │
├──────────────┬──────────────────────────┤
│ Gesture      │ Action                   │
├──────────────┼──────────────────────────┤
│ 0 Sign       │ Launch Terminal          │
│ 1 Finger     │ Workspace 1              │
│ 2 Fingers    │ Workspace 2              │
│ 3 Fingers    │ Workspace 3              │
│ 4 Fingers    │ Move Window Next         │
│ 5 Fingers    │ Move Window Prev         │
│ Fist         │ Cycle Window             │
│ Thumbs Up    │ Open Image               │
│ Thumbs Down  │ Close Window ⚠️          │
├──────────────┴──────────────────────────┤
│ Press Q to Quit                         │
└─────────────────────────────────────────┘
```

---

Happy gesture controlling! 🖐️

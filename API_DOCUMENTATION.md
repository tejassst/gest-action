# API Documentation

## Table of Contents
- [Camera Module](#camera-module)
- [HandTracker Module](#handtracker-module)
- [GestureClassifier Module](#gestureclassifier-module)
- [Action Mapper Module](#action-mapper-module)
- [Training Utilities](#training-utilities)

---

## Camera Module

**File**: `camera.py`

### Class: `Camera`

Encapsulates all camera-related operations using OpenCV.

#### Constructor

```python
Camera()
```

Initializes the camera object and opens the default webcam (device index 0).

**Raises**:
- `RuntimeError`: If the camera fails to open

**Example**:
```python
camera = Camera()
```

#### Methods

##### `read()`

Captures a single frame from the webcam.

**Returns**:
- `numpy.ndarray`: The captured frame in BGR format
- `None`: If frame capture fails

**Example**:
```python
frame = camera.read()
if frame is not None:
    # Process frame
```

##### `show(frame)`

Displays the given frame in a window titled "frame".

**Parameters**:
- `frame` (numpy.ndarray): The frame to display

**Example**:
```python
camera.show(frame)
```

##### `release()`

Releases the camera hardware and closes all OpenCV windows.

**Example**:
```python
camera.release()
```

##### `should_exit()`

Checks if the user has pressed 'Q' or 'q' to exit.

**Returns**:
- `bool`: True if exit key was pressed, False otherwise

**Implementation Details**:
- Waits 1 millisecond for key press
- Checks for 'Q' or 'q' key

**Example**:
```python
if camera.should_exit():
    break
```

---

## HandTracker Module

**File**: `tracker.py`

### Class: `HandTracker`

Uses MediaPipe to detect and track hand landmarks in video frames.

#### Constructor

```python
HandTracker()
```

Initializes the MediaPipe Hands solution with optimized parameters.

**Configuration**:
- `static_image_mode`: False (for video streaming)
- `max_num_hands`: 1 (processes only one hand)
- `min_detection_confidence`: 0.7
- `min_tracking_confidence`: 0.7

**Example**:
```python
tracker = HandTracker()
```

#### Methods

##### `process(frame)`

Processes a video frame to detect and extract normalized hand landmarks.

**Parameters**:
- `frame` (numpy.ndarray): Input frame in BGR format

**Returns**:
- `numpy.ndarray`: Normalized 63-dimensional feature vector (21 landmarks × 3 coordinates)
- `None`: If no hand is detected

**Processing Pipeline**:
1. Convert BGR to RGB
2. Detect hand landmarks using MediaPipe
3. Extract 21 landmarks (x, y, z coordinates)
4. Normalize landmarks:
   - Translate relative to wrist (landmark 0)
   - Scale by maximum distance from wrist
5. Flatten to 1D vector
6. Draw landmarks on frame

**Feature Vector Details**:
- **Raw**: 21 landmarks × 3 coordinates = 63 dimensions
- **Normalized**: Translation and scale invariant
- **Format**: `[x0, y0, z0, x1, y1, z1, ..., x20, y20, z20]`

**Example**:
```python
landmarks = tracker.process(frame)
if landmarks is not None:
    print(f"Feature vector shape: {landmarks.shape}")  # (63,)
```

##### `draw_landmarks(frame, landmarks)`

Draws hand landmarks and connections on the frame.

**Parameters**:
- `frame` (numpy.ndarray): Frame to draw on (modified in-place)
- `landmarks`: MediaPipe hand landmarks object

**Visualization**:
- Draws 21 landmark points
- Draws connections between landmarks
- Uses default MediaPipe styling

**Example**:
```python
# Called internally by process()
self.draw_landmarks(frame, hand)
```

---

## GestureClassifier Module

**File**: `classifier.py`

### Class: `GestureClassifier`

Loads and uses a trained KNN model for gesture classification.

#### Constructor

```python
GestureClassifier(model_file: str)
```

Loads a pre-trained KNN model from a pickle file.

**Parameters**:
- `model_file` (str): Path to the pickle file containing the trained model

**Example**:
```python
classifier = GestureClassifier("gesture_knn.pkl")
```

#### Methods

##### `predict(vector)`

Predicts the gesture class for a given feature vector.

**Parameters**:
- `vector` (numpy.ndarray): 63-dimensional feature vector from HandTracker

**Returns**:
- `int`: Predicted gesture label (0-8)

**Example**:
```python
label = classifier.predict(landmarks)
print(f"Gesture: {label}")
```

##### `predict_with_probability(vector)`

Predicts the gesture class along with confidence score.

**Parameters**:
- `vector` (numpy.ndarray): 63-dimensional feature vector

**Returns**:
- `tuple`: (predicted_label, confidence)
  - `predicted_label` (int): Predicted gesture label (0-8)
  - `confidence` (float): Confidence score (0.0-1.0)

**Implementation**:
- Uses `predict_proba()` from KNN model
- Returns the class with highest probability
- Confidence = probability of predicted class

**Example**:
```python
label, confidence = classifier.predict_with_probability(landmarks)
if confidence >= 0.8:
    print(f"High confidence: {label} ({confidence:.2%})")
else:
    print(f"Low confidence, ignored")
```

---

## Action Mapper Module

**File**: `action_mapper.py`

### Data Structure: `gesture_actions`

A dictionary mapping gesture labels to OS commands.

**Type**: `Dict[int, Callable]`

**Structure**:
```python
gesture_actions = {
    gesture_id: lambda: subprocess.run([command, args...]),
    ...
}
```

### Gesture Mapping

| Gesture ID | Gesture Name | Command | Description |
|------------|--------------|---------|-------------|
| 0 | 0 Sign | `hyprctl dispatch exec kitty` | Launch Kitty terminal |
| 1 | 1 Finger | `hyprctl dispatch workspace 1` | Switch to workspace 1 |
| 2 | 2 Fingers | `hyprctl dispatch workspace 2` | Switch to workspace 2 |
| 3 | 3 Fingers | `hyprctl dispatch workspace 3` | Switch to workspace 3 |
| 4 | 4 Fingers | `hyprctl dispatch movetoworkspace +1` | Move window to next workspace |
| 5 | 5 Fingers | `hyprctl dispatch movetoworkspace -1` | Move window to previous workspace |
| 6 | Fist | `hyprctl dispatch cyclenext` | Cycle to next window |
| 7 | Thumbs Up | `hyprctl dispatch exec gthumb -f ~/Documents/heisenberg.gif` | Open image viewer |
| 8 | Thumbs Down | `hyprctl dispatch killactive` | Close active window |

### Usage

```python
from action_mapper import gesture_actions

# Execute action for gesture 1
gesture_actions[1]()
```

### Customization

To add or modify gesture actions:

```python
gesture_actions = {
    0: lambda: subprocess.run(["your-command", "arg1", "arg2"]),
    1: lambda: subprocess.run(["another-command"]),
    # Add more mappings...
}
```

**Note**: All commands use `subprocess.run()` which blocks until completion.

---

## Training Utilities

### Script: `train_knn.py`

Trains a K-Nearest Neighbors classifier on collected gesture data.

#### Workflow

1. **Load Data**: Reads `data.csv` containing labeled feature vectors
2. **Split Data**: 80% training, 20% testing (random_state=42)
3. **Train Model**: KNN with k=5 neighbors
4. **Evaluate**: Computes accuracy on test set
5. **Save Model**: Exports to `gesture_knn.pkl`

#### Data Format

**Input**: `data.csv`
- Column 0: Label (0-8)
- Columns 1-63: Feature vector

#### Model Configuration

```python
KNeighborsClassifier(n_neighbors=5)
```

- **Algorithm**: K-Nearest Neighbors
- **K value**: 5 (considers 5 closest training samples)
- **Voting**: Majority vote among neighbors

#### Usage

```bash
python train_knn.py
```

#### Output

- Prints model accuracy
- Saves model to `gesture_knn.pkl`

---

### Script: `check_data.py`

Validates the training data and displays statistics.

#### Features

- Shows dataset shape (rows × columns)
- Displays label distribution (count per gesture)
- Helps identify data imbalance

#### Usage

```bash
python check_data.py
```

#### Example Output

```
Shape:  (500, 64)

Label counts:
0    60
1    55
2    58
3    52
4    49
5    51
6    54
7    56
8    65
Name: label, dtype: int64
```

---

## Main Application

**File**: `main.py`

### Function: `main()`

Orchestrates the entire gesture recognition pipeline.

#### Components

1. **Initialization**
   - Creates Camera, HandTracker, and GestureClassifier instances
   - Initializes history buffer (deque with maxlen=14)
   - Sets processing rate (every 2nd frame)

2. **Main Loop**
   - Captures frames from camera
   - Processes frames at specified rate
   - Detects hand landmarks
   - Classifies gestures with confidence
   - Executes actions based on stable predictions

3. **Stability Mechanism**
   - Requires 14 consecutive identical predictions
   - Prevents false triggers from transitional gestures
   - Clears history after action execution

4. **Confidence Filtering**
   - Only accepts predictions with ≥80% confidence
   - Logs and ignores low-confidence predictions

#### Configuration Variables

```python
process_rate = 2        # Process every Nth frame
confidence_threshold = 0.8  # Minimum confidence
history_length = 14     # Consecutive predictions needed
```

#### Data Collection Mode

Uncomment this section to collect training data:

```python
label = 0  # Set to gesture ID

with open("data.csv", "a", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([label] + landmarks.tolist())
```

#### Error Handling

- Uses try-finally to ensure camera release
- Handles frame capture failures gracefully
- Checks for 'Q' key to exit

#### Usage

```bash
python main.py
```

---

## Data Flow Diagram

```
┌─────────┐
│ Camera  │
│  read() │
└────┬────┘
     │ frame (BGR)
     ▼
┌─────────────┐
│ HandTracker │
│  process()  │
└──────┬──────┘
       │ landmarks (63D vector)
       ▼
┌──────────────────┐
│GestureClassifier │
│predict_with_prob()│
└────────┬─────────┘
         │ (label, confidence)
         ▼
┌─────────────────┐
│ Confidence ≥0.8 │
│   History Check │
└────────┬────────┘
         │ stable label
         ▼
┌──────────────┐
│ActionMapper  │
│gesture_actions│
└──────┬───────┘
       │
       ▼
┌────────────┐
│ OS Command │
└────────────┘
```

---

## Type Definitions

### Feature Vector

```python
Type: numpy.ndarray
Shape: (63,)
Dtype: float32
Range: Normalized [-1.0, 1.0]
```

### Gesture Labels

```python
Type: int
Range: 0-8
Labels: {0: "0_sign", 1: "1_finger", 2: "2_fingers", 
         3: "3_fingers", 4: "4_fingers", 5: "5_fingers",
         6: "fist", 7: "thumbs_up", 8: "thumbs_down"}
```

### Confidence Score

```python
Type: float
Range: [0.0, 1.0]
Threshold: 0.8
```

---

## Performance Considerations

### Computational Complexity

- **Hand Detection**: O(1) per frame (MediaPipe optimized)
- **KNN Classification**: O(k × n × d) where k=5, n=training samples, d=63
- **Frame Processing**: ~30-60ms per frame (hardware dependent)

### Memory Usage

- **Model**: ~10-50 KB (depends on training data size)
- **Frame Buffer**: ~1.5 MB per frame (640×480×3)
- **History Buffer**: ~3.5 KB (14 × 63 × 4 bytes)

### Optimization Tips

1. **Reduce frame processing rate**: Increase `process_rate`
2. **Lower camera resolution**: Modify `cv.VideoCapture()` settings
3. **Reduce history length**: Faster response but less stable
4. **Use compiled code**: Consider Cython for critical sections

---

## Error Codes and Exceptions

### Camera Module

- `RuntimeError`: Camera failed to open
  - **Solution**: Check camera permissions, ensure no other app is using camera

### HandTracker Module

- Returns `None`: No hand detected
  - **Normal behavior**: Continue to next frame

### Classifier Module

- `FileNotFoundError`: Model file not found
  - **Solution**: Train model using `train_knn.py`

- `pickle.UnpicklingError`: Corrupted model file
  - **Solution**: Retrain and save model

---

## Dependencies Version Matrix

| Package | Minimum Version | Tested Version |
|---------|----------------|----------------|
| Python | 3.11 | 3.11 |
| opencv-python | 4.5.0 | 4.13.0 |
| mediapipe | 0.10.0 | 0.10.14 |
| numpy | 1.20.0 | 2.4.2 |
| pandas | 1.3.0 | 3.0.0 |
| scikit-learn | 0.24.0 | 1.5.3 |

---

## License

[Add your license here]

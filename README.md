# Gest-Action

A real-time hand gesture recognition system that maps hand gestures to OS-level actions on Linux (Hyprland window manager). The system uses computer vision and machine learning to detect hand landmarks and classify gestures, enabling hands-free control of your desktop environment.

## 🎯 Features

- **Real-time Hand Tracking**: Uses MediaPipe for accurate hand landmark detection
- **Gesture Recognition**: KNN-based machine learning classifier for gesture identification
- **OS Integration**: Direct control of Hyprland window manager operations
- **High Accuracy**: Confidence-based filtering ensures reliable gesture detection
- **Stability**: History-based confirmation prevents false triggers
- **Low Latency**: Optimized processing with adjustable frame rates

## 🏗️ System Architecture

```
Camera → Hand Tracker → Gesture Classifier → Action Mapper → OS Command
   ↓           ↓               ↓                    ↓              ↓
 OpenCV   MediaPipe      KNN Model          Lambda Functions   Hyprctl
```

### Component Overview

1. **Camera Module** (`camera.py`): Handles webcam input/output using OpenCV
2. **Hand Tracker** (`tracker.py`): Detects and normalizes hand landmarks using MediaPipe
3. **Gesture Classifier** (`classifier.py`): Predicts gestures using trained KNN model
4. **Action Mapper** (`action_mapper.py`): Maps gestures to system commands
5. **Main Controller** (`main.py`): Orchestrates the entire pipeline

## 📋 Requirements

### System Requirements
- Linux with Hyprland window manager
- Webcam
- Python 3.11

### Python Dependencies
- opencv-python (cv2)
- mediapipe
- numpy
- pandas
- scikit-learn
- pickle (built-in)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd gest-action
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv gesture-env
   source gesture-env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install opencv-python mediapipe numpy pandas scikit-learn
   ```

4. **Ensure you have a trained model**
   - The project requires `gesture_knn.pkl` (trained KNN model)
   - If not present, you'll need to collect training data and train the model (see Training section)

## 🎮 Usage

### Running the Application

```bash
python main.py
```

- The application will open a window showing the camera feed with hand landmarks
- Perform gestures in front of the camera
- Press 'Q' to quit the application

### Recognized Gestures

| Gesture | ID | Action |
|---------|----|----|
| 0 Sign | 0 | Launch Kitty terminal |
| 1 Finger Up | 1 | Switch to workspace 1 |
| 2 Fingers Up | 2 | Switch to workspace 2 |
| 3 Fingers Up | 3 | Switch to workspace 3 |
| 4 Fingers Up | 4 | Move window to next workspace |
| 5 Fingers Up | 5 | Move window to previous workspace |
| Fist | 6 | Cycle to next window |
| Thumbs Up | 7 | Open image in Gthumb |
| Thumbs Down | 8 | Close active window |

## 🎓 Training the Model

### 1. Collect Training Data

Modify `main.py` to enable data collection:

```python
# Uncomment this section in main.py
label = 0  # Set to gesture ID you're collecting

with open("data.csv", "a", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([label] + landmarks.tolist())
```

Run the application and perform the gesture multiple times to collect diverse samples.

### 2. Check Data Quality

```bash
python check_data.py
```

This displays the shape of your dataset and count of samples per label.

### 3. Train the Model

```bash
python train_knn.py
```

This will:
- Load training data from `data.csv`
- Split into training (80%) and testing (20%) sets
- Train a KNN classifier with k=5
- Save the model to `gesture_knn.pkl`
- Print accuracy on test set

## 📁 Project Structure

```
gest-action/
├── main.py                 # Main application entry point
├── camera.py              # Camera interface wrapper
├── tracker.py             # Hand tracking and landmark extraction
├── classifier.py          # Gesture classification
├── action_mapper.py       # Gesture-to-action mapping
├── train_knn.py          # Model training script
├── check_data.py         # Data validation utility
├── data.csv              # Training data (landmarks + labels)
├── gesture_knn.pkl       # Trained KNN model
├── config.yaml           # Configuration file (unused)
├── NOTES.md              # Development notes
├── actions/              # Platform-specific action modules
│   ├── linux.py         # Linux-specific actions (empty)
│   └── mac.py           # macOS-specific actions (empty)
├── models/              # Model storage
│   └── gesture_model.tflite
└── gesture-env/         # Virtual environment
```

## 🔧 Technical Details

### Hand Landmark Processing

1. **Detection**: MediaPipe detects 21 hand landmarks in 3D space (x, y, z)
2. **Normalization**: 
   - Translate all points relative to wrist (landmark 0)
   - Scale by maximum distance from wrist
   - Creates a 63-dimensional feature vector (21 landmarks × 3 coordinates)
3. **Benefits**: Translation and scale invariant, works regardless of hand position/size

### Gesture Classification

- **Algorithm**: K-Nearest Neighbors (k=5)
- **Confidence Threshold**: 0.8 (80%)
- **Stability Check**: Requires 14 consecutive consistent predictions
- **False Positive Prevention**: Low confidence predictions are ignored

### Performance Optimization

- **Frame Processing Rate**: Every 2nd frame (configurable via `process_rate`)
- **Single Hand Mode**: Processes only one hand for efficiency
- **Minimum Confidence**: Detection confidence = 0.7, Tracking confidence = 0.7

## 🎛️ Configuration

### Adjusting Sensitivity

In `main.py`, modify these parameters:

```python
# Confidence threshold for gesture acceptance
if confidence >= 0.8:  # Lower for more sensitivity, higher for more accuracy

# History window size (consecutive predictions needed)
history = deque(maxlen=14)  # Lower for faster response, higher for stability

# Frame processing rate
process_rate = 2  # Process every Nth frame (lower = faster, higher CPU)
```

### Customizing Actions

Edit `action_mapper.py` to customize gesture actions:

```python
gesture_actions = {
    0: lambda: subprocess.run(["your", "command", "here"]),
    # Add more gesture mappings...
}
```

## 🐛 Troubleshooting

### Camera Not Opening
- Check if camera is being used by another application
- Verify camera permissions
- Try changing camera index in `camera.py`: `cv.VideoCapture(1)` or `cv.VideoCapture(2)`

### Low Accuracy
- Collect more training data for problematic gestures
- Ensure consistent hand positioning during training
- Check lighting conditions (bright, even lighting works best)
- Retrain model with higher quality data

### Hyprland Commands Not Working
- Ensure Hyprland is running
- Test commands manually: `hyprctl dispatch workspace 1`
- Check Hyprland configuration

### High CPU Usage
- Increase `process_rate` in `main.py`
- Reduce camera resolution in `camera.py`

## 🔮 Future Improvements

- [ ] Support for multiple window managers (X11, Wayland)
- [ ] Configuration file support for custom gesture mappings
- [ ] GUI for easy gesture-action binding
- [ ] Support for two-handed gestures
- [ ] Dynamic gesture recognition (motion-based)
- [ ] TensorFlow Lite model integration (`gesture_model.tflite`)
- [ ] Cross-platform support (Linux, macOS, Windows)

## 📝 Development Notes

See `NOTES.md` for detailed development journey and experiences, including:
- Environment setup challenges
- MediaPipe API migration issues
- Gesture design decisions

## 📄 License

[Add your license here]

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 👏 Acknowledgments

- **MediaPipe**: Google's hand tracking solution
- **OpenCV**: Computer vision library
- **scikit-learn**: Machine learning framework
- **Hyprland**: Tiling Wayland compositor

## 📧 Contact

[Add your contact information here]

---

**Note**: This project is designed for Hyprland on Linux. For other window managers or operating systems, you'll need to modify the commands in `action_mapper.py` accordingly.

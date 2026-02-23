# Gest-Action

## System archictecture

- Camera → Landmark Detection → Gesture Classifier → Action Mapper → OS Command

# Experiences

1. Made a venv and installed dependency
2. Could not install tensorflow because I was using Python 3.14 system-wide
3. Updated core system
4. Wrote the camera class with openCV
5. Implemented it in main.py
6. While implementing tracker class ran into problem
   - mediapipe new version has a new API structure so certain attributes did not exist.
   - So I switched to an older version because I am learning too.
7. Tracker works
8. Now I am converting 21 landmarks which has 3 (x,y,z) points into a 63 dimensional vector for ML
9. Great! The vector length is 63
10. Gestures-
    - 0: 0 sign
    - 1: 1 finger up
    - 2: 2 finger up
    - 3: 3 finger up
    - 4: 4 finger up
    - 5: 5 finger up
    - 6: fist up
    - 7: Thumbs up
    - 8: Thumbs down

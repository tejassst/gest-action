import sys
import cv2
import warnings
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QProgressBar,
    QPushButton,
    QMessageBox
)
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt

from gesture_worker import GestureWorker

warnings.filterwarnings("ignore", category=UserWarning, module="google.protobuf")
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gest-Action")
        self.resize(900, 700)

        # Camera Preview
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Platform Label
        self.platform_label  = QLabel()
        self.platform_label.setAlignment(Qt.AlignmentFlag.AlignLeft)


        # Gesture Label
        self.gesture_label = QLabel("Gesture: None")
        self.gesture_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Confidence Bar
        self.confidence_bar = QProgressBar()
        self.confidence_bar.setRange(0, 100)

        # Start/Stop Button
        self.toggle_button = QPushButton("Stop")
        self.toggle_button.clicked.connect(self.toggle_worker)
        
        self.min_bttn = QPushButton("Minimize")
        self.min_bttn.clicked.connect(self.showMinimized)
        # Layout 
        layout = QVBoxLayout()
        layout.addWidget(self.min_bttn)
        layout.addWidget(self.video_label)
        layout.addWidget(self.platform_label)
        layout.addWidget(self.gesture_label)
        layout.addWidget(self.confidence_bar)
        layout.addWidget(self.toggle_button)
        self.setLayout(layout)

        # Start Worker thread
        self.worker = GestureWorker()

        self.worker.frame_signal.connect(self.update_frame)
        self.worker.gesture_signal.connect(self.update_gesture)
        self.worker.error_signal.connect(self.handle_error)
        self.worker.start()
        self.platform_label.setText(self.worker.platform)

    def toggle_worker(self):
        if self.worker.isRunning():
            self.worker.stop()
            self.toggle_button.setText("Start")
        else:
            self.worker = GestureWorker()
            self.worker.frame_signal.connect(self.update_frame)
            self.worker.gesture_signal.connect(self.update_gesture)
            self.worker.error_signal.connect(self.handle_error)
            self.worker.start()
            self.toggle_button.setText("Stop")

    def handle_error(self, message):
        self.gesture_label.setText("Camera unavailable")
        self.confidence_bar.setValue(0)
        self.toggle_button.setText("Start")
        QMessageBox.critical(self, "Camera Error", message)

    def update_frame(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        h, w, ch = rgb.shape
        bytes_per_line = ch * w

        qt_image = QImage(
            rgb.data,
            w,
            h,
            bytes_per_line,
            QImage.Format.Format_RGB888
        )
        pixmap = QPixmap.fromImage(qt_image)
        self.video_label.setPixmap(pixmap)

    def update_gesture(self, label, confidence):
        self.gesture_label.setText(f"Gesture: {label}")
        percent = int(confidence * 100)
        self.confidence_bar.setValue(percent)

    def closeEvent(self, event):
        self.worker.stop()
        event.accept()

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

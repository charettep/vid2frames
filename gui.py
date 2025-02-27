import os
import cv2 # type: ignore
import threading
import subprocess
from PyQt6.QtWidgets import ( # type: ignore
    QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QLabel, QSpinBox, QLineEdit, QHBoxLayout, QProgressBar
)
import logging
from extractor import extract_frames

class FrameExtractorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.output_subfolder = None  # Initialize output_subfolder

    def initUI(self):
        self.setWindowTitle("Video Frame Extractor")
        self.setGeometry(200, 200, 500, 350)
        layout = QVBoxLayout()

        # File Selection
        self.label = QLabel("Select Video File:")
        self.video_path_display = QLineEdit()
        self.video_path_display.setReadOnly(True)
        self.select_button = QPushButton("Browse")
        self.select_button.clicked.connect(self.browse_file)

        file_layout = QHBoxLayout()
        file_layout.addWidget(self.video_path_display)
        file_layout.addWidget(self.select_button)

        # Video Specs Display
        self.specs_label = QLabel("Video Specs: N/A")

        # Frame Extraction Settings
        self.interval_label = QLabel("Extract 1 frame every X seconds:")
        self.interval_input = QSpinBox()
        self.interval_input.setRange(1, 60)
        self.interval_input.setValue(1)

        self.output_label = QLabel("Output Resolution (Width x Height):")
        self.output_width = QSpinBox()
        self.output_width.setRange(100, 1920)
        self.output_width.setValue(640)
        self.output_height = QSpinBox()
        self.output_height.setRange(100, 1080)
        self.output_height.setValue(480)

        res_layout = QHBoxLayout()
        res_layout.addWidget(self.output_width)
        res_layout.addWidget(self.output_height)

        # Output Directory
        self.output_dir_label = QLabel("Save Extracted Frames To:")
        self.output_dir_display = QLineEdit()
        self.output_dir_display.setReadOnly(True)
        self.output_dir_button = QPushButton("Select Folder")
        self.output_dir_button.clicked.connect(self.browse_output_folder)

        output_layout = QHBoxLayout()
        output_layout.addWidget(self.output_dir_display)
        output_layout.addWidget(self.output_dir_button)

        # Start Extraction Button
        self.extract_button = QPushButton("Extract Frames")
        self.extract_button.clicked.connect(self.start_extraction)

        # Open Output Folder Button
        self.open_output_button = QPushButton("Open Output Folder")
        self.open_output_button.clicked.connect(self.open_output_folder)
        self.open_output_button.setEnabled(False)

        # Progress Bar
        self.progress = QProgressBar()
        self.progress.setValue(0)

        # Status Display
        self.status_label = QLabel("Status: Waiting...")

        # Layout Organization
        layout.addWidget(self.label)
        layout.addLayout(file_layout)
        layout.addWidget(self.specs_label)
        layout.addWidget(self.interval_label)
        layout.addWidget(self.interval_input)
        layout.addWidget(self.output_label)
        layout.addLayout(res_layout)
        layout.addWidget(self.output_dir_label)
        layout.addLayout(output_layout)
        layout.addWidget(self.extract_button)
        layout.addWidget(self.open_output_button)
        layout.addWidget(self.progress)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Video File", "", "Video Files (*.mp4 *.avi *.mov)"
        )
        if file_name:
            self.video_path_display.setText(file_name)
            # Load video and extract specs
            cap = cv2.VideoCapture(file_name)
            if cap.isOpened():
                fps = cap.get(cv2.CAP_PROP_FPS)
                frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                duration = frame_count / fps if fps != 0 else 0
                file_ext = os.path.splitext(file_name)[1][1:].upper()
                specs = f"Format: {file_ext}, FPS: {fps:.2f}, Resolution: {width}x{height}, Duration: {duration:.2f} sec"
                print(specs)
                logging.info("Video specs: " + specs)
                # Pre-populate resolution fields
                self.output_width.setValue(width)
                self.output_height.setValue(height)
                # Display specs in GUI
                self.specs_label.setText("Video Specs: " + specs)
                cap.release()
            else:
                self.status_label.setText("Error: Unable to open video file.")
                logging.error("Could not open video file: %s", file_name)

    def browse_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_dir_display.setText(folder)

    def start_extraction(self):
        video_path = self.video_path_display.text()
        output_folder = self.output_dir_display.text()
        interval = self.interval_input.value()
        width = self.output_width.value()
        height = self.output_height.value()

        if not video_path or not output_folder:
            self.status_label.setText("Error: Select video and output folder")
            logging.error("Video path or output folder not selected.")
            return

        # Create a new folder named like the video file (without extension)
        video_basename = os.path.splitext(os.path.basename(video_path))[0]
        self.output_subfolder = os.path.join(output_folder, video_basename)
        if not os.path.exists(self.output_subfolder):
            os.makedirs(self.output_subfolder)
            logging.info("Created output folder: %s", self.output_subfolder)

        self.status_label.setText("Processing...")
        self.open_output_button.setEnabled(False)
        threading.Thread(
            target=extract_frames, 
            args=(
                video_path, self.output_subfolder, interval, width, height,
                self.update_progress, self.update_status
            ),
            daemon=True
        ).start()

    def update_progress(self, value):
        self.progress.setValue(value)

    def update_status(self, message):
        self.status_label.setText(message)
        if "Complete" in message:
            self.open_output_button.setEnabled(True)

    def open_output_folder(self):
        if self.output_subfolder:
            if os.name == 'nt':
                os.startfile(self.output_subfolder)
            else:
                subprocess.Popen(['xdg-open', self.output_subfolder])
# vid2frames

vid2frames is a desktop utility for extracting evenly spaced frames from a video file through a user-friendly PyQt interface. It is designed for creators and researchers who need quick snapshots from videos without writing code.

## Features
- Browse for a video and automatically display its format, resolution, FPS, and duration.
- Configure extraction cadence by choosing how often (in seconds) to capture a frame.
- Resize exported frames to a target width and height before saving.
- Choose the destination folder and open it directly from the app once processing finishes.
- Monitor progress in real time with a status message and progress bar.

## Prerequisites
- **Python:** 3.9 or newer is recommended.
- **Dependencies:** PyQt6 and OpenCV (installed automatically via the provided requirements file).
- A desktop environment capable of running PyQt6 applications (Windows, macOS, or Linux with an X11/Wayland display server).

## Installation
1. Clone or download this repository.
2. (Optional) Create and activate a virtual environment.
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Launching the Application
Run the GUI from the project root:
```bash
python app.py
```
The window allows you to select a video file, adjust extraction settings, and start saving frames.

## Platform Notes & Limitations
- **Requirements:** The GUI depends on PyQt6, and frame extraction requires OpenCV (opencv-python). GPU acceleration is not used.
- **Supported formats:** The file picker filters to `.mp4`, `.avi`, and `.mov` files. Other formats may work if OpenCV can decode them, but they are not officially supported.
- **Output location:** Frames are saved as `.jpg` images inside a subfolder named after the video file within the selected output directory.
- **Environment:** Running the app over remote connections may require X forwarding or similar display solutions.

## Future Roadmap
- Add configurable output image formats (e.g., PNG, WebP).
- Support batch processing of multiple videos.
- Allow command-line usage alongside the GUI for headless workflows.

import os
import cv2
import logging
from datetime import datetime

def extract_frames(video_path, output_folder, interval, width, height, update_progress, update_status):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        update_status("Error: Unable to open video")
        logging.error("Could not open video file: %s", video_path)
        return
    
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_interval = fps * interval
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    extracted = 0

    logging.info("Starting frame extraction...")

    for frame_num in range(0, frame_count, frame_interval):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (width, height))
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        frame_filename = f"frame_{timestamp}_{frame_num}.jpg"
        frame_path = os.path.join(output_folder, frame_filename)
        cv2.imwrite(frame_path, frame)
        extracted += 1

        progress = int((frame_num / frame_count) * 100)
        update_progress(progress)
        logging.info("Extracted frame: %s", frame_filename)

    cap.release()
    update_status(f"Extraction Complete: {extracted} frames saved.")
    update_progress(100)
    logging.info("Frame extraction completed. Total frames saved: %d", extracted)
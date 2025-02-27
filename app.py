import sys
import logging
from PyQt6.QtWidgets import QApplication # type: ignore
from gui import FrameExtractorApp

logging.basicConfig(filename="frame_extractor.log", level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FrameExtractorApp()
    window.show()
    sys.exit(app.exec())
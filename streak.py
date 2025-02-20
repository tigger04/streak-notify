#!/usr/bin/env python3
"""
This script reads text from STDIN and displays it on a transparent window.
The window fades out after a configurable time and closes after the fade animation completes.
"""

# Display configuration
DISPLAY_TIME_MS = 1000  # How long to show the text (milliseconds)
FADE_IN_TIME_MS = 500  # Fade in duration (milliseconds)
FADE_OUT_TIME_MS = 500  # Fade out duration (milliseconds)

# Appearance configuration
FONT_FAMILY = "Tequila"
FONT_SIZE = 28
BACKGROUND_COLOR = "rgba(0, 0, 255, 0.5)"  # Black with 70% opacity
TEXT_COLOR = "rgba(190, 190, 190)"
PADDING_PX = 20
CORNER_RADIUS_PX = 15 # Rounded corner radius

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation
from PyQt5.QtGui import QFont


class FadingWindow(QMainWindow):
    def __init__(self, text):
        super().__init__()

        # Remove window frame and make it stay on top
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        # Make the window background transparent
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Create and style the label
        self.label = QLabel(text, self)
        self.label.setStyleSheet(
            f"""
            QLabel {{
                color: {TEXT_COLOR};
                background-color: {BACKGROUND_COLOR};
                padding: {PADDING_PX}px;
                border-radius: {CORNER_RADIUS_PX}px;
            }}
        """
        )
        self.label.setFont(QFont(FONT_FAMILY, FONT_SIZE))
        self.label.adjustSize()

        # Size the window to fit the label
        self.resize(self.label.size())

        # Center the window on screen
        screen = QApplication.primaryScreen().geometry()
        self.move(
            (screen.width() - self.width()) // 2, (screen.height() - self.height()) // 2
        )

        # Start with zero opacity for fade-in
        self.setWindowOpacity(0.0)

        # Setup fade in animation
        self.fade_in = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in.setStartValue(0.0)
        self.fade_in.setEndValue(1.0)
        self.fade_in.setDuration(FADE_IN_TIME_MS)

        # Setup fade out animation
        self.fade_out = QPropertyAnimation(self, b"windowOpacity")
        self.fade_out.setStartValue(1.0)
        self.fade_out.setEndValue(0.0)
        self.fade_out.setDuration(FADE_OUT_TIME_MS)

        # Timer to start fade out
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.start_fade_out)

        # Timer to close the application
        self.close_timer = QTimer()
        self.close_timer.setSingleShot(True)
        self.close_timer.timeout.connect(self.close)

    def showEvent(self, event):
        super().showEvent(event)
        # Start fade in
        self.fade_in.start()
        # Start countdown to fade out after window is shown
        self.timer.start(DISPLAY_TIME_MS)

    def start_fade_out(self):
        self.fade_out.start()
        # Close the application after fade completes
        self.close_timer.start(FADE_OUT_TIME_MS)


def main():
    # Read from STDIN
    text = sys.stdin.read().strip()
    if not text:
        return

    app = QApplication(sys.argv)

    window = FadingWindow(text)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

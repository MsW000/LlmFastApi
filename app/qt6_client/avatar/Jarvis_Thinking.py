from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QTimer, Qt
# QMovie QTimer 
# QProgressBar 

class JarvisThinkingIndicator(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Jarvis thinking")
        self.setStyleSheet("color: #00ff00; font-weight: bold;")
        self.hide()

        self.dots = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.setInterval(500)

    def start_thinking(self):
        self.dots = 0
        self.setText("Jarvis thinking")
        self.show()
        self.timer.start()

    def stop_thinking(self):
        self.timer.stop()
        self.hide()

    def animate(self):
        self.dots = (self.dots + 1) % 4
        dots_text = "." * self.dots
        self.setText(f"Jarvis thinking{dots_text}")
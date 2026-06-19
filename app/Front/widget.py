import sys
import requests
from PySide6.QtCore import QTimer

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QTabWidget,
)

API_CHAT = "http://127.0.0.1:8000/chat"
API_HISTORY = "http://127.0.0.1:8000/messages"


class JarvisUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Jarvis UI")

        self.tabs = QTabWidget()

        # chat tab
        self.chat_tab = QWidget()
        self.chat_layout = QVBoxLayout()

        self.chat_view = QTextEdit()
        self.chat_view.setReadOnly(True)

        self.input = QLineEdit()

        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.send_message)

        self.chat_layout.addWidget(self.chat_view)
        self.chat_layout.addWidget(self.input)
        self.chat_layout.addWidget(self.send_btn)

        self.chat_tab.setLayout(self.chat_layout)

        # History tab
        self.history_tab = QWidget()
        self.history_layout = QVBoxLayout()

        self.history_view = QTextEdit()
        self.history_view.setReadOnly(True)

        self.refresh_btn = QPushButton("Load history")
        self.refresh_btn.clicked.connect(self.load_history)

        self.history_layout.addWidget(self.history_view)
        self.history_layout.addWidget(self.refresh_btn)

        self.history_tab.setLayout(self.history_layout)

        # add tabs
        self.tabs.addTab(self.chat_tab, "Chat")
        self.tabs.addTab(self.history_tab, "History")

        # main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

        #refresh history
        self.tabs.currentChanged.connect(self.on_tab_changed)
        self.timer = QTimer()
        self.timer.timeout.connect(self.load_history)
        self.timer.start(10000) # update ever 10 sec.

    # chat logic
    def send_message(self):
        text = self.input.text()

        if not text:
            return

        self.chat_view.append(f"You: {text}")

        try:
            response = requests.post(
                API_CHAT,
                json={"message": text},
                timeout=30
            )

            data = response.json()

            self.chat_view.append(
                f"Jarvis: {data.get('answer', 'No response')}"
            )

        except Exception as e:
            self.chat_view.append(f"Error: {e}")

        self.input.clear()

    # history logic
    def load_history(self):
        try:
            response = requests.get(API_HISTORY, timeout=30)

            if response.status_code == 200:
                messages = response.json()

                self.history_view.clear()

                for msg in messages:
                    self.history_view.append(f"You: {msg['user_message']}")
                    self.history_view.append(f"Jarvis: {msg['ai_response']}")
                    self.history_view.append("")

            else:
                self.history_view.append(f"Error: {response.status_code}")

        except Exception as e:
            self.history_view.append(f"Connection error: {e}")

    def on_tab_changed(self, index):
        if index ==1:
            self.load_history()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = JarvisUI()
    widget.show()
    sys.exit(app.exec())
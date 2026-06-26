import sys
import os
import requests
from PySide6.QtCore import QTimer
from PySide6.QtGui import QMovie, QPixmap
from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QTabWidget,
    QLabel,
)

API_CHAT = "http://127.0.0.1:8000/chat"
API_HISTORY = "http://127.0.0.1:8000/messages"


class JarvisUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Jarvis UI")

        #background 

        self.setStyleSheet("""
        QWidget {
            background: transparent;
        }

        QTabWidget {
            background: transparent;
        }

        QTabWidget::pane {
            background: transparent;
            border: none;
        }

        QTabBar::tab {
            background: rgba(0, 0, 0, 120);
            color: white;
            padding: 6px;
            border-radius: 5px;
        }

        QTextEdit {
            background-color: rgba(0, 0, 0, 160);
            color: white;
            border: none;
        }

        QLineEdit {
            background-color: rgba(0, 0, 0, 160);
            color: white;
            border: none;
        }

        QPushButton {
            background-color: rgba(0, 150, 255, 180);
            color: white;
            border-radius: 6px;
        }

        QPushButton:hover {
            background-color: rgba(0, 180, 255, 220);
        }
        """)

        self.bg = QLabel(self)
        self.bg.setGeometry(self.rect())
        self.bg.setScaledContents(True)

        base_dir = os.path.dirname(__file__)
        gif_path = os.path.join(
            base_dir,
            "..",
            "avatar",
            "Lego The Matrix.jpg"
        )

        if not os.path.exists(gif_path):
                print(f"[ERROR] File not found: {gif_path}")

        pixmap = QPixmap(gif_path)
        self.bg.setPixmap(pixmap)

        self.bg.lower()

        self.overlay = QLabel(self)
        self.overlay.setGeometry(self.rect())
        self.overlay.setStyleSheet("background-color: rgba(0,0,0,120);")

        self.overlay.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.overlay.raise_()

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("background: transparent;")
        self.tabs.setAttribute(Qt.WA_StyledBackground, True)
        

        # chat tab
        self.chat_tab = QWidget()
        self.chat_layout = QVBoxLayout()

        self.chat_view = QTextEdit()
        self.chat_view.setReadOnly(True)

        self.input = QLineEdit()

        #cursor
        self.cursor_label = QLabel(">", self)
        self.cursor_label.setStyleSheet("color: cyan; font-weight: bold;")
        self.cursor_label.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.cursor_label.show()

        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.send_message)

        self.chat_layout.addWidget(self.chat_view)
        self.chat_layout.addWidget(self.input)
        self.chat_layout.addWidget(self.send_btn)

        self.chat_tab.setLayout(self.chat_layout)

        #скрываю стандартный курсор
        self.input.setStyleSheet("""
        QLineEdit {
            color: white;
            background-color: rgba(0, 0, 0, 160);
            border: none;
            selection-color: white;
            selection-background-color: rgba(0,150,255,120);
        }
        """)

        #blink_cursor
        self.cursor_visible = True

        self.cursor_timer = QTimer()
        self.cursor_timer.timeout.connect(self.blink_cursor)
        self.cursor_timer.start(500)
        
        #timer cursor
        self.cursor_move_timer = QTimer()
        self.cursor_move_timer.timeout.connect(self.move_cursor)
        self.cursor_move_timer.start(60)

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
        QTimer.singleShot(100, self.focus_input)

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

    #resize window
    def resizeEvent(self, event):
        rect = self.rect()
        self.bg.setGeometry(rect)
        self.overlay.setGeometry(rect)
        self.move_cursor()
        return super().resizeEvent(event)
    #CURSOR
    #
    #focus cursor
    def focus_input(self):
        self.tabs.setCurrentIndex(0)
        self.input.setFocus()
        self.move_cursor()
    #position cursor
    def move_cursor(self):
        pos = self.input.mapTo(self, self.input.rect().topLeft())
        self.cursor_label.move(pos.x() - 10, pos.y() - 1)
    #blink cursor
    def blink_cursor(self):
        self.cursor_visible = not self.cursor_visible
        self.cursor_label.setVisible(self.cursor_visible)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = JarvisUI()
    widget.show()
    sys.exit(app.exec())
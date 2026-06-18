import sys
import requests

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QLineEdit,
    QPushButton
)

API_URL = "http://127.0.0.1:8000/chat" 


class JarvisUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Jarvis UI")

        # layout
        layout = QVBoxLayout()

        # чат окно
        self.chat = QTextEdit()
        self.chat.setReadOnly(True)

        # ввод
        self.input = QLineEdit()
        self.input.setPlaceholderText("Напиши сообщение...")

        # кнопка
        self.button = QPushButton("Send")
        self.button.clicked.connect(self.send_message)

        # добавляем в layout
        layout.addWidget(self.chat)
        layout.addWidget(self.input)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def send_message(self):
        text = self.input.text().strip()

        if not text:
            return

        # показываем user сообщение
        self.chat.append(f"You: {text}")

        try:
            response = requests.post(
                API_URL,
                json={"message": text},
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                self.chat.append(f"Jarvis: {data.get('response', 'No response')}")
            else:
                self.chat.append(f"Error: {response.status_code}")

        except Exception as e:
            self.chat.append(f"Connection error: {str(e)}")

        self.input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = JarvisUI()
    widget.show()

    sys.exit(app.exec())
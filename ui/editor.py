from PySide6.QtWidgets import QPlainTextEdit
from PySide6.QtGui import QFont


class CodeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()

        # Fuente tipo IDE
        font = QFont("Consolas", 15)
        self.setFont(font)

        # Texto de ejemplo
        self.setPlaceholderText("Escribe tu codigo aqui...")
from PySide6.QtWidgets import QTextEdit
from PySide6.QtGui import QFont



class CodeEditor(QTextEdit):
    def __init__(self):
        super().__init__()

                # # Fuente tipo IDE
        # font = QFont("Consolas", 15)
        # self.setFont(font)

        self.setPlaceholderText("Escribe tu codigo aqui...")
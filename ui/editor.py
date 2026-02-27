from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtGui import QFont


class CodeEditor(QTextEdit):
    def __init__(self):
        super().__init__()

        # Fuente tipo IDE
        font = QFont("Consolas", 11)
        self.setFont(font)

        # Tabulación
        self.setTabStopDistance(4 * self.fontMetrics().horizontalAdvance(" "))

        # Texto inicial opcional
        self.setPlaceholderText("Escribe tu código aquí...")
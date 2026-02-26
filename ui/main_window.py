from PySide6.QtWidgets import QMainWindow
from ui.editor import CodeEditor


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuracion ventana
        self.setWindowTitle("IDE - Compilador")
        self.resize(1000, 700)

        # Editor de codigo
        self.editor = CodeEditor()

        # El editor sera el contenido central
        self.setCentralWidget(self.editor)
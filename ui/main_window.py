from PyQt6.QtWidgets import (QMainWindow,QFileDialog,QTextEdit,QDockWidget)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt

from ui.editor import CodeEditor
import subprocess


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # ---------------- Ventana ----------------
        self.setWindowTitle("IDE Compilador")
        self.resize(1000, 700)

        # ---------------- Editor central ----------------
        self.editor = CodeEditor()
        self.setCentralWidget(self.editor)

        # archivo actual
        self.current_file = None

        # ---------------- Consola inferior ----------------
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setPlaceholderText("Salida del compilador...")

        self.console_dock = QDockWidget("Consola", self)
        self.console_dock.setWidget(self.console)

        self.addDockWidget(
            Qt.DockWidgetArea.BottomDockWidgetArea,
            self.console_dock
        )

        # Crear menú
        self.create_menu()

    # =====================================================
    #                    MENÚ
    # =====================================================

    def create_menu(self):

        menu_bar = self.menuBar()

        # ---------------- MENU ARCHIVO ----------------
        file_menu = menu_bar.addMenu("Archivo")

        new_action = QAction("Nuevo", self)
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        open_action = QAction("Abrir", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Guardar", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction("Guardar como", self)
        save_as_action.triggered.connect(self.save_as_file)
        file_menu.addAction(save_as_action)

        file_menu.addSeparator()

        exit_action = QAction("Salir", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # ---------------- MENU COMPILAR ----------------
        compile_menu = menu_bar.addMenu("Compilar")

        lex_action = QAction("Análisis Léxico", self)
        lex_action.triggered.connect(self.run_lexer)
        compile_menu.addAction(lex_action)

        syn_action = QAction("Análisis Sintáctico", self)
        syn_action.triggered.connect(self.run_parser)
        compile_menu.addAction(syn_action)

        sem_action = QAction("Análisis Semántico", self)
        sem_action.triggered.connect(self.run_semantic)
        compile_menu.addAction(sem_action)

    # =====================================================
    #                FUNCIONES ARCHIVO
    # =====================================================

    def new_file(self):
        self.editor.clear()
        self.current_file = None

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Abrir archivo",
            "",
            "Archivos (*.txt *.py *.c *.cpp)"
        )

        if file_name:
            with open(file_name, "r", encoding="utf-8") as file:
                self.editor.setPlainText(file.read())

            self.current_file = file_name

    def save_file(self):
        if self.current_file:
            with open(self.current_file, "w", encoding="utf-8") as file:
                file.write(self.editor.toPlainText())
        else:
            self.save_as_file()

    def save_as_file(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar archivo",
            "",
            "Archivos (*.txt)"
        )

        if file_name:
            with open(file_name, "w", encoding="utf-8") as file:
                file.write(self.editor.toPlainText())

            self.current_file = file_name

    # =====================================================
    #                CONSOLA
    # =====================================================

    def write_console(self, text):
        self.console.append(text)

    # =====================================================
    #            FUNCIONES DEL COMPILADOR
    # =====================================================

    def run_lexer(self):

        if not self.current_file:
            self.write_console("⚠ Guarda el archivo antes de ejecutar.")
            return

        self.write_console(">>> Ejecutando análisis léxico...\n")

        try:
            result = subprocess.run(
                ["python", "compiler/lexer.py", self.current_file],
                capture_output=True,
                text=True
            )

            if result.stdout:
                self.write_console(result.stdout)

            if result.stderr:
                self.write_console("ERROR:\n" + result.stderr)

        except Exception as e:
            self.write_console(f"Error: {e}")

    def run_parser(self):
        self.write_console(">>> Análisis sintáctico (pendiente)")

    def run_semantic(self):
        self.write_console(">>> Análisis semántico (pendiente)")
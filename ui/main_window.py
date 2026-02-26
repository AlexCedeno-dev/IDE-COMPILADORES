from PyQt6.QtWidgets import (QMainWindow, QFileDialog, QMessageBox) 
from PyQt6.QtGui import QAction
from ui.editor import CodeEditor

from PyQt6.QtWidgets import QTextEdit
import subprocess


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("IDE Compilador")
        
        #Tamaño de la ventana
        self.resize(1000, 700)

        #Editor central 
        self.editor = CodeEditor()
        print(isinstance(self.editor, QTextEdit))
        print(type(self.editor))
        self.setCentralWidget(self.editor)

        #archivo actual
        self.current_file = None

        #Crear menú
        self.create_menu()

        # Toolbar
        toolbar = self.addToolBar("Compilar")


# ----------------------------
#            MENÚ
# ----------------------------
    def create_menu(self):

        menu_bar = self.menuBar()

        #-----------------------------
        # MENU ARCHIVO
        file_menu = menu_bar.addMenu("Archivo")

        # NUEVO
        new_action = QAction("Nuevo", self)
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        # ABRIR
        open_action = QAction("Abrir", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        # GUARDAR
        save_action = QAction("Guardar", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        # GUARDAR COMO
        save_as_action = QAction("Guardar como", self)
        save_as_action.triggered.connect(self.save_as_file)
        file_menu.addAction(save_as_action)

        # CERRAR
        close_action = QAction("Cerrar", self)
        close_action.triggered.connect(self.close)
        file_menu.addAction(close_action)

        file_menu.addSeparator()

        # SALIR
        exit_action = QAction("Salir", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

#-------------------------------------------------------------
        # MENU COMPILAR
        compile_menu = self.menuBar().addMenu("Compilar")

        # Analisis Lexico
        lex_action = QAction("Analisis Léxico", self)
        lex_action.triggered.connect(self.run_lexer)
        compile_menu.addAction(lex_action)

        # Analisis Sintactico
        syn_action = QAction("Analisis Sintáctico", self)    
        syn_action.triggered.connect(self.run_parser)
        compile_menu.addAction(syn_action)

        # Analisis Semantico
        sem_action = QAction("Analisis Semántico", self)
        sem_action.triggered.connect(self.run_semantic)
        compile_menu.addAction(sem_action)


    # ---------------- FUNCIONES DE MENU DE ARCHIVOS----------------

    def new_file(self):
        self.editor.clear()
        self.current_file = None

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Abrir archivo",
            "",
            "Archivos de texto (*.txt *.c *.cpp *.py)"
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
            "Archivos de texto (*.txt)"
        )

        if file_name:
            with open(file_name, "w", encoding="utf-8") as file:
                file.write(self.editor.toPlainText())
            self.current_file = file_name


    # ---------------- FUNCIONES DE MENU DE COMPILADOR----------------

        def run_lexer(self):
            if not self.current_file:
                return
            
            result = subprocess.run(["python", "compiler/lexer.py", self.current_file], capture_output=True, text=True)
            print(result.stdout)

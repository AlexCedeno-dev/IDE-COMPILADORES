from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QKeySequence, QIcon
from ui.editor import CodeEditor
import subprocess
import os


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("IDE Compilador")
        self.resize(1200, 800)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        self.statusBar().showMessage("Línea: 1 Columna: 1")

        self.create_menu()
        self.create_toolbar()
        self.create_docks()

        self.new_file()

    # =========================
    # EDITOR ACTUAL
    # =========================

    def current_editor(self):
        return self.tabs.currentWidget()

    def update_cursor(self):
        editor = self.current_editor()
        if editor:
            cursor = editor.textCursor()
            line = cursor.blockNumber() + 1
            col = cursor.columnNumber() + 1
            self.statusBar().showMessage(f"Línea: {line} Columna: {col}")

    # =========================
    # ARCHIVOS
    # =========================

    def new_file(self):
        editor = CodeEditor()
        index = self.tabs.addTab(editor, "Sin título")
        self.tabs.setCurrentIndex(index)
        editor.cursorPositionChanged.connect(self.update_cursor)

    def open_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Abrir")

        if file:
            with open(file, "r") as f:
                content = f.read()

            editor = CodeEditor()
            editor.setPlainText(content)

            filename = os.path.basename(file)
            index = self.tabs.addTab(editor, filename)
            self.tabs.setCurrentIndex(index)

            editor.file_path = file
            editor.cursorPositionChanged.connect(self.update_cursor)

    def save_file(self):
        editor = self.current_editor()

        if hasattr(editor, "file_path"):
            with open(editor.file_path, "w") as f:
                f.write(editor.toPlainText())
        else:
            self.save_as_file()

    def save_as_file(self):
        editor = self.current_editor()

        file, _ = QFileDialog.getSaveFileName(self, "Guardar")

        if file:
            with open(file, "w") as f:
                f.write(editor.toPlainText())

            editor.file_path = file
            filename = os.path.basename(file)
            self.tabs.setTabText(self.tabs.currentIndex(), filename)

    def close_tab(self, index):
        self.tabs.removeTab(index)

    def close_file(self):
        index = self.tabs.currentIndex()
        if index != -1:
            self.tabs.removeTab(index)

    # =========================
    # MENÚ
    # =========================

    def create_menu(self):
        menu_bar = self.menuBar()

        # ===== ARCHIVO =====
        file_menu = menu_bar.addMenu("📁 Archivo")

        new_action = QAction("Nuevo", self)
        new_action.setShortcut(QKeySequence("Ctrl+N"))
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        open_action = QAction("Abrir", self)
        open_action.setShortcut(QKeySequence("Ctrl+O"))
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Guardar", self)
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        saveas_action = QAction("Guardar como", self)
        saveas_action.setShortcut(QKeySequence("Ctrl+Shift+S"))
        saveas_action.triggered.connect(self.save_as_file)
        file_menu.addAction(saveas_action)

        close_action = QAction("Cerrar", self)
        close_action.setShortcut(QKeySequence("Ctrl+W"))
        close_action.triggered.connect(self.close_file)
        file_menu.addAction(close_action)

        file_menu.addSeparator()

        exit_action = QAction("Salir", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # ===== PESTAÑAS =====
        tabs_menu = menu_bar.addMenu("🗂️ Pestañas")

        next_tab = QAction("Siguiente", self)
        next_tab.setShortcut(QKeySequence("Ctrl+Tab"))
        next_tab.triggered.connect(
            lambda: self.tabs.setCurrentIndex(
                (self.tabs.currentIndex() + 1) % self.tabs.count()
            )
        )
        tabs_menu.addAction(next_tab)

        prev_tab = QAction("Anterior", self)
        prev_tab.setShortcut(QKeySequence("Ctrl+Shift+Tab"))
        prev_tab.triggered.connect(
            lambda: self.tabs.setCurrentIndex(
                (self.tabs.currentIndex() - 1) % self.tabs.count()
            )
        )
        tabs_menu.addAction(prev_tab)

        # ===== TEMAS =====
        theme_menu = menu_bar.addMenu("🎨 Temas")

        dark = QAction("Oscuro", self)
        dark.triggered.connect(lambda: self.set_theme("dark"))
        theme_menu.addAction(dark)

        light = QAction("Claro", self)
        light.triggered.connect(lambda: self.set_theme("light"))
        theme_menu.addAction(light)

        dracula = QAction("Dracula", self)
        dracula.triggered.connect(lambda: self.set_theme("dracula"))
        theme_menu.addAction(dracula)

    # =========================
    # TOOLBAR
    # =========================

    def create_toolbar(self):
        toolbar = self.addToolBar("Compilar")

        toolbar.addAction("Léxico", self.run_lexer)
        toolbar.addAction("Sintáctico", self.run_parser)
        toolbar.addAction("Semántico", self.run_semantic)
        toolbar.addAction("Intermedio", self.run_intermediate)
        toolbar.addAction("Ejecutar", self.run_execution)

    # =========================
    # DOCKS
    # =========================

    def create_docks(self):
        self.lex = QTextEdit(); self.lex.setReadOnly(True)
        self.syn = QTextEdit(); self.syn.setReadOnly(True)
        self.sem = QTextEdit(); self.sem.setReadOnly(True)
        self.inter = QTextEdit(); self.inter.setReadOnly(True)
        self.sym = QTextEdit(); self.sym.setReadOnly(True)
        self.err = QTextEdit(); self.err.setReadOnly(True)
        self.console = QTextEdit(); self.console.setReadOnly(True)

        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea,
                           self.createDock("Léxico", self.lex))
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea,
                           self.createDock("Sintáctico", self.syn))
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea,
                           self.createDock("Semántico", self.sem))
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea,
                           self.createDock("Intermedio", self.inter))
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea,
                           self.createDock("Tabla de Símbolos", self.sym))
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea,
                           self.createDock("Errores", self.err))
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea,
                           self.createDock("Consola", self.console))

    def createDock(self, title, widget):
        dock = QDockWidget(title, self)
        dock.setWidget(widget)
        return dock

    # =========================
    # COMPILADOR
    # =========================

    def run_process(self, script, output):
        editor = self.current_editor()

        if not hasattr(editor, "file_path"):
            self.console.append("Guarda el archivo primero")
            return

        result = subprocess.run(
            ["python", f"compiler/{script}", editor.file_path],
            capture_output=True,
            text=True
        )

        output.setText(result.stdout)

        if result.stderr:
            self.err.setText(result.stderr)

    def run_lexer(self): self.run_process("lexer.py", self.lex)
    def run_parser(self): self.run_process("parser.py", self.syn)
    def run_semantic(self): self.run_process("semantic.py", self.sem)
    def run_intermediate(self): self.run_process("intermediate.py", self.inter)
    def run_execution(self): self.run_process("executor.py", self.console)

    # =========================
    # TEMAS
    # =========================

    def set_theme(self, theme):

        if theme == "dark":
            self.setStyleSheet("""
                QMainWindow { background:#1e1e1e; color:white; }
                QTextEdit { background:#252526; color:#f8f8f2; }
                QTabBar::tab:selected { background:#007acc; }
            """)

        elif theme == "light":
            self.setStyleSheet("""
                QMainWindow { background:white; color:black; }
                QTextEdit { background:white; color:black; }
                QTabBar::tab:selected { background:#ddd; }
            """)

        elif theme == "dracula":
            self.setStyleSheet("""
                QMainWindow { background:#282a36; color:#f8f8f2; }
                QTextEdit { background:#44475a; color:#f8f8f2; }
                QTabBar::tab:selected { background:#bd93f9; }
            """)
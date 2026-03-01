from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtGui import QAction, QKeySequence, QIcon
from ui.editor import CodeEditor
import subprocess
import os

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.settings = QSettings("IDECompilador", "IDEConfig")
        self.setWindowTitle("IDE Compilador")
        self.resize(1200, 800)

        self.closed_tabs = []

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        self.statusBar().showMessage("Línea: 1 Columna: 1")

        self.create_menu()
        self.create_toolbar()
        self.create_docks()

        self.new_file()

        saved_theme = self.settings.value("theme", "dark")
        self.set_theme(saved_theme)

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
        editor = self.tabs.widget(index)

        if editor:
            self.closed_tabs.append({
                "content": editor.toPlainText(),
                "title": self.tabs.tabText(index),
                "file_path": getattr(editor, "file_path", None)
            })

        self.tabs.removeTab(index)

    def close_file(self):
        index = self.tabs.currentIndex()
        if index != -1:
            self.tabs.removeTab(index)

    def reopen_last_tab(self):
        if not self.closed_tabs:
            return

        data = self.closed_tabs.pop()

        editor = CodeEditor()
        editor.setPlainText(data["content"])

        if data["file_path"]:
            editor.file_path = data["file_path"]

        index = self.tabs.addTab(editor, data["title"])
        self.tabs.setCurrentIndex(index)

        editor.cursorPositionChanged.connect(self.update_cursor)


    # =========================
    # EDITAR FUNCIONES
    # =========================

    def current_editor(self):
        editor = self.tabs.currentWidget()
        if isinstance(editor, CodeEditor):
            return editor
        return None

    def undo_text(self):
        editor = self.current_editor()
        if editor:
            editor.undo()

    def redo_text(self):
        editor = self.current_editor()
        if editor:
            editor.redo()

    def cut_text(self):
        editor = self.current_editor()
        if editor:
            editor.cut()

    def copy_text(self):
        editor = self.current_editor()
        if editor:
            editor.copy()

    def paste_text(self):
        editor = self.current_editor()
        if editor:
            editor.paste()

    def select_all_text(self):
        editor = self.current_editor()
        if editor:
            editor.selectAll()

    def show_find_dialog(self):
        editor = self.current_editor()
        if editor:
            text, ok = QInputDialog.getText(self, "Buscar", "Texto:")
            if ok and text:
                if not editor.find(text):
                    QMessageBox.information(self, "Buscar", "No se encontró el texto")

    # =========================
    # ZOOM
    # =========================

    def zoom_in(self):
        editor = self.current_editor()
        if editor:
            editor.zoomIn(2)

    def zoom_out(self):
        editor = self.current_editor()
        if editor:
            editor.zoomOut(2)

    def reset_zoom(self):
        editor = self.current_editor()
        if editor:
            font = editor.font()
            font.setPointSize(12)
            editor.setFont(font)

    # =========================
    # MENÚ
    # =========================

    def create_menu(self):
        menu_bar = self.menuBar()

        # ===== ARCHIVO =====
        file_menu = menu_bar.addMenu("Archivo")

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

        # ===== EDITAR =====
        edit_menu = menu_bar.addMenu("Editar")

        undo_action = QAction("Deshacer", self)
        undo_action.setShortcut(QKeySequence("Ctrl+Z"))
        undo_action.triggered.connect(self.undo_text)
        edit_menu.addAction(undo_action)

        redo_action = QAction("Rehacer", self)
        redo_action.setShortcut(QKeySequence("Ctrl+Y"))
        redo_action.triggered.connect(self.redo_text)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        cut_action = QAction("Cortar", self)
        cut_action.setShortcut(QKeySequence("Ctrl+X"))
        cut_action.triggered.connect(self.cut_text)
        edit_menu.addAction(cut_action)

        copy_action = QAction("Copiar", self)
        copy_action.setShortcut(QKeySequence("Ctrl+C"))
        copy_action.triggered.connect(self.copy_text)
        edit_menu.addAction(copy_action)

        paste_action = QAction("Pegar", self)
        paste_action.setShortcut(QKeySequence("Ctrl+V"))
        paste_action.triggered.connect(self.paste_text)
        edit_menu.addAction(paste_action)

        edit_menu.addSeparator()

        select_all_action = QAction("Seleccionar Todo", self)
        select_all_action.setShortcut(QKeySequence("Ctrl+A"))
        select_all_action.triggered.connect(self.select_all_text)
        edit_menu.addAction(select_all_action)

        edit_menu.addSeparator()

        find_action = QAction("Buscar", self)
        find_action.setShortcut(QKeySequence("Ctrl+F"))
        find_action.triggered.connect(self.show_find_dialog)
        edit_menu.addAction(find_action)

        edit_menu.addSeparator()

        zoom_in_action = QAction("Zoom +", self)
        zoom_in_action.setShortcut(QKeySequence("Ctrl++"))
        zoom_in_action.triggered.connect(self.zoom_in)
        edit_menu.addAction(zoom_in_action)

        zoom_out_action = QAction("Zoom -", self)
        zoom_out_action.setShortcut(QKeySequence("Ctrl+-"))
        zoom_out_action.triggered.connect(self.zoom_out)
        edit_menu.addAction(zoom_out_action)

        reset_zoom_action = QAction("Restablecer Zoom", self)
        reset_zoom_action.setShortcut(QKeySequence("Ctrl+0"))
        reset_zoom_action.triggered.connect(self.reset_zoom)
        edit_menu.addAction(reset_zoom_action)        
        
        # ===== PESTAÑAS =====
        tabs_menu = menu_bar.addMenu("Pestañas")
        tabs_menu.addSeparator()

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
        theme_menu = menu_bar.addMenu("Temas")

        dark = QAction("Oscuro", self)
        dark.triggered.connect(lambda: self.set_theme("dark"))
        theme_menu.addAction(dark)

        light = QAction("Claro", self)
        light.triggered.connect(lambda: self.set_theme("light"))
        theme_menu.addAction(light)

        dracula = QAction("Dracula", self)
        dracula.triggered.connect(lambda: self.set_theme("dracula"))
        theme_menu.addAction(dracula)

        ocean = QAction("Ocean Blue", self)
        ocean.triggered.connect(lambda: self.set_theme("ocean"))
        theme_menu.addAction(ocean)

        sunset = QAction("Sunset", self)
        sunset.triggered.connect(lambda: self.set_theme("sunset"))
        theme_menu.addAction(sunset)

        forest = QAction("Forest", self)
        forest.triggered.connect(lambda: self.set_theme("forest"))
        theme_menu.addAction(forest)

        neon = QAction("Neon Purple", self)
        neon.triggered.connect(lambda: self.set_theme("neon"))
        theme_menu.addAction(neon)

        hacker = QAction("Hacker Classic", self)
        hacker.triggered.connect(lambda: self.set_theme("hacker"))
        theme_menu.addAction(hacker)

        # ===== DESARROLLADORES =====
        dev_menu = menu_bar.addMenu("Desarrolladores")

        about_dev = QAction("Equipo de Desarrollo", self)
        about_dev.triggered.connect(self.show_developers)
        dev_menu.addAction(about_dev)

    # =========================
    # TOOLBAR
    # =========================

    def create_toolbar(self):

        self.toolbar = self.addToolBar("Compilar")
        self.toolbar.setMovable(False)

        self.lex_btn = QAction("Léxico", self)
        self.lex_btn.setCheckable(True)
        self.lex_btn.triggered.connect(lambda: self.activate_button(self.lex_btn, self.run_lexer))

        self.syn_btn = QAction("Sintáctico", self)
        self.syn_btn.setCheckable(True)
        self.syn_btn.triggered.connect(lambda: self.activate_button(self.syn_btn, self.run_parser))

        self.sem_btn = QAction("Semántico", self)
        self.sem_btn.setCheckable(True)
        self.sem_btn.triggered.connect(lambda: self.activate_button(self.sem_btn, self.run_semantic))

        self.int_btn = QAction("Intermedio", self)
        self.int_btn.setCheckable(True)
        self.int_btn.triggered.connect(lambda: self.activate_button(self.int_btn, self.run_intermediate))

        self.exe_btn = QAction("Ejecutar", self)
        self.exe_btn.setCheckable(True)
        self.exe_btn.triggered.connect(lambda: self.activate_button(self.exe_btn, self.run_execution))

        self.toolbar.addAction(self.lex_btn)
        self.toolbar.addAction(self.syn_btn)
        self.toolbar.addAction(self.sem_btn)
        self.toolbar.addAction(self.int_btn)
        self.toolbar.addAction(self.exe_btn)

    def activate_button(self, btn, func):
        for action in self.toolbar.actions():
            action.setChecked(False)

        btn.setChecked(True)
        func()

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

        dock.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable |
            QDockWidget.DockWidgetFeature.DockWidgetFloatable |
            QDockWidget.DockWidgetFeature.DockWidgetClosable
        )

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

    def run_lexer(self):
        self.run_process("lexer.py", self.lex)

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

        elif theme == "ocean":
            self.setStyleSheet("""
                QMainWindow { background:#0f172a; color:#e2e8f0; }
                QTextEdit { background:#1e293b; color:#e2e8f0; }
                QTabWidget::pane { border: 1px solid #334155; }
                QTabBar::tab { background:#1e293b; padding:8px; }
                QTabBar::tab:selected { background:#3b82f6; color:white; }
                QMenuBar { background:#0f172a; color:#e2e8f0; }
                QMenu { background:#1e293b; color:#e2e8f0; }
            """)

        elif theme == "sunset":
            self.setStyleSheet("""
                QMainWindow { background:#2b1d1d; color:#ffe4d6; }
                QTextEdit { background:#3a2a2a; color:#fff3e6; }
                QTabBar::tab { background:#3a2a2a; padding:8px; }
                QTabBar::tab:selected { background:#ff7b00; color:black; }
                QMenuBar { background:#2b1d1d; color:#ffe4d6; }
                QMenu { background:#3a2a2a; color:#fff3e6; }
            """)

        elif theme == "forest":
            self.setStyleSheet("""
                QMainWindow { background:#0d1f1a; color:#d1fae5; }
                QTextEdit { background:#13332b; color:#a7f3d0; }
                QTabBar::tab { background:#13332b; padding:8px; }
                QTabBar::tab:selected { background:#10b981; color:black; }
                QMenuBar { background:#0d1f1a; color:#d1fae5; }
                QMenu { background:#13332b; color:#a7f3d0; }
            """)            

        elif theme == "neon":
            self.setStyleSheet("""
                QMainWindow { background:#140021; color:#f5d0fe; }
                QTextEdit { background:#1f0033; color:#e879f9; }
                QTabBar::tab { background:#1f0033; padding:8px; }
                QTabBar::tab:selected { background:#c026d3; color:white; }
                QMenuBar { background:#140021; color:#f5d0fe; }
                QMenu { background:#1f0033; color:#e879f9; }
            """)

        elif theme == "hacker":
            self.setStyleSheet("""
                QMainWindow { background:black; color:#00ff00; }
                QTextEdit { background:black; color:#00ff00; }
                QTabBar::tab { background:#001100; padding:8px; }
                QTabBar::tab:selected { background:#00aa00; color:black; }
                QMenuBar { background:black; color:#00ff00; }
                QMenu { background:#001100; color:#00ff00; }
            """)

        self.settings.setValue("theme", theme)

    
    def show_developers(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Desarrolladores")
        dialog.resize(420, 300)

        layout = QVBoxLayout()

        title = QLabel("IDE Compilador")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size:18px; font-weight:bold;")

        subtitle = QLabel("Equipo de Desarrollo:")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        dev1 = QLabel("Jesus Abraham Robledo Lopez")
        dev1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dev1.setStyleSheet("font-size:14px; color:#3b82f6;")

        id1 = QLabel("ID: 284745")
        id1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        dev2 = QLabel("Edgar Alejandro Cedeño Suarez")
        dev2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dev2.setStyleSheet("font-size:14px; color:#10b981;")

        id2 = QLabel("ID: 262728")
        id2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        version = QLabel("Versión 1.0")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(10)
        layout.addWidget(dev1)
        layout.addWidget(id1)
        layout.addSpacing(10)
        layout.addWidget(dev2)
        layout.addWidget(id2)
        layout.addSpacing(10)
        layout.addWidget(version)

        dialog.setLayout(layout)
        dialog.exec()
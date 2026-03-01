from PyQt6.QtWidgets import QPlainTextEdit, QWidget, QTextEdit
from PyQt6.QtGui import QColor, QTextFormat, QPainter, QFont
from PyQt6.QtCore import Qt, QRect, QSize
from ui.syntax_highlighter import SyntaxHighlighter
from PyQt6.QtGui import QAction, QKeySequence, QIcon
import platform


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def sizeHint(self):
        return QSize(self.codeEditor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)
    


class CodeEditor(QPlainTextEdit):

    def __init__(self):
        super().__init__()

        if platform.system() == "Darwin":
            self.setFont(QFont("Menlo", 11))
        else:
            self.setFont(QFont("Consolas", 11))

        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1e1e1e;
                color: white;
                border: none;
            }
        """)

        self.lineNumberArea = LineNumberArea(self)

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()

        # activar syntax highlighting
        self.highlighter = SyntaxHighlighter(self.document())

    def lineNumberAreaWidth(self):
        digits = len(str(self.blockCount()))
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(),
                                       self.lineNumberArea.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(
            QRect(cr.left(), cr.top(),
                  self.lineNumberAreaWidth(), cr.height())
        )

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor(30, 30, 30))

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = int(self.blockBoundingGeometry(
            block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(Qt.GlobalColor.white)
                painter.drawText(0, top, self.lineNumberArea.width(),
                                 self.fontMetrics().height(),
                                 Qt.AlignmentFlag.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + \
                int(self.blockBoundingRect(block).height())
            blockNumber += 1

    def highlightCurrentLine(self):
        extraSelections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()

            lineColor = QColor(40, 40, 40)

            selection.format.setBackground(lineColor)
            selection.format.setProperty(
                QTextFormat.Property.FullWidthSelection, True)

            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()

            extraSelections.append(selection)

        self.setExtraSelections(extraSelections)

    def wheelEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.angleDelta().y() > 0:
                self.zoomIn(2)
            else:
                self.zoomOut(2)
        else:
            super().wheelEvent(event)
from PySide2.QtWidgets import QWidget, QPlainTextEdit, QTextEdit, QAction, QLineEdit, QApplication
from PySide2.QtGui import QColor, QPainter, QTextFormat, QFont, QKeySequence,\
    QKeyEvent, QTextCharFormat, QBrush, QTextCursor
from PySide2.QtCore import Qt, QRect, QSize, Signal, QEvent, QPoint, QRegExp


class Editor(QPlainTextEdit):

    keyPressed = Signal(QEvent)

    class _NumberArea(QWidget):
        def __init__(self, editor):
            super().__init__(editor)
            self.codeEditor = editor

        def sizeHint(self):
            return QSize(self.editor.lineNumberAreaWidth(), 0)

        def paintEvent(self, event):
            self.codeEditor.lineNumberAreaPaintEvent(event)

    def __init__(self, **kwargs):
        parent = kwargs["parent"] if "parent" in kwargs else None
        super().__init__(parent)
        self._addSaveAction = kwargs["saveAction"] if "saveAction" in kwargs else False
        self._addSaveAction = kwargs["saveAction"] if "saveAction" in kwargs else False
        if self._addSaveAction:
            self.saveACT = QAction("Save")
            self.saveACT.setShortcut(QKeySequence("Ctrl+S"))
            self.saveACT.triggered.connect(lambda: self._save_file(self.toPlainText()))
            self.addAction(self.saveACT)
        self._saveCB = kwargs["saveFunction"] if "saveFunction" in kwargs else None
        self.setFont(QFont("Courier New", 11))
        self.lineNumberArea = Editor._NumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth(0)
        self.findHighlightFormat = QTextCharFormat()
        self.findHighlightFormat.setBackground(QBrush(QColor("red")))
        self.searchTxtBx = None

    def lineNumberAreaWidth(self):
        digits = 5
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(229, 248, 255, 255)
            
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        #self.setExtraSelections(extraSelections)

    def setTheme(self):
        self.update()

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        blockColor = QColor(233,233,233)
        
        painter.fillRect(event.rect(), blockColor)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        fontColor = QColor(130, 130, 130, 255)

        # Just to make sure I use the right font
        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                fFont = QFont("Courier New", 10)
                painter.setPen(fontColor)
                painter.setFont(fFont)
                painter.drawText(0, top, self.lineNumberArea.width(), height, Qt.AlignCenter, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    def contextMenuEvent(self, event):
        menu = self.createStandardContextMenu()
        if self._addSaveAction:
            index = 0
            if len(menu.actions()) > 6: index = 5
            act_beforeACT = menu.actions()[index]
            menu.insertAction(act_beforeACT, self.saveACT)
        action = menu.addAction("Find" + "\t" + "Ctrl+F")
        action.triggered.connect(self.find_key)
        menu.popup(event.globalPos())

    def keyPressEvent(self, event:QKeyEvent):
        if event.key() == Qt.Key_F and (event.modifiers() & Qt.ControlModifier):
            self.find_key()
        if event.key() == Qt.Key_Escape:
            if self.searchTxtBx is not None:
                self.searchTxtBx.hide()
                self.searchTxtBx = None
                self.clear_format()
        super(Editor, self).keyPressEvent(event)

    def find_key(self):
        if self.searchTxtBx is None:
            self.searchTxtBx = QLineEdit(self)
            p = self.geometry().topRight() - self.searchTxtBx.geometry().topRight() - QPoint(50, 0)
            self.searchTxtBx.move(p)
            self.searchTxtBx.show()
            self.searchTxtBx.textChanged.connect(self.find_with_pattern)
        self.searchTxtBx.setFocus()

    def find_with_pattern(self, pattern):
        self.setUndoRedoEnabled(False)
        self.clear_format()
        if pattern == "":
            return
        cursor = self.textCursor()
        regex = QRegExp(pattern)
        pos = 0
        index = regex.indexIn(self.toPlainText(), pos)
        while index != -1:
            cursor.setPosition(index)
            cursor.movePosition(QTextCursor.EndOfWord, QTextCursor.KeepAnchor, 1)
            cursor.mergeCharFormat(self.findHighlightFormat)
            pos = index + regex.matchedLength()
            index = regex.indexIn(self.toPlainText(), pos)
        self.setUndoRedoEnabled(True)

    def clear_format(self):
        cursor = self.textCursor()
        cursor.select(QTextCursor.Document)
        cursor.setCharFormat(QTextCharFormat())
        cursor.clearSelection()
        self.setTextCursor(cursor)

    def setSaveCB(self, cb):
        self._saveCB = cb

    def _save_file(self, text):
        if self._saveCB is not None:
            self._saveCB(text)



from PySide2.QtCore import Qt, Signal
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import QSizePolicy, QAction
from PySide2.QtWidgets import QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, QGridLayout,\
    QLineEdit, QPushButton, QGroupBox, QLabel, QComboBox, QSplitter, QFileDialog
from GUI.QImageLabel import QImageLabel
from GUI.editor import Editor

class MainWindow(QMainWindow):

    convert = Signal(str)

    def __init__(self):
        super().__init__(None)
        self.browse_btn = QPushButton(self, text="Browse")
        self.convert_btn = QPushButton(self, text="Convert")
        self.img_widget = QImageLabel(parent=self)
        self.img_path = ""
        self.editor = Editor(parent=self)
        self.__draw()
        self.__connect()


    def __draw(self):
        mainW = QSplitter(Qt.Horizontal, parent=self)
        mainW.addWidget(self.__draw_left_panel(mainW))
        mainW.addWidget(self.__draw_right_panel(mainW))
        self.setCentralWidget(mainW)

    def __draw_right_panel(self, parent=None):
        return self.editor

    def __draw_left_panel(self, parent=None):
        leftW = QWidget(parent)
        leftW.setLayout(QVBoxLayout())
        leftW.layout().addWidget(self.img_widget)
        leftW.layout().addWidget(self.browse_btn)
        leftW.layout().addWidget(self.convert_btn)
        return leftW

    def __connect(self):
        self.browse_btn.clicked.connect(lambda: self.__on_browse_clicked())
        self.convert_btn.clicked.connect(lambda: self.convert.emit(self.img_path))
    
    def __on_browse_clicked(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Image files (*.jpg *.png)")[0]
        if fname != "":
            self.img_widget.setImagePath(fname)
            self.img_path = fname
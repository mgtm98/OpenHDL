from PySide2.QtCore import QPoint, Qt
from PySide2.QtGui import QPixmap, QPainter
from PySide2.QtWidgets import QLabel, QWidget, QFrame, QSizePolicy


class QImageLabel(QLabel):
    def __init__(self, img_path:str="", parent:QWidget=None):
        super(QImageLabel, self).__init__(parent)
        self.setFrameStyle(QFrame.StyledPanel)
        self.__pixmap = QPixmap(img_path)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

    def setImagePath(self, path:str):
        self.__pixmap = QPixmap(path)
        self.repaint()

    def paintEvent(self, event):
        size = self.size()
        painter = QPainter(self)
        point = QPoint(0, 0)
        scaledPix = self.__pixmap.scaled(size, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        point.setX((size.width() - scaledPix.width()) / 2)
        point.setY((size.height() - scaledPix.height()) / 2)
        painter.drawPixmap(point, scaledPix)
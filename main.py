from sys import argv, exit
import sys
import requests

from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class wdow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.x = int(650 * 2)
        self.y = int(450 * 2)

        self.setGeometry(600, 100, self.x, self.y)
        self.setMinimumSize(self.x, self.y)
        self.setStyleSheet("background-color: black")
        self.setWindowTitle('MapsAPI')

        self.zoom_par = [20, 13, 7, 4, 2, 1, 0.5, 0.2, 0.1, 0.07, 0.03, 0.02, 0.01, 0.007, 0.003, 0.001, 0.0005,
                         0.0002, 0.00014, 0.0001, 0.00005]
        self.point_k = [0.2]
        self.map = QLabel(self)
        self.zoom = 11
        self.longitude = 55.97
        self.width = 54.75
        self.flag = ''

        self.draw_map()

    def draw_map(self):
        pt = f'&pt={self.flag}' if self.flag else ''
        self.req = requests.get(f'https://static-maps.yandex.ru/1.x/?ll={self.longitude},{self.width}&'
                                f'l=map&z={self.zoom}&size=650,450{pt}')
        with open('map.png', 'wb') as img:
            img.write(self.req.content)
        pix_m = QPixmap('map.png')
        pix_m = pix_m.scaled(self.x, self.y)
        self.map.setPixmap(pix_m)

    def keyPressEvent(self, event):
        if event.key():
            shift = self.zoom_par[self.zoom - 1]
            if event.key() == Qt.Key_Down:
                self.width -= shift
            if event.key() == Qt.Key_Up:
                self.width += shift
            if event.key() == Qt.Key_Left:
                self.longitude -= shift
            if event.key() == Qt.Key_Right:
                self.longitude += shift

            if event.key() == Qt.Key_PageDown:
                if self.zoom > 1:
                    self.zoom -= 1
            if event.key() == Qt.Key_PageUp:
                if self.zoom < 21:
                    self.zoom += 1

            if event.key() == Qt.Key_Escape:
                self.flag = ''
            self.draw_map()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


sys.excepthook = except_hook

if __name__ == '__main__':
    app = QApplication(argv)
    w = wdow()
    w.show()
    exit(app.exec_())

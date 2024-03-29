from sys import argv, exit
import sys
import requests

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QTextEdit
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon, QFont, QPainter


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
        self.skl = QLabel(self)
        self.zoom = 11
        self.longitude = 55.97
        self.width = 54.75
        self.flag = ''
        self.map_type = 'map'
        self.pt = ''

        self.searchResult = QTextEdit(self)
        self.searchResult.setGeometry(0, 0, 500, self.y)
        self.searchResult.setFont(QFont('Calibri', 16))
        self.searchResult.setStyleSheet('background-color: rgb(255, 255, 255, 150);')
        self.searchResult.setReadOnly(True)

        self.changeLayerBtn = QPushButton(self) # Изменение типов карты + красивые иконки
        self.changeLayerBtn.setGeometry(self.x - 80, 30, 50, 50)
        self.changeLayerBtn.setIcon(QIcon('data/layer.png'))
        self.changeLayerBtn.setIconSize(QSize(50, 50))
        self.changeLayerBtn.setStyleSheet('background-color: rgba(0, 0, 0, 0);')
        self.changeLayerBtn.clicked.connect(self.changeLayers)

        self.searchPlace = QLineEdit(self) # Поле ввода
        self.searchPlace.setGeometry(25, 25, 400, 40)
        self.searchPlace.setStyleSheet('background-color: rgba(0, 0, 0, 0);')
        self.searchPlace.setFont(QFont('Calibri', 16))

        self.searchBtn = QPushButton(self) # Кнопка поиска + красивые иконки
        self.searchBtn.setGeometry(430, 20, 50, 50)
        self.searchBtn.setIcon(QIcon('data/search.png'))
        self.searchBtn.setIconSize(QSize(40, 40))
        self.searchBtn.setStyleSheet('background-color: rgba(0, 0, 0, 0);')
        self.searchBtn.clicked.connect(self.search)

        self.deleteBtn = QPushButton(self) # Кнопка отчистки
        self.deleteBtn.setStyleSheet('background-color: rgba(0, 0, 0, 0);')
        self.deleteBtn.setFont(QFont('Calibri', 24, 100))
        self.deleteBtn.setText('X')
        self.deleteBtn.setGeometry(390, 30, 40, 28)
        self.deleteBtn.clicked.connect(self.delete)

        self.hideBtn = QPushButton(self) # Кнопка скрытия результатов
        self.hideBtn.setGeometry(500, 20, 20, 50)
        self.hideBtn.setStyleSheet('background-color: rgba(0, 0, 0, 0); border: none;')
        self.hideBtn.setText('<')
        self.hideBtn.setFont(QFont('Calibri', 24, 80))
        self.hideBtn.clicked.connect(self.hideMenu)

        self.drawMap()

    def hideMenu(self): # Срытие/показ результатов
        if self.searchResult.isHidden():
            self.searchResult.show()
            self.hideBtn.setText('<')
        else:
            self.searchResult.hide()
            self.hideBtn.setText('>')

    def delete(self): # Удаление запроса
        self.searchResult.setText('')
        self.searchPlace.setText('')
        self.pt = ''
        self.drawMap()

    def search(self): # Обработчик запросов
        text = self.searchPlace.text()
        if text:
            try:
                self.findReq = requests.get(f'https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de'
                                            f'7710b&geocode={text}&format=json').json()['response']['GeoObjectCollection'] \
                    ['featureMember'][0]
                cord = self.findReq['GeoObject']['Point']['pos']
                self.searchResult.setText('\n\n' + self.findReq['GeoObject']['metaDataProperty']['GeocoderMetaData']['text'])
                self.pt = ''
                self.longitude = float(cord[:cord.index(' ')])
                self.width = float(cord[cord.index(' '):])
                self.pt = f'&pt={self.longitude},{self.width},flag'
                self.drawMap()
            except:
                self.searchResult.setText('\n\nНичего не найдено...')

    def changeColor(self, color: str): # 'dark' or 'white'
        if color == 'dark':
            self.changeLayerBtn.setIcon(QIcon('data/layer_negate.png'))
        else:
            self.changeLayerBtn.setIcon(QIcon('data/layer.png'))

    def changeLayers(self): # Красивое изменение иконок в зависимости от типа карты (На спутнике сливается)
        if self.map_type == 'map':
            self.map_type = 'sat'
            self.changeColor('dark')
        elif self.map_type == 'sat':
            self.map_type = 'skl'
            self.changeColor('dark')
        else:
            self.map_type = 'map'
            self.changeColor('white')
        self.drawMap()

    def drawMap(self): # Отрисовка основной карты
        zoom = f'z={self.zoom}&' if self.zoom else ''
        self.req = requests.get(f'https://static-maps.yandex.ru/1.x/?ll={self.longitude},{self.width}&'
                                f'{zoom}size=650,450{self.pt}&l={self.map_type if self.map_type != "skl" else "sat"}')
        with open('data/map.png', 'wb') as img:
            img.write(self.req.content)
        pixMap = QPixmap('data/map.png').scaled(self.x, self.y)

        if self.map_type == 'skl': # Отрисовка гибридного типа карты
            sklReq = requests.get(f'https://static-maps.yandex.ru/1.x/?ll={self.longitude},{self.width}&'
                                  f'{zoom}size=650,450&l=skl')
            with open('data/skl.png', 'wb') as img:
                img.write(sklReq.content)
            pixSkl = QPixmap('data/skl.png')
            pixSkl = pixSkl.scaled(self.x, self.y)
            painter = QPainter(pixMap)
            painter.save()
            painter.drawPixmap(0, 0, pixSkl) # Совмещение спутника и дорог
            painter.restore()
            painter.end()
        self.map.setPixmap(pixMap)

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
            if event.key() == Qt.Key_Enter:
                self.search()

            if self.longitude > 175:
                self.longitude = 175
            if self.longitude < -175:
                self.longitude = -175
            if self.width > 85:
                self.width = 85
            if self.width < -85:
                self.width = -85

            self.drawMap()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


sys.excepthook = except_hook

if __name__ == '__main__':
    app = QApplication(argv)
    w = wdow()
    w.show()
    exit(app.exec_())

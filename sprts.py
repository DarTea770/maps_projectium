import os

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt
import sys
import requests

def get_img(map_request):
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    # Запишем полученное изображение в файл.
    map_file = "map.png"
    os.remove(map_file)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file


class Widget(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        scr = QtWidgets.QApplication.desktop().screenGeometry()
        self.w, self.h = scr.width(), scr.height()
        self.setGeometry(0, 0, self.w - 30, self.h - 30)

        self.map_size = 0.0016
        request = f"https://static-maps.yandex.ru/1.x/?l=sat&ll=37.677564,55.653309&spn={self.map_size},{self.map_size}&size=650,450"
        self.pixmap = QtGui.QPixmap(get_img(request)).scaled(self.w - 30, self.h, Qt.IgnoreAspectRatio)
        self.image = QtWidgets.QLabel(self)
        self.image.move(0, 0)
        self.image.resize(self.w, self.h)
        self.image.setPixmap(self.pixmap)

        self.btn_size_up = QtWidgets.QPushButton(self)
        self.btn_size_up.setText('+')
        self.btn_size_up.move(self.w // 40, self.h // 2 - self.h // 25)
        self.btn_size_up.resize(self.w // 30, self.w // 30)
        self.btn_size_up.clicked.connect(self.size_map_up)

        self.btn_size_down = QtWidgets.QPushButton(self)
        self.btn_size_down.setText('-')
        self.btn_size_down.move(self.w // 40, self.h // 2 + self.h // 25)
        self.btn_size_down.resize(self.w // 30, self.w // 30)
        self.btn_size_down.clicked.connect(self.size_map_down)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Equal:
            self.size_map_up()
        if event.key() == Qt.Key_Minus:
            self.size_map_down()

    def size_map_up(self):
        if self.map_size >= 0.0007:
            if self.map_size >= 0.01:
                self.map_size = round(self.map_size - 0.1, 4)
            elif self.map_size >= 0.0045:
                self.map_size = round(self.map_size - 0.003, 4)
            else:
                self.map_size = round(self.map_size - 0.001, 4)
        request = f"https://static-maps.yandex.ru/1.x/?l=sat&ll=37.677564,55.653309&spn={self.map_size},{self.map_size}&size=650,450"
        pixmap = QtGui.QPixmap(get_img(request)).scaled(self.w - 30, self.h, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.image.setPixmap(pixmap)

    def size_map_down(self):
        if self.map_size <= 0.5:
            self.map_size += 0.002 if self.map_size < 0.006 else 0.1
            self.map_size = round(self.map_size, 4)
        request = f"https://static-maps.yandex.ru/1.x/?l=sat&ll=37.677564,55.653309&spn={self.map_size},{self.map_size}&size=650,450"
        pixmap = QtGui.QPixmap(get_img(request)).scaled(self.w - 30, self.h, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.image.setPixmap(pixmap)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    wind = Widget()
    wind.show()
    sys.exit(app.exec_())

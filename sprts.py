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
        self.coords = [37.618764, 55.759626]
        request = f"https://static-maps.yandex.ru/1.x/?l=sat&ll={self.coords[0]},{self.coords[1]}&spn={self.map_size},{self.map_size}&size=650,450"
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
        if event.key() == Qt.Key_A:
            self.move_map_right()
        if event.key() == Qt.Key_D:
            self.move_map_left()
        if event.key() == Qt.Key_W:
            self.move_map_up()
        if event.key() == Qt.Key_S:
            self.move_map_down()

    def size_map_up(self):
        if self.map_size >= 0.0007:
            if self.map_size >= 0.5:
                self.map_size = round(self.map_size - 0.4, 4)
            elif self.map_size >= 0.1:
                self.map_size = round(self.map_size - 0.08, 4)
            elif self.map_size >= 0.01:
                self.map_size = round(self.map_size - 0.006 if self.map_size < 0.02 else self.map_size - 0.02, 4)
            elif self.map_size >= 0.0045:
                self.map_size = round(self.map_size - 0.004, 4)
            else:
                self.map_size = round(self.map_size - 0.001, 4)
        request = f"https://static-maps.yandex.ru/1.x/?l=sat&ll={self.coords[0]},{self.coords[1]}&spn={self.map_size},{self.map_size}&size=650,450"
        pixmap = QtGui.QPixmap(get_img(request)).scaled(self.w - 30, self.h, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.image.setPixmap(pixmap)

    def size_map_down(self):
        if self.map_size <= 1.5:
            if self.map_size < 0.006:
                self.map_size += 0.002
            elif self.map_size < 0.02:
                self.map_size += 0.009
            elif self.map_size < 0.5:
                self.map_size += 0.1
            else:
                self.map_size += 0.4
            self.map_size = round(self.map_size, 4)
        request = f"https://static-maps.yandex.ru/1.x/?l=sat&ll={self.coords[0]},{self.coords[1]}&spn={self.map_size},{self.map_size}&size=650,450"
        pixmap = QtGui.QPixmap(get_img(request)).scaled(self.w - 30, self.h, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.image.setPixmap(pixmap)

    def move_map_left(self):
        if self.map_size > 0.3:
            self.coords[0] = self.coords[0] + 0.1
        elif self.map_size > 0.1:
            self.coords[0] = self.coords[0] + 0.05
        else:
            self.coords[0] = self.coords[0] + 0.004
        request = f"https://static-maps.yandex.ru/1.x/?l=sat&ll={self.coords[0]},{self.coords[1]}&spn={self.map_size},{self.map_size}&size=650,450"
        pixmap = QtGui.QPixmap(get_img(request)).scaled(self.w - 30, self.h, Qt.IgnoreAspectRatio,
                                                        Qt.FastTransformation)
        self.image.setPixmap(pixmap)

    def move_map_right(self):
        if self.map_size > 0.3:
            self.coords[0] = self.coords[0] - 0.1
        elif self.map_size > 0.1:
            self.coords[0] = self.coords[0] - 0.05
        else:
            self.coords[0] = self.coords[0] - 0.004
        request = f"https://static-maps.yandex.ru/1.x/?l=sat&ll={self.coords[0]},{self.coords[1]}&spn={self.map_size},{self.map_size}&size=650,450"
        pixmap = QtGui.QPixmap(get_img(request)).scaled(self.w - 30, self.h, Qt.IgnoreAspectRatio,
                                                        Qt.FastTransformation)
        self.image.setPixmap(pixmap)

    def move_map_up(self):
        if self.map_size > 0.8:
            self.coords[1] = self.coords[1] + 0.3
        elif self.map_size > 0.3:
            self.coords[1] = self.coords[1] + 0.1
        elif self.map_size > 0.1:
            self.coords[1] = self.coords[1] + 0.05
        else:
            self.coords[1] = self.coords[1] + 0.003
        request = f"https://static-maps.yandex.ru/1.x/?l=sat&ll={self.coords[0]},{self.coords[1]}&spn={self.map_size},{self.map_size}&size=650,450"
        pixmap = QtGui.QPixmap(get_img(request)).scaled(self.w - 30, self.h, Qt.IgnoreAspectRatio,
                                                        Qt.FastTransformation)
        self.image.setPixmap(pixmap)

    def move_map_down(self):
        if self.map_size > 0.8:
            self.coords[1] = self.coords[1] - 0.3
        elif self.map_size > 0.3:
            self.coords[1] = self.coords[1] - 0.1
        elif self.map_size > 0.1:
            self.coords[1] = self.coords[1] - 0.05
        else:
            self.coords[1] = self.coords[1] - 0.003
        request = f"https://static-maps.yandex.ru/1.x/?l=sat&ll={self.coords[0]},{self.coords[1]}&spn={self.map_size},{self.map_size}&size=650,450"
        pixmap = QtGui.QPixmap(get_img(request)).scaled(self.w - 30, self.h, Qt.IgnoreAspectRatio,
                                                        Qt.FastTransformation)
        self.image.setPixmap(pixmap)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    wind = Widget()
    wind.show()
    sys.exit(app.exec_())

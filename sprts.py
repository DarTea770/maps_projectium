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
    if os.path.isfile('map.png'):
        os.remove('map.png')
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file


def get_info(request):
    response = requests.get(request)
    if response:
        json_response = response.json()
        if json_response['response']['GeoObjectCollection']['metaDataProperty']['GeocoderResponseMetaData']['found'] != '0':
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            coords = [float(i) for i in toponym['Point']['pos'].split()]
            return coords


class Widget(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        scr = QtWidgets.QApplication.desktop().screenGeometry()
        self.w, self.h = scr.width(), scr.height()
        self.setGeometry(0, 0, self.w - 30, self.h - 30)

        self.map_size = 0.0016
        self.coords = [37.618764, 55.759626]
        self.layer, self.traffic = 'map', ''

        request = f"https://static-maps.yandex.ru/1.x/?l={self.layer + self.traffic}&ll={self.coords[0]},{self.coords[1]}&spn={self.map_size},{self.map_size}&size=650,450"
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

        self.layer_changer = QtWidgets.QPushButton(self)
        self.layer_changer.setText('Layer')
        self.layer_changer.move(self.w - self.w // 15, self.h // 25)
        self.layer_changer.resize(self.w // 20, self.w // 30)
        self.layer_changer.clicked.connect(self.change_layer)

        self.traffic_changer = QtWidgets.QPushButton(self)
        self.traffic_changer.setText('Traffic')
        self.traffic_changer.move(self.w - 2 * (self.w // 15), self.h // 25)
        self.traffic_changer.resize(self.w // 20, self.w // 30)
        self.traffic_changer.clicked.connect(lambda: self.change_layer(trf=True))

        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.resize(self.w // 9, self.w // 35)
        self.lineEdit.move(self.w // 55, self.w // 45)

        self.done_btn = QtWidgets.QPushButton(self)
        self.done_btn.setText('Search')
        self.done_btn.resize(self.w // 20, self.w // 35)
        self.done_btn.move(self.w // 15 * 2, self.h // 25)
        self.done_btn.pressed.connect(lambda: self.move_to_new_place(self.lineEdit.text()))

        self.clear = QtWidgets.QPushButton(self)
        self.clear.setText('X')
        self.clear.resize(self.w // 35, self.w // 35)
        self.clear.move(self.w // 16 * 3, self.h // 25)
        self.clear.pressed.connect(self.clear_lnedit)

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
        self.update_image()

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
        self.update_image()

    def move_map_left(self):
        if self.map_size > 0.3:
            self.coords[0] = self.coords[0] + 0.1
        elif self.map_size > 0.1:
            self.coords[0] = self.coords[0] + 0.05
        else:
            self.coords[0] = self.coords[0] + 0.004
        self.update_image()

    def move_map_right(self):
        if self.map_size > 0.3:
            self.coords[0] = self.coords[0] - 0.1
        elif self.map_size > 0.1:
            self.coords[0] = self.coords[0] - 0.05
        else:
            self.coords[0] = self.coords[0] - 0.004
        self.update_image()

    def move_map_up(self):
        if self.map_size > 0.8:
            self.coords[1] = self.coords[1] + 0.3
        elif self.map_size > 0.3:
            self.coords[1] = self.coords[1] + 0.1
        elif self.map_size > 0.1:
            self.coords[1] = self.coords[1] + 0.05
        else:
            self.coords[1] = self.coords[1] + 0.003
        self.update_image()

    def move_map_down(self):
        if self.map_size > 0.8:
            self.coords[1] = self.coords[1] - 0.3
        elif self.map_size > 0.3:
            self.coords[1] = self.coords[1] - 0.1
        elif self.map_size > 0.1:
            self.coords[1] = self.coords[1] - 0.05
        else:
            self.coords[1] = self.coords[1] - 0.003
        self.update_image()

    def change_layer(self, trf=False):
        if not trf:
            self.layer = 'sat,skl' if self.layer == 'map' else 'map'
        else:
            self.traffic = ',trf' if self.traffic == '' else ''
        self.update_image()

    def move_to_new_place(self, text):
        req = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={'+'.join(text.split())}&format=json&lang=en_RU"
        coords = get_info(req)
        self.coords = coords if coords is not None else self.coords
        self.map_size = 0.0016
        self.update_image()

    def update_image(self):
        request = f"https://static-maps.yandex.ru/1.x/?l={self.layer + self.traffic}&ll={self.coords[0]},{self.coords[1]}&spn={self.map_size},{self.map_size}&size=650,450"
        self.pixmap = QtGui.QPixmap(get_img(request)).scaled(self.w - 30, self.h, Qt.IgnoreAspectRatio)
        self.image.setPixmap(self.pixmap)

    def clear_lnedit(self):
        if self.lineEdit.text() != '':
            self.lineEdit.clear()
        else:
            self.map_size = 0.0016
            self.coords = [37.618764, 55.759626]
            self.lineEdit.clear()
            self.update_image()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    wind = Widget()
    wind.show()
    sys.exit(app.exec_())

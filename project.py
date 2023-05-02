import sys
import mysql

from secrets import compare_digest
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy, QMainWindow,
    QGridLayout, QLabel
)
from PyQt6.QtCore import Qt
from PyQt6 import QtWidgets
from mysql.connector import connect


# ОСНОВНОЕ ОКНО ПОСЛЕ РЕГИСТРАЦИИ/ВХОДА
class Main(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.resize(500, 500)
        self.setWindowTitle("My App")


# Окно регистрации/входа(отдельное окно)
class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход/Регистрация")
        self.setFixedSize(450, 150)

        layout = QGridLayout()
        self.setLayout(layout)

        # все виджеты окна
        labels = {}
        self.lineEdits = {}

        labels['Username'] = QLabel("Имя")
        labels['Password'] = QLabel("Пароль")
        labels['Username'].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        labels['Password'].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.lineEdits['Username'] = QLineEdit()
        self.lineEdits['Password'] = QLineEdit()
        self.lineEdits['Password'].setEchoMode(QLineEdit.EchoMode.Password)

        layout.addWidget(labels['Username'], 0, 0, 1, 1)
        layout.addWidget(self.lineEdits['Username'], 0, 1, 1, 3)
        layout.addWidget(labels['Password'], 1, 0, 1, 1)
        layout.addWidget(self.lineEdits['Password'], 1, 1, 1, 3)

        # кнопки
        button_sign_up = QPushButton("Зарегестрироваться")
        layout.addWidget(button_sign_up, 2, 2, 1, 1)
        button_sign_up.clicked.connect(self.sign_up)

        button_login = QPushButton("Войти")
        button_login.clicked.connect(self.login)
        layout.addWidget(button_login, 2, 3, 1, 1)

        self.button_see_password = QPushButton("🙈")
        self.button_see_password.clicked.connect(self.show_pass)
        layout.addWidget(self.button_see_password, 1, 4, 1, 1)

        self.status = QLabel('')
        self.status.setStyleSheet("font-size: 20px; color: red;")
        layout.addWidget(self.status, 3, 2, 1, 1)

    def sign_up(self):
        # добавить проверки на пустоту и на пароль!

        username = self.lineEdits['Username'].text()
        password = self.lineEdits['Password'].text()

        db_config = {
            "user": "me",
            "password": "password",
            "host": "193.124.118.138",
            "database": "task_table",
        }
        database = mysql.connector.connect(**db_config)
        cursor = database.cursor(buffered=True)

        cursor.execute(f"SELECT * FROM users WHERE login='{username}'")
        info = cursor.fetchall()

        if len(info) == 0:
            cursor.execute(f"INSERT INTO users(login, password) VALUES('{username}', '{password}')")
            database.commit()
            self.main = Main()
            self.main.show()
            self.close()
        else:
            self.status.setText("Choose another name!")

    def show_pass(self):
        echo_mode = self.lineEdits['Password'].echoMode()

        if echo_mode == QLineEdit.EchoMode.Normal:
            self.button_see_password.setText("🙈")
            self.lineEdits['Password'].setEchoMode(QLineEdit.EchoMode.Password)
        else:
            self.button_see_password.setText("🐵")
            self.lineEdits['Password'].setEchoMode(QLineEdit.EchoMode.Normal)

    def login(self):
        username = self.lineEdits['Username'].text()
        password = self.lineEdits['Password'].text()

        db_config = {
            "user": "me",
            "password": "password",
            "host": "193.124.118.138",
            "database": "task_table",
        }
        database = mysql.connector.connect(**db_config)
        cursor = database.cursor(buffered=True)

        cursor.execute(f"SELECT * FROM users WHERE login='{username}'")
        user_info = cursor.fetchall()

        if len(user_info) == 0:
            self.status.setText("No such user!")
        else:
            if password != user_info[0][1]:
                self.status.setText("Wrong password!")
            else:
                self.main = Main()
                self.main.show()
                self.close()


app = QApplication(sys.argv)
window = Login()
window.show()

app.exec()

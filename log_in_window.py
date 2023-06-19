import sign_up_window
import main_window
import other_classes
import add_table_window

import sys
import mysql

from secrets import compare_digest
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy,
                             QMainWindow, QGridLayout, QLabel, QStatusBar, QCheckBox, QDialog, QStackedWidget
                             )
from PyQt6.QtCore import Qt
from PyQt6 import QtWidgets
from PyQt6.uic import loadUi
from PyQt6.QtCore import QCoreApplication
from mysql.connector import connect


db_config = {
            "user": "me",
            "password": "password",
            "host": "193.124.118.138",
            "database": "tasks_table_copy",
        }
database = mysql.connector.connect(**db_config)
cursor = database.cursor(buffered=True)

class logIn(QDialog):
    def __init__(self):
        super(logIn, self).__init__()
        loadUi("Users_Interfaces/login.ui", self)
        self.setWindowTitle("Вход/Регистрация")

        # кнопка перехода в окно "РЕГИСТРАЦИЯ"
        self.signup.clicked.connect(self.sign_up)

        # кнопка и поле для пароля
        self.show_hide_pass_btn.setText("🙈")
        self.show_hide_pass_btn.clicked.connect(self.show_pass)
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        # кнопка входа
        self.login_btn.clicked.connect(self.log_in)

    def sign_up(self):
        self.close()
        self.signUp = sign_up_window.signUp()
        self.signUp.show()

    def log_in(self):
        self.status.setText("")

        username = self.username.text()
        password = self.password.text()
        global current_user

        cursor.execute(f"SELECT * FROM users WHERE login='{username}'")
        user_info = cursor.fetchall()

        if len(user_info) == 0:
            self.status.setText("Неверный логин или пароль!")
        else:
            if password != user_info[0][2]:
                self.status.setText("Неверный логин или пароль!")
            else:
                self.close()

                # текущий пользователь
                global current_user
                current_user = other_classes.User(username, password)

                self.main = main_window.Main()
                self.main.show()

    def show_pass(self):
        echo_mode = self.password.echoMode()

        if echo_mode == QLineEdit.EchoMode.Normal:
            self.show_hide_pass_btn.setText("🙈")
            self.password.setEchoMode(QLineEdit.EchoMode.Password)
        else:
            self.show_hide_pass_btn.setText("🐵")
            self.password.setEchoMode(QLineEdit.EchoMode.Normal)

# функция, которая возвращает текущего пользователя
def curr():
    return current_user
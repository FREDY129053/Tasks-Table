import log_in_window
import main_window

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

class signUp(QDialog):
    def __init__(self):
        super(signUp, self).__init__()
        loadUi("Users_Interfaces/signup.ui", self)
        self.setWindowTitle("Вход/Регистрация")

        # кнопка перехода в окно "ВХОД"
        self.login.clicked.connect(self.log_in)

        # кнопка и поле для пароля
        self.show_hide_pass_btn.setText("🙈")
        self.show_hide_pass_btn.clicked.connect(self.show_pass)
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        # кнопка и поле для подтверждения пароля
        self.show_hide_pass_btn_2.setText("🙈")
        self.show_hide_pass_btn_2.clicked.connect(self.show_pass_2)
        self.confirm_password.setEchoMode(QLineEdit.EchoMode.Password)

        # кнопка регистрации
        self.registration_btn.clicked.connect(self.sign_up)

    def sign_up(self):
        # добавить проверки на пустоту и на пароль!

        username = self.username.text()
        password = self.password.text()
        confirm_password = self.confirm_password.text()

        # count_of_spec_symb = password.count('~', '!','@','#','$','%','^','&','*','(',')','+','`', ';',':','<','>','/','\\',''|',')
        # print(count_of_spec_symb)

        # роверка на пустоту
        # if username == "" or password == "" or confirm_password == "":
        #     self.status.setText("Заполните все поля!")
        if compare_digest(password, confirm_password):
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

                self.main = main_window.Main()
                self.main.show()
            else:
                self.status.setText("Данное имя занято!")
        else:
            self.status.setText("Пароли не совпадают!")

    def log_in(self):
        self.close()
        self.logIn = log_in_window.logIn()
        self.logIn.show()

    def show_pass(self):
        echo_mode = self.password.echoMode()

        if echo_mode == QLineEdit.EchoMode.Normal:
            self.show_hide_pass_btn.setText("🙈")
            self.password.setEchoMode(QLineEdit.EchoMode.Password)
        else:
            self.show_hide_pass_btn.setText("🐵")
            self.password.setEchoMode(QLineEdit.EchoMode.Normal)

    def show_pass_2(self):
        echo_mode = self.confirm_password.echoMode()

        if echo_mode == QLineEdit.EchoMode.Normal:
            self.show_hide_pass_btn_2.setText("🙈")
            self.confirm_password.setEchoMode(QLineEdit.EchoMode.Password)
        else:
            self.show_hide_pass_btn_2.setText("🐵")
            self.confirm_password.setEchoMode(QLineEdit.EchoMode.Normal)

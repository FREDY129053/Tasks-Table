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


# ОСНОВНОЕ ОКНО ПОСЛЕ РЕГИСТРАЦИИ/ВХОДА
class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(500, 500)
        self.setWindowTitle("My App")

        add_table_action = QAction("Добавить доску", self)
        add_table_action.triggered.connect(self.add_table)

        # Меню
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        file_menu.addAction(add_table_action)

    def add_table(self):
        self.main = AddTable()
        self.main.show()


# Создание новой доски
class AddTable(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(500, 150)
        self.setWindowTitle("Новая доска")

        layout = QGridLayout()
        self.setLayout(layout)

        labels = {}
        self.lineEdits = {}
        self.checkBox = {}

        labels['TableName'] = QLabel("Название доски")
        labels['Public/Private'] = QLabel("Приватная доска")
        labels['Coauthors'] = QLabel("Соавторы (через запятую)")

        self.lineEdits['TableName'] = QLineEdit()
        self.lineEdits['Coauthors'] = QLineEdit()

        self.checkBox['Public/Private'] = QCheckBox()

        layout.addWidget(labels['TableName'], 0, 0, 1, 1)
        layout.addWidget(labels['Coauthors'], 1, 0, 1, 1)
        layout.addWidget(labels['Public/Private'], 2, 0, 1, 1)
        layout.addWidget(self.lineEdits['TableName'], 0, 1, 1, 2)
        layout.addWidget(self.lineEdits['Coauthors'], 1, 1, 1, 2)
        layout.addWidget(self.checkBox['Public/Private'], 2, 1)

        add_table_button = QPushButton("Создать доску")
        layout.addWidget(add_table_button, 3, 2, 1, 1)
        add_table_button.clicked.connect(self.add_table)

        self.status = QLabel('')
        self.status.setStyleSheet("font-size: 20px; color: red;")
        layout.addWidget(self.status, 4, 2, 1, 1)

    def add_table(self):
        db_config = {
            "user": "me",
            "password": "password",
            "host": "193.124.118.138",
            "database": "task_table",
        }
        database = mysql.connector.connect(**db_config)
        cursor = database.cursor(buffered=True)

        table_name = self.lineEdits['TableName'].text()
        coauthors = self.lineEdits['Coauthors'].text().split(', ')
        public_private = self.checkBox['Public/Private'].checkState()

        # Проверка на наличие введенных соавторов в бд
        is_wrong_coauthor = False
        for i in coauthors:
            cursor.execute(f"SELECT * FROM users WHERE login='{i}'")
            user_info = cursor.fetchall()
            if len(user_info) == 0:
                self.status.setText(f"Пользователь \"{i}\" не найден")
                is_wrong_coauthor = True

        if len(table_name) == 0:
            self.status.setText("Введите название доски")
        elif is_wrong_coauthor == False:
            print(table_name)
            print(coauthors)
            print(public_private)
            self.close()

        layout = QGridLayout()
        self.setLayout(layout)

        button_ = QPushButton("Зарегестрироваться")
        layout.addWidget(button_, 2, 2, 1, 1)

        cont = QWidget()
        cont.setLayout(layout)

        self.setCentralWidget(cont)


# Окно регистрации/входа(отдельное окно)
class signUp(QDialog):
    def __init__(self):
        super(signUp, self).__init__()
        loadUi("signup.ui", self)
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

                self.main = Main()
                self.main.show()
            else:
                self.status.setText("Данное имя занято!")
        else:
            self.status.setText("Пароли не совпадают!")

    def log_in(self):
        self.close()
        self.logIn = logIn()
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


class logIn(QDialog):
    def __init__(self):
        super(logIn, self).__init__()
        loadUi("login.ui", self)
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
        self.signUp = signUp()
        self.signUp.show()

    def log_in(self):
        username = self.username.text()
        password = self.password.text()

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
                self.close()
                self.main = Main()
                self.main.show()


    def show_pass(self):
        echo_mode = self.password.echoMode()

        if echo_mode == QLineEdit.EchoMode.Normal:
            self.show_hide_pass_btn.setText("🙈")
            self.password.setEchoMode(QLineEdit.EchoMode.Password)
        else:
            self.show_hide_pass_btn.setText("🐵")
            self.password.setEchoMode(QLineEdit.EchoMode.Normal)


app = QApplication(sys.argv)
window = logIn()
# widget = QStackedWidget()
# widget.addWidget(window)
# widget.setFixedSize(500, 500)
# widget.show()
window.show()

app.exec()

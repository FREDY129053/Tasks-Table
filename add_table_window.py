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
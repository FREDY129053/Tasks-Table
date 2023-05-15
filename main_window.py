import add_table_window

import sys
import mysql

from secrets import compare_digest
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy,
                             QMainWindow, QGridLayout, QLabel, QStatusBar, QCheckBox, QDialog, QStackedWidget,
                             QTableWidget, QScrollArea
                             )
from PyQt6.QtCore import Qt
from PyQt6 import QtWidgets
from PyQt6.uic import loadUi
from PyQt6.QtCore import QCoreApplication
from mysql.connector import connect


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        loadUi("Users_Interfaces/main_window.ui", self)

        self.setWindowTitle("Main")

        btn = self.findChild(QPushButton, 'add_table_btn')
        self.add_table_btn.clicked.connect(self.add_table)

        table = self.findChild(QTableWidget, 'tableWidget')
        scroll_area = self.findChild(QScrollArea, 'scrollArea')

        parent = scroll_area.parentWidget()
        btn.move(650, 513)
        btn.setParent(parent)

        scroll_layout = QVBoxLayout()
        scroll_widget = QWidget()

        for _ in range(100):
            new = QTableWidget()
            name = QLabel()
            name.setText("TABLES")
            scroll_layout.addWidget(name)
            new.setFixedWidth(740)
            new.setFixedHeight(300)
            new.setColumnCount(3)
            new.setHorizontalHeaderLabels(['Надо сделать', 'В процессе', 'Готово!'])
            self.load_data(new)

            scroll_layout.addWidget(new)

            scroll_widget.setLayout(scroll_layout)
            scroll_area.setWidget(scroll_widget)

            # new.setGeometry(table.geometry().x(), table.geometry().y() + (50 + table.height()) * i, table.width(), table.height())
            # new.setParent(self)

    # заполнение таблицы данными
    def load_data(self, table):
        tasks = [{"name": "Посрать", "age": "Покупка туалетки", "address": "Срать"},
                 {"name": "Mark", "age": "18", "address": "Alabama"},
                 {"name": "Посрать", "age": "Покупка туалетки", "address": ""},
                 {"name": "Посрать", "age": "Покупка туалетки", "address": ""},
                 {"name": "Посрать", "age": "Покупка туалетки", "address": "Обосраться"},
                 {"name": "Посрать", "age": "Покупка туалетки", "address": ""},
                 {"name": "Посрать", "age": "Покупка туалетки", "address": "Отложить кучу"},
                 {"name": "Посрать", "age": "Покупка туалетки", "address": ""},
                 {"name": "Посрать", "age": "Покупка туалетки", "address": ""},
                 {"name": "Посрать", "age": "Покупка туалетки", "address": "Надристать"}]
        row = 0
        table.setRowCount(len(tasks))

        for task in tasks:
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(task["name"]))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(task["age"]))
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(task["address"]))
            row += 1

    def add_table(self):
        self.main = add_table_window.AddTable()
        self.main.show()

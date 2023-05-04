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

class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        loadUi("Users_Interfaces/main_window.ui", self)

        self.setWindowTitle("Main")

        self.add_table_btn.clicked.connect(self.add_table)

    def add_table(self):
        self.main = add_table_window.AddTable()
        self.main.show()

    # def __init__(self):
    #     super().__init__()
    #
    #     self.resize(500, 500)
    #     self.setWindowTitle("My App")
    #
    #     add_table_action = QAction("Добавить доску", self)
    #     add_table_action.triggered.connect(self.add_table)
    #
    #     # Меню
    #     menubar = self.menuBar()
    #     file_menu = menubar.addMenu("File")
    #     file_menu.addAction(add_table_action)
    #
    # def add_table(self):
    #     self.main = add_table_window.AddTable()
    #     self.main.show()


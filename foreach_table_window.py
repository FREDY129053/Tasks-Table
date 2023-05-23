import sys
import mysql
import other_classes

# эти два класса ВАЖНЫ, иначе сломается (хз почему)
import log_in_window
import sign_up_window
#

from log_in_window import *
from sign_up_window import *
from secrets import compare_digest
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy,
                             QMainWindow, QGridLayout, QLabel, QStatusBar, QCheckBox, QDialog, QStackedWidget,
                             QTableWidget
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
    "database": "task_table",
}
database = mysql.connector.connect(**db_config)
cursor = database.cursor(buffered=True)


class EachTable(QWidget):
    def __init__(self, window_title):
        super(EachTable, self).__init__()
        loadUi("Users_Interfaces/tables_widget.ui", self)
        self.setWindowTitle(window_title)

        name = self.findChild(QLabel, 'label_2')
        author = self.findChild(QLabel, 'label')
        coauthor = self.findChild(QLabel, 'label_3')

        name.setText(self.windowTitle())

        cursor.execute(f"SELECT author_login FROM tables WHERE table_name = '{self.windowTitle()}'")
        author_from_db = cursor.fetchone()
        author.setText(author_from_db[0])

        cursor.execute(f"SELECT coauthors_login FROM tables WHERE table_name = '{self.windowTitle()}'")
        coauthors_from_db = cursor.fetchone()
        coauthor.setText(coauthors_from_db[0])

        # self.add_column_btn.clicked.connect(self.add_column)

        # table = self.findChild(QTableWidget)
        # print(self.windowTitle())
        # cursor.execute(f"SELECT size_of_table FROM tables WHERE table_name = '{self.windowTitle()}'")
        # size_of_current_table = cursor.fetchall()
        # print(size_of_current_table)

    def add_column(self):
        cursor.execute(f"UPDATE tables SET size_of_table = size_of_table + 1 WHERE table_name = '{self.windowTitle()}'")
        database.commit()

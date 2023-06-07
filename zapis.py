import sys
import mysql

import add_coauthors_window
import other_classes
import add_column
import add_note

# эти два класса ВАЖНЫ, иначе сломается (хз почему)
import log_in_window
import sign_up_window
#

from log_in_window import *
from sign_up_window import *
from secrets import compare_digest
from PyQt6.QtGui import QAction, QStandardItemModel, QStandardItem, QPixmap
from PyQt6.QtWidgets import (QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy,
                             QMainWindow, QGridLayout, QLabel, QStatusBar, QCheckBox, QDialog, QStackedWidget,
                             QTableWidget, QHeaderView, QTableWidgetItem, QColumnView, QTableView, QScrollArea,
                             QSpacerItem
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


class EachNote(QWidget):
    def __init__(self, window_title):
        super(EachNote, self).__init__()
        loadUi("Users_Interfaces/note.ui", self)
        self.setWindowTitle(window_title)
        print("\nOk")

        cursor.execute(f"SELECT author, text FROM columns WHERE name = '{window_title}'")
        info_from_db = cursor.fetchall()[0]
        print(info_from_db)

        author, description = info_from_db

        self.author.setText(author)
        self.author_2.setText(self.windowTitle())
        self.label_4.setText(description)

        if author is None or author == '':
            self.author.setText("Никто...")
        if description is None or description == '':
            self.label_4.setText("Ничего...")

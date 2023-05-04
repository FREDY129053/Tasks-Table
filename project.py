import log_in_window

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = log_in_window.logIn()
    # widget = QStackedWidget()
    # widget.addWidget(window)
    # widget.setFixedSize(500, 500)
    # widget.show()
    window.show()

    app.exec()

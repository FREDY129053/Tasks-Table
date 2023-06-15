import sys
import mysql
import other_classes

# эти два класса ВАЖНЫ, иначе сломается (хз почему)
import log_in_window
import sign_up_window
#

from log_in_window import *
from sign_up_window import *
from PyQt6.QtWidgets import QWidget, QFileDialog
from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi
from mysql.connector import connect

db_config = {
    "user": "me",
    "password": "password",
    "host": "193.124.118.138",
    "database": "tasks_table_copy",
}
database = mysql.connector.connect(**db_config)
cursor = database.cursor(buffered=True)


class AddTable(QWidget):
    def __init__(self):
        super(AddTable, self).__init__()
        loadUi("Users_Interfaces/add_table.ui", self)
        self.setWindowTitle("Новая доска")

        self.add_file.clicked.connect(self.add_back)

        self.add_table_btn.clicked.connect(self.add_table)

    def add_back(self):
        global file_path

        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Image Files (*.png *.jpg *.bmp)")
        file_path, _ = file_dialog.getOpenFileName(self, "Выберите изображение", "", "Image Files (*.png *.jpg *.bmp)")

    def add_table(self):
        global is_wrong_coauthor

        table_name = self.name.text()
        author = sign_up_window.curr() if sign_up_window.curr() is not None else log_in_window.curr()
        # coauthors = self.coauthors.text().split(', ')

        # 1 - приватная, 0 - публичная
        table_type = 0 if str(self.table_type.checkState()) == str(Qt.CheckState.Unchecked) else 1

        cursor.execute(f"SELECT id FROM users WHERE login = '{author.username}'")
        author_id = int(cursor.fetchone()[0])
        print(author_id)

        # Проверка на наличие введенных соавторов в бд
        # if len(coauthors) == 0:
        #     pass
        # else:
        #     is_wrong_coauthor = False
        #     for i in coauthors:
        #         cursor.execute(f"SELECT * FROM users WHERE login='{i}'")
        #         user_info = cursor.fetchall()
        #         if len(user_info) == 0:
        #             self.status.setText(f"Пользователь \"{i}\" не найден")
        #             is_wrong_coauthor = True

        if len(table_name) == 0:
            self.status_2.setText("Введите название доски!")
        else:
            cursor.execute(
                f"INSERT INTO board(name, author_id, status) VALUES('{table_name}', {author_id}, {table_type})")
            database.commit()
            self.close()

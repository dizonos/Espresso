import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5 import uic


class Coffee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect('coffee.db')
        self.cur = self.con.cursor()
        self.loadtable()

    def loadtable(self):
        # ['id', 'grade', 'roast degree', 'milled', 'taste description', 'price', 'size']
        header = self.cur.execute('pragma table_info(coffee)').fetchall()
        header = [i[1] for i in header]
        self.tableWidget.setColumnCount(len(header))
        self.tableWidget.setHorizontalHeaderLabels(header)
        self.tableWidget.setRowCount(0)
        content = self.cur.execute('SELECT * FROM coffee').fetchall()
        for i, row in enumerate(content):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                item = elem
                if j == 1:
                    grade = self.cur.execute("SELECT title FROM grade WHERE id = ?", (elem,)).fetchall()
                    item = grade[0][0]
                elif j == 2:
                    roast = self.cur.execute("SELECT title FROM roast_degree WHERE id = ?", (elem,)).fetchall()
                    item = roast[0][0]
                elif j == 3:
                    item = 'молотый' if elem == 1 else 'в зернах'
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(item)))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Coffee()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
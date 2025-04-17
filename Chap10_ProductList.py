import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5 import uic 
import sqlite3
import os.path 

class ProductDB:
    def __init__(self, db_path="ProductList.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Price INTEGER NOT NULL
            );
        """)
        self.conn.commit()

    def insert(self, name, price):
        self.cursor.execute("INSERT INTO Products (Name, Price) VALUES (?, ?);", (name, price))
        self.conn.commit()

    def update(self, prod_id, name, price):
        self.cursor.execute("UPDATE Products SET Name=?, Price=? WHERE id=?;", (name, price, prod_id))
        self.conn.commit()

    def delete(self, prod_id):
        self.cursor.execute("DELETE FROM Products WHERE id=?;", (prod_id,))
        self.conn.commit()

    def fetch_all(self):
        self.cursor.execute("SELECT * FROM Products ORDER BY id ASC;")
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

#화면 로딩 
form_class = uic.loadUiType("ProductList.ui")[0]

class DemoForm(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.db = ProductDB()

        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["제품ID", "제품명", "가격"])
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 100)
        self.tableWidget.setTabKeyNavigation(False)

        self.prodID.returnPressed.connect(lambda: self.focusNextChild())
        self.prodName.returnPressed.connect(lambda: self.focusNextChild())
        self.prodPrice.returnPressed.connect(lambda: self.focusNextChild())

        self.tableWidget.doubleClicked.connect(self.doubleClick)

        self.getProduct()  # 초기 데이터 로딩

    def addProduct(self):
        name = self.prodName.text()
        price = self.prodPrice.text()
        if not name or not price.isdigit():
            QMessageBox.warning(self, "오류", "유효한 제품명과 가격을 입력하세요.")
            return
        self.db.insert(name, int(price))
        self.getProduct()

    def updateProduct(self):
        prod_id = self.prodID.text()
        name = self.prodName.text()
        price = self.prodPrice.text()
        if not (prod_id.isdigit() and price.isdigit()):
            QMessageBox.warning(self, "오류", "유효한 ID와 가격을 입력하세요.")
            return
        self.db.update(int(prod_id), name, int(price))
        self.getProduct()

    def removeProduct(self):
        prod_id = self.prodID.text()
        if not prod_id.isdigit():
            QMessageBox.warning(self, "오류", "올바른 ID를 입력하세요.")
            return
        self.db.delete(int(prod_id))
        self.getProduct()

    def getProduct(self):
        products = self.db.fetch_all()
        self.tableWidget.setRowCount(len(products))
        self.tableWidget.clearContents()
        for row, item in enumerate(products):
            id_item = QTableWidgetItem(str(item[0]))
            id_item.setTextAlignment(Qt.AlignRight)
            name_item = QTableWidgetItem(item[1])
            price_item = QTableWidgetItem(str(item[2]))
            price_item.setTextAlignment(Qt.AlignRight)

            self.tableWidget.setItem(row, 0, id_item)
            self.tableWidget.setItem(row, 1, name_item)
            self.tableWidget.setItem(row, 2, price_item)

    def doubleClick(self):
        row = self.tableWidget.currentRow()
        self.prodID.setText(self.tableWidget.item(row, 0).text())
        self.prodName.setText(self.tableWidget.item(row, 1).text())
        self.prodPrice.setText(self.tableWidget.item(row, 2).text())

    def closeEvent(self, event):
        self.db.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demoForm = DemoForm()
    demoForm.show()
    app.exec_()





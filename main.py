import sys,os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sqlite3
from PIL import Image

con = sqlite3.connect('phone_book.db')
cur = con.cursor()
defaultImg = "store.png"
store_phone = None
close_trigger = None
gid = None
gmenu = None
gprice = None


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("전화번호부")
        self.setGeometry(750,380,300,300)
        self.UI()
        self.show()

    def UI(self):
        self.mainDesign()
        self.layouts()
        self.getStore()

    def mainDesign(self):

        self.title = QLabel("전화번호부")
        self.title.setAlignment(Qt.AlignCenter)
        self.store_list = QListWidget()
        self.store_list.doubleClicked.connect(self.store_detail)

        self.addbtn = QPushButton("추가")
        self.addbtn.clicked.connect(self.store_add)
        self.updatebtn = QPushButton("변경")
        self.updatebtn.clicked.connect(self.store_update)
        self.deletebtn = QPushButton("삭제")
        self.deletebtn.clicked.connect(self.store_delete)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topbox = QVBoxLayout()
        self.midbox = QHBoxLayout()
        self.bottombox = QHBoxLayout()

        self.topbox.addWidget(self.title)
        self.midbox.addStretch(1)
        self.midbox.addWidget(self.store_list)
        self.midbox.addStretch(1)
        self.bottombox.addStretch(1)
        self.bottombox.addWidget(self.addbtn)
        self.bottombox.addSpacing(10)
        self.bottombox.addWidget(self.updatebtn)
        self.bottombox.addSpacing(10)
        self.bottombox.addWidget(self.deletebtn)
        self.bottombox.addStretch(1)

        self.mainLayout.addSpacing(10)
        self.mainLayout.addLayout(self.topbox)
        self.mainLayout.addSpacing(10)
        self.mainLayout.addLayout(self.midbox)
        self.mainLayout.addSpacing(10)
        self.mainLayout.addLayout(self.bottombox)
        self.mainLayout.addSpacing(10)

        self.setLayout(self.mainLayout)

    def store_detail(self):
        global store_phone

        store = self.store_list.currentItem().text()
        store_phone = store.split(" ")[1]

        self.gotodetail=Store_Detail()
        self.close()

    def store_add(self):
        self.gotoadd = Store_add()
        self.close()

    def store_update(self):
        global store_phone

        if self.store_list.selectedItems():
            store = self.store_list.currentItem().text()
            store_phone = store.split(" ")[1]
            self.gotoupdate = Store_update()
            self.close()

        else:
            QMessageBox.information(self, "경고!!!", "변경을 위한 매장을 선택해주세요.")

    def store_delete(self):

        if self.store_list.selectedItems():
            store = str(self.store_list.currentItem().text().split(" ")[1])
            mbox = QMessageBox()
            mbox.setIcon(QMessageBox.Question)
            mbox.setWindowTitle("경고")
            mbox.setText("정말로 삭제하시겠습니까?")
            mbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            mboxY = mbox.button(QMessageBox.Yes)
            mboxY.setText("네")
            mboxN = mbox.button(QMessageBox.No)
            mboxN.setText("아니요")
            mbox.exec_()
            if mbox.clickedButton() == mboxY:
                try:
                    query = 'DELETE FROM phone_book WHERE phone = ?'
                    cur.execute(query, (store,))
                    con.commit()
                    QMessageBox.information(self, "알림", "삭제되었습니다.")
                    self.close()
                    self.main = Window()
                except:
                    QMessageBox.information(self, "경고", "삭제되지 않았습니다.")
        else:
            QMessageBox.information(self, "경고!!!", "삭제를 위한 매장을 선택해주세요.")

    def getStore(self):
        query = "SELECT store, phone FROM phone_book"
        stores = cur.execute(query).fetchall()
        for store in stores:
            self.store_list.addItem(store[0] + " " + store[1])


class Store_add(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("추가하기")
        self.setGeometry(750, 380, 220, 250)
        self.UI()
        self.show()

    def UI(self):
        self.mainDesign()
        self.layouts()

    def closeEvent(self, QCloseEvent):
        self.main=Window()

    def mainDesign(self):

        self.title = QLabel("매장정보 추가")
        self.title.setAlignment(Qt.AlignCenter)
        self.name = QLabel("매장명 :")
        self.nameEntry = QLineEdit()
        self.phone = QLabel("연락처 :")
        self.phoneEntry = QLineEdit()
        self.img = QLabel("이미지 :")
        self.imgEntry = QPushButton("불러오기")
        self.imgEntry.clicked.connect(self.uploadImage)
        self.confirm=QPushButton("추가하기")
        self.confirm.clicked.connect(self.addStore)

    def layouts(self):

        self.mainLayout = QVBoxLayout()
        self.entryLayout = QFormLayout()

        self.entryLayout.addRow(self.name, self.nameEntry)
        self.entryLayout.addRow(self.phone, self.phoneEntry)
        self.entryLayout.addRow(self.img, self.imgEntry)

        self.mainLayout.addStretch(2)
        self.mainLayout.addWidget(self.title)
        self.mainLayout.addStretch(3)
        self.mainLayout.addLayout(self.entryLayout)
        self.mainLayout.addStretch(2)
        self.mainLayout.addWidget(self.confirm, alignment=Qt.AlignCenter)
        self.mainLayout.addStretch(3)
        self.mainLayout.setContentsMargins(20,0,20,0)

        self.confirm.setFixedSize(100,30)
        self.confirm.setStyleSheet("background-color: orange")
        self.entryLayout.setSpacing(10)

        self.setLayout(self.mainLayout)

    def uploadImage(self):
        global defaultImg
        size =(128,128)
        self.fileName, ok = QFileDialog.getOpenFileName(self, '이미지 불러오기', '', 'Image Files (*.jpg *.png)')

        if ok:
            defaultImg = os.path.basename(self.fileName)
            img = Image.open(self.fileName)
            img = img.resize(size)
            img.save("images/{}".format(defaultImg))

    def addStore(self):
        global defaultImg
        name = self.nameEntry.text()
        phone = self.phoneEntry.text()
        img = defaultImg


        if (name and phone !=""):
            try:
                query = "INSERT INTO phone_book (store, phone, img) VALUES(?,?,?)"
                cur.execute(query,(name,phone,img))
                con.commit()
                QMessageBox.information(self,"안내","매장정보가 추가되었습니다.")
                self.close()
                self.main=Window()
            except:
                QMessageBox.information(self,"경고","매장정보가 추가되지 않았습니다.")
        else:
            QMessageBox.information(self,"경고","빈칸을 채워주세요.")


class Store_update(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("변경하기")
        self.setGeometry(750, 380, 220, 250)
        self.UI()
        self.show()

    def UI(self):
        self.mainDesign()
        self.layouts()

    def closeEvent(self, QCloseEvent):
        self.main=Window()

    def mainDesign(self):
        global store_phone
        query = "SELECT * FROM phone_book WHERE phone = ?  "
        stored_data = cur.execute(query, (store_phone,)).fetchone()
        display_store = stored_data[1]
        display_phone = stored_data[2]

        self.title = QLabel("매장정보 변경")
        self.title.setAlignment(Qt.AlignCenter)
        self.name = QLabel("매장명 :")
        self.nameEntry = QLineEdit(display_store)
        self.phone = QLabel("연락처 :")
        self.phoneEntry = QLineEdit(display_phone)
        self.img = QLabel("이미지 :")
        self.imgEntry = QPushButton("불러오기")
        self.imgEntry.clicked.connect(self.uploadImage)
        self.confirm=QPushButton("변경하기")
        self.confirm.clicked.connect(self.updateStore)

        self.title.font(self)

    def layouts(self):

        self.mainLayout = QVBoxLayout()
        self.entryLayout = QFormLayout()

        self.entryLayout.addRow(self.name, self.nameEntry)
        self.entryLayout.addRow(self.phone, self.phoneEntry)
        self.entryLayout.addRow(self.img, self.imgEntry)

        self.mainLayout.addStretch(2)
        self.mainLayout.addWidget(self.title)
        self.mainLayout.addStretch(3)
        self.mainLayout.addLayout(self.entryLayout)
        self.mainLayout.addStretch(2)
        self.mainLayout.addWidget(self.confirm, alignment=Qt.AlignCenter)
        self.mainLayout.addStretch(3)
        self.mainLayout.setContentsMargins(20,0,20,0)

        self.confirm.setFixedSize(100,30)
        self.confirm.setStyleSheet("background-color: orange")
        self.entryLayout.setSpacing(10)

        self.setLayout(self.mainLayout)

    def uploadImage(self):
        global defaultImg
        size =(128,128)
        self.fileName, ok = QFileDialog.getOpenFileName(self, '이미지 불러오기', '', 'Image Files (*.jpg *.png)')

        if ok:
            defaultImg = os.path.basename(self.fileName)
            img = Image.open(self.fileName)
            img = img.resize(size)
            img.save("images/{}".format(defaultImg))

    def updateStore(self):
        global store_phone
        global defaultImg

        name = self.nameEntry.text()
        phone = self.phoneEntry.text()
        img = defaultImg

        if (name and phone !=""):
            try:
                query = "UPDATE phone_book SET store = ?, phone = ?, img = ? WHERE phone = ?"
                cur.execute(query,(name,phone,img,store_phone))
                con.commit()
                QMessageBox.information(self,"안내","매장정보가 변경되었습니다.")
                self.close()
                self.main=Window()
            except:
                QMessageBox.information(self,"경고","매장정보가 변경되지 않았습니다.")
        else:
            QMessageBox.information(self,"경고","빈칸을 채워주세요.")


class Store_Detail(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("매장정보")
        self.setGeometry(750, 380, 300, 300)
        self.UI()
        self.show()

        global close_trigger
        close_trigger = 0

    def UI(self):
        self.mainDesign()
        self.layouts()
        self.font()
        self.displayRecord()
        self.getMenu()

    def closeEvent(self, QCloseEvent):

        if close_trigger == 0:
            self.main=Window()
        else:
            self.close()

    def mainDesign(self):

        self.title = QLabel("메뉴")
        self.title.setAlignment(Qt.AlignCenter)

        ##### right main layout #####
        self.menu_list = QListWidget()
        self.addButton = QPushButton("추가")
        self.addButton.clicked.connect(self.addMenu)
        self.editButton = QPushButton("변경")
        self.editButton.clicked.connect(self.editMenu)
        self.deleteButton = QPushButton("삭제")
        self.deleteButton.clicked.connect(self.deleteMenu)

    def font(self):
        font = QFont()
        font.setPointSize(15)
        self.title.setFont(font)

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.leftMainLayout = QVBoxLayout()
        self.leftTopLayout = QVBoxLayout()
        self.leftBottomLayout = QFormLayout()
        self.rightMainLayout = QVBoxLayout()
        self.rightBottomLayout = QHBoxLayout()

        self.mainLayout.addSpacing(20)
        self.mainLayout.addLayout(self.leftMainLayout)
        self.mainLayout.addSpacing(20)
        self.mainLayout.addLayout(self.rightMainLayout)

        self.leftMainLayout.addLayout(self.leftTopLayout)
        self.leftMainLayout.addLayout(self.leftBottomLayout)

        self.rightMainLayout.addSpacing(10)
        self.rightMainLayout.addWidget(self.title)
        self.rightMainLayout.addSpacing(10)
        self.rightMainLayout.addWidget(self.menu_list)
        self.rightMainLayout.addSpacing(5)
        self.rightMainLayout.addLayout(self.rightBottomLayout)

        self.rightBottomLayout.addWidget(self.addButton)
        self.rightBottomLayout.addWidget(self.editButton)
        self.rightBottomLayout.addWidget(self.deleteButton)

        self.setLayout(self.mainLayout)

    def displayRecord(self):

        global store_phone

        query ="SELECT * FROM phone_book WHERE phone = ?"
        stored_data =  cur.execute(query,(store_phone,)).fetchone()
        display_store = stored_data[1]
        display_number = stored_data[2]
        display_img = stored_data[3]

        self.img = QLabel()
        self.img.setPixmap(QPixmap("images/"+display_img))
        self.name = QLabel(display_store)
        self.number = QLabel(display_number)

        self.leftTopLayout.addSpacing(30)
        self.leftTopLayout.addWidget(self.img)
        self.leftTopLayout.addSpacing(20)

        self.leftBottomLayout.addRow("매장명: ",self.name)
        self.leftBottomLayout.setSpacing(10)
        self.leftBottomLayout.addRow("전화번호: ",self.number)

    def addMenu(self):
        global close_trigger
        close_trigger = 1
        self.gotoadd = AddMenu()
        self.close()

    def editMenu(self):
        try:
            global close_trigger
            global gid
            global gmenu
            global gprice

            gmenu = self.menu_list.currentItem().text().split(" ")[0]
            gprice = self.menu_list.currentItem().text().split(" ")[1]

            query = "SELECT id FROM menus WHERE menu = ? and price = ?"
            gid = cur.execute(query,(gmenu,gprice)).fetchone()[0]

            if self.menu_list.selectedItems():
                close_trigger = 1
                self.gotoedit = EditMenu()
                self.close()
        except:
            QMessageBox.information(self,"경고","변경할 메뉴가 선택되지 않았습니다.")

    def deleteMenu(self):
        global gid
        global gmenu
        global gprice

        gmenu = self.menu_list.currentItem().text().split(" ")[0]
        gprice = self.menu_list.currentItem().text().split(" ")[1]

        query = "SELECT id FROM menus WHERE menu = ? and price = ?"
        gid = cur.execute(query,(gmenu,gprice)).fetchone()[0]

        if self.menu_list.selectedItems():
            mbox = QMessageBox()
            mbox.setIcon(QMessageBox.Question)
            mbox.setWindowTitle("경고")
            mbox.setText("정말로 삭제하시겠습니까?")
            mbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            mboxY = mbox.button(QMessageBox.Yes)
            mboxY.setText("네")
            mboxN = mbox.button(QMessageBox.No)
            mboxN.setText("아니요")
            mbox.exec_()
            if mbox.clickedButton() == mboxY:
                try:
                    query = "DELETE FROM menus WHERE id = ?"
                    cur.execute(query, (gid,))
                    con.commit()
                    QMessageBox.information(self, "알림", "선택한 메뉴가 삭제되었습니다.")
                    self.close()
                    self.main = Store_Detail()
                except:
                    QMessageBox.information(self, "경고", "선택한 메뉴가 삭제되지 않았습니다.")
        else:
            QMessageBox.information(self,"경고","삭제할 메뉴가 선택되지 않았습니다.")


    def getMenu(self):
        global store_phone
        try:
            query = "SELECT menu, price, phone FROM menus"
            menus = cur.execute(query).fetchall()
            for menu in menus:
                print(menu[0])

            if (menus[0][2]) == store_phone:
                for menu in menus:
                    self.menu_list.addItem(menu[0] + " " + menu[1])
        except:
            pass





class AddMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("추가하기")
        self.setGeometry(750, 380, 220, 250)
        self.UI()
        self.show()

    def UI(self):
        self.mainDesign()
        self.layouts()

    def closeEvent(self, QCloseEvent):
        self.main=Store_Detail()

    def mainDesign(self):
        self.title = QLabel("메뉴 추가")
        self.title.setAlignment(Qt.AlignCenter)
        self.menu = QLabel("메뉴명 :")
        self.menuEntry = QLineEdit()
        self.price = QLabel("가격 :")
        self.priceEntry = QLineEdit()
        self.confirm = QPushButton("추가하기")
        self.confirm.clicked.connect(self.addMenu)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.entryLayout = QFormLayout()

        self.entryLayout.addRow(self.menu, self.menuEntry)
        self.entryLayout.addRow(self.price, self.priceEntry)

        self.mainLayout.addStretch(2)
        self.mainLayout.addWidget(self.title)
        self.mainLayout.addStretch(3)
        self.mainLayout.addLayout(self.entryLayout)
        self.mainLayout.addStretch(2)
        self.mainLayout.addWidget(self.confirm, alignment=Qt.AlignCenter)
        self.mainLayout.addStretch(3)
        self.mainLayout.setContentsMargins(20, 0, 20, 0)

        self.confirm.setFixedSize(100, 30)
        self.confirm.setStyleSheet("background-color: orange")
        self.entryLayout.setSpacing(10)

        self.setLayout(self.mainLayout)

    def addMenu(self):

        global store_phone

        self.menu = self.menuEntry.text()
        self.price = self.priceEntry.text()

        if (self.menu and self.price != ""):
            try:
                query = "INSERT INTO menus (menu, price, phone) VALUES(?,?,?)"
                cur.execute(query, (self.menu, self.price, store_phone))
                con.commit()
                QMessageBox.information(self, "안내", "메뉴가 추가되었습니다.")
                self.close()
                self.main = Store_Detail()
            except:
                QMessageBox.information(self, "경고", "메뉴가 추가되지 않았습니다.")
        else:
            QMessageBox.information(self, "경고", "빈칸을 채워주세요.")

class EditMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("변경하기")
        self.setGeometry(750, 380, 220, 250)
        self.UI()
        self.show()

    def UI(self):
        self.mainDesign()
        self.layouts()

    def closeEvent(self, QCloseEvent):
        self.main=Store_Detail()

    def mainDesign(self):

        global gmenu
        global gprice

        self.title = QLabel("메뉴 변경")
        self.title.setAlignment(Qt.AlignCenter)
        self.menu = QLabel("메뉴명 :")
        self.menuEntry = QLineEdit(gmenu)
        self.price = QLabel("가격 :")
        self.priceEntry = QLineEdit(gprice)
        self.confirm = QPushButton("변경하기")
        self.confirm.clicked.connect(self.editMenu)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.entryLayout = QFormLayout()

        self.entryLayout.addRow(self.menu, self.menuEntry)
        self.entryLayout.addRow(self.price, self.priceEntry)

        self.mainLayout.addStretch(2)
        self.mainLayout.addWidget(self.title)
        self.mainLayout.addStretch(3)
        self.mainLayout.addLayout(self.entryLayout)
        self.mainLayout.addStretch(2)
        self.mainLayout.addWidget(self.confirm, alignment=Qt.AlignCenter)
        self.mainLayout.addStretch(3)
        self.mainLayout.setContentsMargins(20, 0, 20, 0)

        self.confirm.setFixedSize(100, 30)
        self.confirm.setStyleSheet("background-color: orange")
        self.entryLayout.setSpacing(10)

        self.setLayout(self.mainLayout)

    def editMenu(self):

        global gid

        self.menu = self.menuEntry.text()
        self.price = self.priceEntry.text()

        if (self.menu and self.price != ""):
            try:
                query = "UPDATE menus SET menu = ?, price =? WHERE id = ?"
                cur.execute(query, (self.menu, self.price, gid))
                con.commit()
                QMessageBox.information(self, "안내", "메뉴가 변경되었습니다.")
                self.close()
                self.main = Store_Detail()
            except:
                QMessageBox.information(self, "경고", "메뉴가 변경되지 않았습니다.")
        else:
            QMessageBox.information(self, "경고", "빈칸을 채워주세요.")



def main():
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())

if __name__ == '__main__':
    main()




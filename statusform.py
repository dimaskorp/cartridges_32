from PySide2.QtCore import (QCoreApplication, QMetaObject, QRect, QSize, Qt)
from PySide2.QtGui import (QIcon, QFont)
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setMinimumSize(QSize(600, 500))
        Dialog.setMaximumSize(QSize(600, 500))
        font = QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)

        self.toolBox_s = QToolBox(Dialog)
        self.toolBox_s.setObjectName("toolBox_m")
        self.toolBox_s.setGeometry(10, 10, 600, 500)
        self.toolBox_s.setFont(font)
        self.toolBox_s.setLayoutDirection(Qt.LeftToRight)

        self.lineEdit_StatusForm = QLineEdit(self.toolBox_s)
        self.lineEdit_StatusForm.setObjectName("lineEdit_StatusForm")
        self.lineEdit_StatusForm.setGeometry(QRect(10, 0, 300, 25))
        self.lineEdit_StatusForm.setFrame(True)
        self.lineEdit_StatusForm.setEchoMode(QLineEdit.Normal)
        self.lineEdit_StatusForm.setClearButtonEnabled(True)

        self.pB_print_StatusForm = QPushButton(self.toolBox_s)
        self.pB_print_StatusForm.setObjectName("pB_print_StatusForm")
        self.pB_print_StatusForm.setGeometry(QRect(400, 0, 150, 25))
        self.pB_print_StatusForm.setFont(font)

        self.pB_add_StatusForm = QPushButton(self.toolBox_s)
        self.pB_add_StatusForm.setObjectName("pB_add_StatusForm")
        self.pB_add_StatusForm.setGeometry(QRect(10, 40, 100, 25))
        icon = QIcon()
        icon.addFile("images/add.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pB_add_StatusForm.setIcon(icon)

        self.pB_edit_StatusForm = QPushButton(self.toolBox_s)
        self.pB_edit_StatusForm.setObjectName("pB_edit_StatusForm")
        self.pB_edit_StatusForm.setGeometry(QRect(110, 40, 100, 25))
        self.pB_edit_StatusForm.setCheckable(True)
        icon1 = QIcon()
        icon1.addFile("images/edit.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pB_edit_StatusForm.setIcon(icon1)

        self.pB_delete_StatusForm = QPushButton(self.toolBox_s)
        self.pB_delete_StatusForm.setObjectName("pB_delete_StatusForm")
        self.pB_delete_StatusForm.setGeometry(QRect(210, 40, 100, 25))
        icon2 = QIcon()
        icon2.addFile("images/delete.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pB_delete_StatusForm.setIcon(icon2)

        self.tableView_StatusForm = QTableView(self.toolBox_s)
        self.tableView_StatusForm.setObjectName("tableView_StatusForm")
        self.tableView_StatusForm.setGeometry(QRect(0, 90, 580, 380))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle("Отделения и статусы")
        Dialog.setWindowIcon(QIcon('images/iconc.jpg'))
        self.pB_print_StatusForm.setText("Печать штрих кода")

    # retranslateUi


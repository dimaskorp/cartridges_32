from PySide2.QtCore import (QCoreApplication, QMetaObject, QRect, QSize, Qt)
from PySide2.QtGui import (QIcon, QFont)
from PySide2.QtWidgets import *

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName("Dialog")
        #Dialog.resize(600, 500)
        Dialog.setMinimumSize(QSize(600, 500))
        Dialog.setMaximumSize(QSize(600, 500))
        font = QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(True)

        self.toolBox_m = QToolBox(Dialog)
        self.toolBox_m.setObjectName("toolBox_m")
        self.toolBox_m.setGeometry(10, 10, 600, 500)
        self.toolBox_m.setFont(font)
        self.toolBox_m.setLayoutDirection(Qt.LeftToRight)

        # self.splitter = QSplitter(Dialog)
        # self.splitter.setObjectName("splitter")
        # self.splitter.setGeometry(QRect(10, 10, 580, 480))
        # self.splitter.setOrientation(Qt.Vertical)

        self.lineEdit_ModelForm = QLineEdit(self.toolBox_m)
        self.lineEdit_ModelForm.setObjectName("lineEdit_ModelForm")
        self.lineEdit_ModelForm.setGeometry(QRect(150, 0, 200, 25))
        self.lineEdit_ModelForm.setFrame(True)
        self.lineEdit_ModelForm.setEchoMode(QLineEdit.Normal)
        self.lineEdit_ModelForm.setClearButtonEnabled(True)




        self.widget = QWidget(self.toolBox_m)
        self.widget.setObjectName("widget")


        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        #self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pB_add_ModelForm = QPushButton(self.widget)
        self.pB_add_ModelForm.setObjectName("pB_add_ModelForm")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pB_add_ModelForm.sizePolicy().hasHeightForWidth())
        self.pB_add_ModelForm.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(u"images/add.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pB_add_ModelForm.setIcon(icon)
        self.horizontalLayout.addWidget(self.pB_add_ModelForm)

        self.pB_edit_ModelForm = QPushButton(self.widget)
        self.pB_edit_ModelForm.setObjectName(u"pB_edit_ModelForm")
        self.pB_edit_ModelForm.setMouseTracking(False)
        self.pB_edit_ModelForm.setTabletTracking(False)
        self.pB_edit_ModelForm.setFocusPolicy(Qt.StrongFocus)
        self.pB_edit_ModelForm.setAutoFillBackground(False)
        icon1 = QIcon()
        icon1.addFile(u"images/edit.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pB_edit_ModelForm.setIcon(icon1)
        self.pB_edit_ModelForm.setCheckable(True)
        self.pB_edit_ModelForm.setChecked(False)
        self.pB_edit_ModelForm.setAutoRepeat(False)
        self.pB_edit_ModelForm.setAutoExclusive(False)
        self.horizontalLayout.addWidget(self.pB_edit_ModelForm)

        self.pB_delete_ModelForm = QPushButton(self.widget)
        self.pB_delete_ModelForm.setObjectName(u"pB_delete_ModelForm")
        icon2 = QIcon()
        icon2.addFile(u"images/delete.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pB_delete_ModelForm.setIcon(icon2)
        self.horizontalLayout.addWidget(self.pB_delete_ModelForm)

        self.tableView_ModelForm = QTableView(self.toolBox_m)
        self.tableView_ModelForm.setObjectName("tableView_ModelForm")

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", "Модели", None))
        Dialog.setWindowIcon(QIcon('images/iconc.jpg'))
        self.pB_add_ModelForm.setText("")
        self.pB_edit_ModelForm.setText("")
        self.pB_delete_ModelForm.setText("")
    # retranslateUi


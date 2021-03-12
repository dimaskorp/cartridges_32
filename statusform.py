from PySide2.QtCore import (QCoreApplication, QMetaObject, QRect, QSize, Qt)
from PySide2.QtGui import (QIcon)
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 510)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(0, 0))
        Dialog.setMaximumSize(QSize(400, 510))
        self.splitter = QSplitter(Dialog)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setGeometry(QRect(10, 20, 381, 481))
        self.splitter.setOrientation(Qt.Vertical)
        self.lineEdit_StatusForm = QLineEdit(self.splitter)
        self.lineEdit_StatusForm.setObjectName(u"lineEdit_StatusForm")
        self.lineEdit_StatusForm.setMaximumSize(QSize(16777215, 25))
        self.splitter.addWidget(self.lineEdit_StatusForm)
        self.widget = QWidget(self.splitter)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.pB_print_StatusForm = QPushButton(self.widget)
        self.pB_print_StatusForm.setObjectName(u"pB_print_StatusForm")

        self.horizontalLayout.addWidget(self.pB_print_StatusForm)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pB_add_StatusForm = QPushButton(self.widget)
        self.pB_add_StatusForm.setObjectName(u"pB_add_StatusForm")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pB_add_StatusForm.sizePolicy().hasHeightForWidth())
        self.pB_add_StatusForm.setSizePolicy(sizePolicy1)
        icon = QIcon()
        icon.addFile(u"images/add.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pB_add_StatusForm.setIcon(icon)

        self.horizontalLayout.addWidget(self.pB_add_StatusForm)

        self.pB_edit_StatusForm = QPushButton(self.widget)
        self.pB_edit_StatusForm.setObjectName(u"pB_edit_StatusForm")
        self.pB_edit_StatusForm.setMouseTracking(False)
        self.pB_edit_StatusForm.setTabletTracking(False)
        self.pB_edit_StatusForm.setFocusPolicy(Qt.StrongFocus)
        self.pB_edit_StatusForm.setAutoFillBackground(False)
        icon1 = QIcon()
        icon1.addFile(u"images/edit.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pB_edit_StatusForm.setIcon(icon1)
        self.pB_edit_StatusForm.setCheckable(True)
        self.pB_edit_StatusForm.setChecked(False)
        self.pB_edit_StatusForm.setAutoRepeat(False)
        self.pB_edit_StatusForm.setAutoExclusive(False)

        self.horizontalLayout.addWidget(self.pB_edit_StatusForm)

        self.pB_delete_StatusForm = QPushButton(self.widget)
        self.pB_delete_StatusForm.setObjectName(u"pB_delete_StatusForm")
        icon2 = QIcon()
        icon2.addFile(u"images/delete.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pB_delete_StatusForm.setIcon(icon2)

        self.horizontalLayout.addWidget(self.pB_delete_StatusForm)

        self.splitter.addWidget(self.widget)
        self.tableView_StatusForm = QTableView(self.splitter)
        self.tableView_StatusForm.setObjectName(u"tableView_StatusForm")
        self.tableView_StatusForm.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.tableView_StatusForm.sizePolicy().hasHeightForWidth())
        self.tableView_StatusForm.setSizePolicy(sizePolicy2)
        self.tableView_StatusForm.setDragDropOverwriteMode(False)
        self.splitter.addWidget(self.tableView_StatusForm)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", "Отделения и статусы", None))
        Dialog.setWindowIcon(QIcon('images/iconc.jpg'))
        self.pB_print_StatusForm.setText(QCoreApplication.translate("Dialog", "Печать штрих кода", None))
        self.pB_add_StatusForm.setText("")
        self.pB_edit_StatusForm.setText("")
        self.pB_delete_StatusForm.setText("")
    # retranslateUi


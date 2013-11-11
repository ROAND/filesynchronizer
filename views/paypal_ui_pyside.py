# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'paypal.ui'
#
# Created: Mon Nov 11 14:02:14 2013
#      by: pyside-uic 0.2.14 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_PaypalDialog(object):
    def setupUi(self, PaypalDialog):
        PaypalDialog.setObjectName("PaypalDialog")
        PaypalDialog.resize(318, 417)
        self.gridLayout_3 = QtGui.QGridLayout(PaypalDialog)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.happyWebView = QtWebKit.QWebView(PaypalDialog)
        self.happyWebView.setUrl(QtCore.QUrl("about:blank"))
        self.happyWebView.setObjectName("happyWebView")
        self.gridLayout_2.addWidget(self.happyWebView, 0, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 5, 0, 1, 1)
        self.label_4 = QtGui.QLabel(PaypalDialog)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 6, 0, 1, 1)
        self.label_3 = QtGui.QLabel(PaypalDialog)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_5 = QtGui.QLabel(PaypalDialog)
        self.label_5.setText("")
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 0, 0, 1, 1)
        self.label = QtGui.QLabel(PaypalDialog)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 1, 0, 1, 1)
        self.happyButton = QtGui.QPushButton(PaypalDialog)
        self.happyButton.setObjectName("happyButton")
        self.gridLayout_3.addWidget(self.happyButton, 8, 0, 1, 1)
        self.label_2 = QtGui.QLabel(PaypalDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 7, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.happySlider = QtGui.QSlider(PaypalDialog)
        self.happySlider.setMinimum(1)
        self.happySlider.setMaximum(10)
        self.happySlider.setOrientation(QtCore.Qt.Horizontal)
        self.happySlider.setObjectName("happySlider")
        self.gridLayout.addWidget(self.happySlider, 0, 0, 1, 1)
        self.happyEdit = QtGui.QLineEdit(PaypalDialog)
        self.happyEdit.setObjectName("happyEdit")
        self.gridLayout.addWidget(self.happyEdit, 0, 2, 1, 1)
        self.label_6 = QtGui.QLabel(PaypalDialog)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 4, 0, 1, 1)

        self.retranslateUi(PaypalDialog)
        QtCore.QMetaObject.connectSlotsByName(PaypalDialog)

    def retranslateUi(self, PaypalDialog):
        PaypalDialog.setWindowTitle(QtGui.QApplication.translate("PaypalDialog", "PayPal", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("PaypalDialog", "10% of the amount you choose will be donated to the rsync project and the rest goes to the developers.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("PaypalDialog", "Here you can show us how much you liked it.", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PaypalDialog", "Did you like SynchroniZeRD? Oh what a stupid question, of course you did (:", None, QtGui.QApplication.UnicodeUTF8))
        self.happyButton.setText(QtGui.QApplication.translate("PaypalDialog", "Make someone happy!", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("PaypalDialog", " Cheers!", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("PaypalDialog", "US$", None, QtGui.QApplication.UnicodeUTF8))

from PySide import QtWebKit

#-*- coding: utf-8 -*-
import sys
import os
import subprocess
from threading import Thread
import socket
from email.mime.text import MIMEText
import smtplib
import paypalrestsdk
from paypalrestsdk import Payment


def backendError():
    print ("You should choose PySide or PyQt4 as a UI-- Example: python synchhronizerd.py -PySide Or: python synchronizerd.py -PyQt4")

if len(sys.argv) == 2:
    if sys.argv[1] == '-PySide':
        # PySide -----------------------------------
        import PySide
        from PySide import QtGui
        from PySide import QtCore
        from PySide.QtCore import Signal as Signal
        from PySide.QtCore import Slot as Slot
        from PySide.QtGui import QMessageBox
        from PySide.QtCore import QThread, QObject
        from PySide.QtWebKit import QWebView
        from views.synchronizerd_ui_pyside import Ui_SyncMain
        from views.feedback_ui_pyside import Ui_FeedbackDialog
        from views.paypal_ui_pyside import Ui_PaypalDialog
        #------------------------------------------
    elif sys.argv[1] == '-PyQt4':
        # PyQt4 ------------------------------------
        import PyQt4
        from PyQt4 import QtGui
        from PyQt4 import QtCore
        from PyQt4.QtGui import QMessageBox
        from PyQt4.QtCore import QThread, QObject
        from PyQt4.QtCore import pyqtSignal as Signal
        from PyQt4.QtCore import pyqtSlot as Slot
        from PyQt4.QtWebKit import QWebView
        from views.synchronizerd_ui import Ui_SyncMain
        from views.feedback_ui import Ui_FeedbackDialog
        from views.paypal_ui import Ui_PaypalDialog
        #------------------------------------------
    else:
        backendError()
        sys.exit()
else:
    backendError()
    sys.exit()

__version__ = '1.0.0'
import platform

dir_from = None
dir_to = None


@Slot(str)
def mBoxExec(message):
    '''Mostra message box error'''
    QMessageBox.critical(None, 'Error!', message, QMessageBox.Ok)


@Slot(str)
def mBoxExecSuccess(message):
    '''Mostra message box sucess'''
    QMessageBox.information(None, 'Sucess!', message, QMessageBox.Ok)


class Communicate(QObject):
    speak = Signal(str)
    mBox = Signal(str)
    mBoxEr = Signal(str)


class EmailSender(Thread):

    def __init__(self, nome, appName, email, mensagem, com):
        Thread.__init__(self)
        self.mensagem = mensagem
        self.appName = appName
        self.email = email
        self.nome = nome
        self.com = com

    def run(self):
        self.sendMail(self.nome, self.appName, self.email, self.mensagem)

    def sendMail(self, nome, appName, email, mensagem):
        try:
            sender = "contato@roandigital.com"
            receivers = ['suporte@roandigital.com']
            message = MIMEText(
                mensagem + os.linesep + "Application: %s" % appName)
            message[
                'Subject'] = "Feedback SynchroniZeRD - %s" % socket.gethostname()
            message['From'] = " %s <%s>" % (nome, email)
            message['To'] = "Suporte <suporte@roandigital.com>"

            conn = smtplib.SMTP("smtp.roandigital.com:587")
            conn.login("suporte@roandigital.com", "erros1234")
            conn.sendmail(sender, receivers, message.as_string())
            conn.quit()
            self.com.mBox.emit(
                'The email was sent with sucess. \n\nThank you for your feedback. \n\nWe hope you enjoy SynchroniZeRD!')
        except Exception as e:
            self.com.mBoxEr.emit(
                'The email was not sent, sorry.\n\n You may want to check your internet connection.')
            print (e)


class CheckProgress(QThread):

    def __init__(self, dir_from, dir_to, some):
        QThread.__init__(self, None)
        box = Communicate()
        box.mBox.connect(mBoxExec)
        try:
            self.processo = subprocess.Popen(
                ["rsync", "-av", "--progress", "--size-only", "%s" %
                 dir_from, "%s" % dir_to], shell=False, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            self.some = some
        except Exception as e:
            box.mBox.emit(
                u'Error invoking rsync, please check if you have rsync installed.\n:= %s' % e.message)
            print (e)

    def run(self):
        self.getProgress()

    def getProgress(self):
        while True:
            out = self.processo.stdout.readline(150)
            if out == '' and self.processo.poll() is not None:
                print ("processo acabou")
                break
            print (out)
            self.some.speak.emit(out)


class Feedback(QtGui.QDialog):

    def __init__(self):
        super(Feedback, self).__init__()
        self.ui = Ui_FeedbackDialog()
        self.ui.setupUi(self)
        self.ui.sendButton.clicked.connect(self.sendMail)
        self.com = Communicate()
        self.com.mBox.connect(mBoxExecSuccess)
        self.com.mBoxEr.connect(mBoxExec)

    def sendMail(self):
        mail = EmailSender(self.ui.nameEdit.text(), 'SynchroniZeRD',
                           self.ui.emailEdit.text(), self.ui.messageEdit.toPlainText(), self.com)
        mail.start()
        mail.join()
        self.close()

class PayPalUI(QtGui.QDialog):

    def __init__(self):
        super(PayPalUI, self).__init__()
        self.ui = Ui_PaypalDialog()
        self.ui.setupUi(self)
        self.ui.happySlider.valueChanged.connect(self.chValue)
        self.ui.happyButton.clicked.connect(self.createPayment)
        img = QtGui.QPixmap('paypal_logo.jpg')
        self.ui.label_5.setPixmap(img)
        self.ui.label_5.setScaledContents(True)
        self.ui.label_5.setFixedSize(300,50)
        self.ui.happyEdit.textChanged.connect(self.chText)
        self.ui.happyEdit.setText('3')
        
    def chValue(self):
        self.ui.happyEdit.setText(str(self.ui.happySlider.value()))

    def chText(self):
        self.ui.happySlider.setValue(float(self.ui.happyEdit.text()))

    def createPayment(self):
        price = self.ui.happyEdit.text()
        paypalrestsdk.configure({
            "mode": "sandbox", # sandbox or live
            "client_id": "ASS1fRDDkhHgMRXFYLJ9J02663eBb1ktC65nEQ6iVKbD4PyJPilbycGv6pxF",
            "client_secret": "EDo-XBCkEY72na40ngY_D6h8r6T2IhfBYtZoHEFV9Rf2sSYtsYDqmhexF3tO" })
        payment = Payment({
  "intent":  "sale",

  # ###Payer
  # A resource representing a Payer that funds a payment
  # Payment Method as 'paypal'
  "payer":  {
    "payment_method":  "paypal" },

  # ###Redirect URLs
  "redirect_urls": {
    "return_url": "http://roandigital.com/",
    "cancel_url": "http://roandigital.com/applications/" },

  # ###Transaction
  # A transaction defines the contract of a
  # payment - what is the payment for and who
  # is fulfilling it.
  "transactions":  [ {

    # ### ItemList
    "item_list": {
      "items": [{
        "name": "synchronizerd",
        "sku": "synchronizerd",
        "price": price,
        "currency": "USD",
        "quantity": 1 }]},

    # ###Amount
    # Let's you specify a payment amount.
    "amount":  {
      "total":  price,
      "currency":  "USD" },
    "description":  "This is the payment transaction for SynchroniZeRD." } ] } )
        if payment.create():
            print("payment created")
            for link in payment.links:
                if link.method=="REDIRECT":
                    red = link.href
                    self.ui.happyWebView.load(red)
        else:
            print('deu merda')


class MainUi(QtGui.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainUi, self).__init__()
        self.ui = Ui_SyncMain()
        self.ui.setupUi(self)
        self.ui.btOpenFrom.clicked.connect(self.fromOpen)
        self.ui.btOpenTo.clicked.connect(self.toOpen)
        self.ui.btSync.clicked.connect(self.sync)
        self.some = Communicate()
        self.some.speak.connect(self.sayWords)
        self.ui.actionOpen_Folder_From.activated.connect(self.fromOpen)
        self.ui.actionOpen_Folder_To.activated.connect(self.toOpen)
        self.ui.action_About.activated.connect(self.aboutBox)
        self.ui.action_License.activated.connect(self.aboutLicense)
        self.ui.actionAbout_Qt.activated.connect(self.aboutBoxQt)
        self.ui.action_Exit.activated.connect(self.exitMenu)
        self.ui.actionSend_Feedback.activated.connect(self.feedback)
        self.ui.actionMake_someone_happy.activated.connect(self.paypalui)

    @Slot(str)
    def sayWords(self, words):
        self.ui.textStatus.append(words)

    def paypalui(self):
        pay = PayPalUI()
        pay.exec_()

    def feedback(self):
        feed = Feedback()
        feed.exec_()

    def aboutBox(self):
        about = QMessageBox.about(self, "About SynchroniZeRD",
        u"""<b>SynchroniZeRD</b> v %s
        <p><b>Copyright (C) 2013</b> Ronnie Andrew.</p>
        <p>
        All rights reserved in accordance with
        GPL v3 or later - NO WARRANTIES!</p>
        <p>This application can be used to synchronize folders using <b>rsync</b> as main feature.</p>
        <p><b>Official Website:</b> <a href='http://roandigital.com/applications/synchronizerd'>Roan Digital</a></p>
        <p><b>Platform: </b>%s</p>
        """ % (__version__, platform.system()))

    def aboutBoxQt(self):
        QMessageBox.aboutQt(self, 'About Qt')
        pass

    def aboutLicense(self):
        try:
            f = open('GNU_HTML')
            license = QtGui.QDialog()
            license.resize(650, 480)
            license.setWindowTitle('SynchroniZeRD License')
            licenseText = QWebView()
            licenseText.setHtml(f.read())
            layout = QtGui.QGridLayout(license)
            layout.addWidget(licenseText)
            license.exec_()
        except:
            QMessageBox.critical(
                self, 'Error', 'Unable to open GNU_HTML License file.')

    def fromOpen(self):
        chosenFromDir = self.getDirectory()
        self.dir_from = chosenFromDir + "/"
        print (self.dir_from)
        self.ui.textFrom.setText(self.dir_from)
        pass

    def toOpen(self):
        chosenToDir = self.getDirectory()
        self.dir_to = chosenToDir + "/"
        print (self.dir_to)
        self.ui.textTo.setText(self.dir_to)
        pass

    def sync(self):
        self.threadProgress = CheckProgress(
            self.dir_from, self.dir_to, self.some)
        self.threadProgress.start()
        pass

    def getDirectory(self):
        dialog = QtGui.QFileDialog()
        dialog.setFileMode(QtGui.QFileDialog.Directory)
        dialog.setOption(QtGui.QFileDialog.ShowDirsOnly)
        return dialog.getExistingDirectory()

    def exitMenu(self):
        self.close()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = MainUi()
    try:
        app.setWindowIcon(QtGui.QIcon('synchronizer-rd.png'))
    except:
        QMessageBox.critical(
            main, 'Error', 'Unable to open icon synchronizer-rd.png')
    main.show()
    sys.exit(app.exec_())

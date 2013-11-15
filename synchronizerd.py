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


def backend_error():
    print(
        "You should choose PySide or PyQt4 as a UI-- Example: python synchhronizerd.py -PySide Or: python synchronizerd.py -PyQt4")

def get_file(desired_file):
    usrpath = os.path.join('/usr/share/synchronizerd/', desired_file)
    try:
        if os.path.exists(desired_file):
            return desired_file
        elif os.path.exists(usrpath):
            return usrpath
    except Exception as ex:
        print(ex)

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
        from PyQt4.QtGui import QMessageBox, QMainWindow
        from PyQt4.QtCore import QThread, QObject
        from PyQt4.QtCore import pyqtSignal as Signal
        from PyQt4.QtCore import pyqtSlot as Slot
        from PyQt4.QtWebKit import QWebView
        from views.synchronizerd_ui import Ui_SyncMain
        from views.feedback_ui import Ui_FeedbackDialog
        from views.paypal_ui import Ui_PaypalDialog
        #------------------------------------------
    else:
        backend_error()
        sys.exit()
else:
    backend_error()
    sys.exit()

__version__ = '1.0.0'
import platform

dir_from = None
dir_to = None


@Slot(str)
def m_box_exec(message):
    """Mostra message box error"""
    QMessageBox.critical(None, 'Error!', message, QMessageBox.Ok)


@Slot(str)
def m_box_exec_success(message):
    """Mostra message box sucess"""
    QMessageBox.information(None, 'Sucess!', message, QMessageBox.Ok)


class Communicate(QObject):
    speak = Signal(str)
    mBox = Signal(str)
    mBoxEr = Signal(str)


class EmailSender(Thread):
    def __init__(self, nome, app_name, email, mensagem, com):
        Thread.__init__(self)
        self.mensagem = mensagem
        self.app_name = app_name
        self.email = email
        self.nome = nome
        self.com = com

    def run(self):
        self.send_mail(self.nome, self.app_name, self.email, self.mensagem)

    def send_mail(self, nome, app_name, email, mensagem):
        try:
            sender = "contato@roandigital.com"
            receivers = ['suporte@roandigital.com']
            message = MIMEText(
                mensagem + os.linesep + "Application: %s" % app_name)
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
            print(e)


class CheckProgress(QThread):
    def __init__(self, dir_from, dir_to, some):
        QThread.__init__(self, None)
        box = Communicate()
        box.mBox.connect(m_box_exec)
        try:
            self.processo = subprocess.Popen(
                ["rsync", "-av", "--progress", "--size-only", "%s" %
                                                              dir_from, "%s" % dir_to], shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            self.some = some
        except Exception as e:
            box.mBox.emit(
                u'Error invoking rsync, please check if you have rsync installed.\n:= %s' % e.message)
            print(e)

    def run(self):
        self.get_progress()

    def get_progress(self):
        while True:
            out = self.processo.stdout.readline(150)
            if out == '' and self.processo.poll() is not None:
                print("processo acabou")
                break
            print(out)
            self.some.speak.emit(out)


class Feedback(QtGui.QDialog):
    def __init__(self):
        super(Feedback, self).__init__()
        self.ui = Ui_FeedbackDialog()
        self.ui.setupUi(self)
        self.ui.sendButton.clicked.connect(self.send_mail)
        self.com = Communicate()
        self.com.mBox.connect(m_box_exec_success)
        self.com.mBoxEr.connect(m_box_exec)

    def send_mail(self):
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
        self.ui.happySlider.valueChanged.connect(self.ch_value)
        self.ui.happyButton.clicked.connect(self.create_payment)
        img = QtGui.QPixmap(get_file('paypal_logo.jpg'))
        self.ui.label_5.setPixmap(img)
        self.ui.label_5.setScaledContents(True)
        self.ui.label_5.setFixedSize(300, 50)
        self.ui.happyEdit.textChanged.connect(self.ch_text)
        self.ui.happyEdit.setText('3')
        self.ui.happyWebView.urlChanged.connect(self.ch_web_view)
        self.ui.happyWebView.loadProgress.connect(self.progress_webview)

    def progress_webview(self, progress):
        self.ui.progressBar.setValue(progress)

    def ch_value(self):
        self.ui.happyEdit.setText(str(self.ui.happySlider.value()))

    def ch_text(self):
        self.ui.happySlider.setValue(float(self.ui.happyEdit.text()))

    def ch_web_view(self):
        url = self.ui.happyWebView.url()
        url_string = url.toString()

        if 'PayerID=' in url_string:
            for s in url_string.split('&'):
                if s.startswith('PayerID='):
                    id = s.strip('PayerID=')
                    if self.payment.execute({"payer_id": id}):
                        m_box_exec_success(
                            'Congratulations, you have made someone happy!')
                    else:
                        m_box_exec(
                            'Sorry, your transaction could not be completed.')

    def create_payment(self):
        price = self.ui.happyEdit.text()
        paypalrestsdk.configure({
            "mode": "sandbox", # sandbox or live
            "client_id": "ASS1fRDDkhHgMRXFYLJ9J02663eBb1ktC65nEQ6iVKbD4PyJPilbycGv6pxF",
            "client_secret": "EDo-XBCkEY72na40ngY_D6h8r6T2IhfBYtZoHEFV9Rf2sSYtsYDqmhexF3tO"})
        self.payment = Payment({
            "intent": "sale",

            # Payer
            # A resource representing a Payer that funds a payment
            # Payment Method as 'paypal'
            "payer": {
                "payment_method": "paypal"},

            # Redirect URLs
            "redirect_urls": {
                "return_url": "http://roandigital.com/applications/synchronizerd/thanks",
                "cancel_url": "http://roandigital.com/applications/synchronizerd/sorry"},

            # Transaction
            # A transaction defines the contract of a
            # payment - what is the payment for and who
            # is fulfilling it.
            "transactions": [{

                                 # ItemList
                                 "item_list": {
                                     "items": [{
                                                   "name": "SynchroniZeRD",
                                                   "sku": "1",
                                                   "price": price,
                                                   "currency": "USD",
                                                   "quantity": 1}]},

                                 # Amount
                                 # Let's you specify a payment amount.
                                 "amount": {
                                     "total": price,
                                     "currency": "USD"},
                                 "description": "This is the payment transaction for SynchroniZeRD."}]})
        if self.payment.create():
            m_box_exec_success(
                'Your payment was created, redirecting to paypal for authorization.')
            for link in self.payment.links:
                if link.method == "REDIRECT":
                    red = link.href
                    self.ui.happyWebView.load(red)
                    self.setMinimumSize(1024, 600)

        else:
            print('error')


class MainUi(QtGui.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainUi, self).__init__()
        self.ui = Ui_SyncMain()
        self.ui.setupUi(self)
        self.ui.btOpenFrom.clicked.connect(self.from_open)
        self.ui.btOpenTo.clicked.connect(self.to_open)
        self.ui.btSync.clicked.connect(self.sync)
        self.some = Communicate()
        self.some.speak.connect(self.say_words)
        self.ui.actionOpen_Folder_From.activated.connect(self.from_open)
        self.ui.actionOpen_Folder_To.activated.connect(self.to_open)
        self.ui.action_About.activated.connect(self.about_box)
        self.ui.action_License.activated.connect(self.about_license)
        self.ui.actionAbout_Qt.activated.connect(self.about_box_qt)
        self.ui.action_Exit.activated.connect(self.exit_menu)
        self.ui.actionSend_Feedback.activated.connect(self.feedback)
        self.ui.actionMake_someone_happy.activated.connect(self.paypalui)
        self.ui.btOpenTo.setIcon(QtGui.QIcon(get_file('openfolder.png')))
        self.ui.btOpenFrom.setIcon(QtGui.QIcon(get_file('openfolder.png')))

    @Slot(str)
    def say_words(self, words):
        self.ui.textStatus.append(words)

    @staticmethod
    def paypalui():
        pay = PayPalUI()
        pay.exec_()

    @staticmethod
    def feedback():
        feed = Feedback()
        feed.exec_()

    def about_box(self):
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

    def about_box_qt(self):
        QMessageBox.aboutQt(self, 'About Qt')

    def about_license(self):
        try:
            f = open(get_file('GNU_HTML'))
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

    def from_open(self):
        chosen_from_dir = self.get_directory()
        self.dir_from = chosen_from_dir + "/"
        print(self.dir_from)
        self.ui.textFrom.setText(self.dir_from)
        pass

    def to_open(self):
        chosen_to_dir = self.get_directory()
        self.dir_to = chosen_to_dir + "/"
        print(self.dir_to)
        self.ui.textTo.setText(self.dir_to)
        pass

    def sync(self):
        self.thread_progress = CheckProgress(
            self.dir_from, self.dir_to, self.some)
        self.thread_progress.start()
        pass

    def get_directory(self):
        dialog = QtGui.QFileDialog()
        dialog.setFileMode(QtGui.QFileDialog.Directory)
        dialog.setOption(QtGui.QFileDialog.ShowDirsOnly)
        return dialog.getExistingDirectory()

    def exit_menu(self):
        self.close()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = MainUi()
    try:
        app.setWindowIcon(QtGui.QIcon(get_file('synchronizer-rd.png')))
        main.setWindowIcon(QtGui.QIcon(get_file('synchronizer-rd.png')))
    except:
        QMessageBox.critical(
            main, 'Error', 'Unable to open icon synchronizer-rd.png')
    main.show()
    sys.exit(app.exec_())

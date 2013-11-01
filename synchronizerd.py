#-*- coding: utf-8 -*-
import sys
import os
import subprocess
import PySide
from threading import Thread
from PySide import QtGui
from PySide import QtCore
from PySide.QtGui import QMessageBox
from PySide.QtCore import QThread, QObject
from views.synchronizerd_ui import Ui_SyncMain
__version__ = '1.0.0'
import platform

dir_from = None
dir_to = None
if len(sys.argv) == 3:
    entrada1 = sys.argv[1]
    print entrada1
    entrada2 = sys.argv[2]
    print entrada2
    if os.path.isdir(entrada1):
        dir_from = entrada1
        print "Path 1 is a directory"

    if os.path.isdir(entrada2):
        dir_to = entrada2
        print "Path 2 is a directory"

    dir_from = entrada1
    dir_from = entrada2


def mBoxExec(message):
    QMessageBox.information(None, 'Error!', message, QMessageBox.Ok)


class Communicate(QObject):
    speak = QtCore.Signal(str)
    mBox = QtCore.Signal(str)


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
            print e

    def run(self):
        self.getProgress()

    def getProgress(self):
        while True:
            out = self.processo.stdout.readline(150)
            if out == '' and self.processo.poll() is not None:
                print "processo acabou"
                break
            print out
            self.some.speak.emit(out)


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
        self.ui.actionAbout_Qt.activated.connect(self.aboutBoxQt)

    @QtCore.Slot(str)
    def sayWords(self, words):
        self.ui.textStatus.append(words)

    def aboutBox(self):
        about = QMessageBox.about(self, "About SynchroniZeRD",
        u"""<b>SynchroniZeRD</b> v %s
        <p>Copyright (C) 2013 Ronnie Andrew.
        All rights reserved in accordance with
        GPL v3 or later - NO WARRANTIES!</p>
        <p>This application can be used to synchronize folders using <b>rsync</b> as main feature.</p>
        <p><b>Official Website:</b> <a href='http://roandigital.com/applications/synchronizerd'>Roan Digital</a></p>
        <p>%s</p>
        """ % (__version__, platform.system()))

    def aboutBoxQt(self):
        QMessageBox.aboutQt(self, 'About Qt')
        pass

    def fromOpen(self):
        chosenFromDir = self.getDirectory()
        self.dir_from = chosenFromDir + "/"
        print self.dir_from
        self.ui.textFrom.setText(self.dir_from)
        pass

    def toOpen(self):
        chosenToDir = self.getDirectory()
        self.dir_to = chosenToDir + "/"
        print self.dir_to
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

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = MainUi()
    main.show()
    sys.exit(app.exec_())

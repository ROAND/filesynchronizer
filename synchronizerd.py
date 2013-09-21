import sys
import os
import subprocess
from threading import Thread
from PySide import QtGui
from PySide import QtCore
from views.synchronizerd_ui import Ui_SyncMain
import Queue

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


class CheckProgress(Thread):

    def __init__(self, process, status, queue):
        Thread.__init__(self)
        self.process = process
        self.status = status
        self.queue = queue

    def run(self):
        self.getProgress()

    def getProgress(self):
        while True:
            out = self.process.stdout.readline(150)
            if out == '' and self.process.poll() != None:
                self.queue.task_done()
                print "processo acabou"
                break
            # print out
            self.queue.put(out)
#           self.status.append(out)
            # yield out


class MainUi(QtGui.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainUi, self).__init__()
        self.ui = Ui_SyncMain()
        self.ui.setupUi(self)
        self.ui.btOpenFrom.clicked.connect(self.fromOpen)
        self.ui.btOpenTo.clicked.connect(self.toOpen)
        self.ui.btSync.clicked.connect(self.sync)
        self.queue = Queue.Queue()

    def fromOpen(self):
        chosenFromDir = self.getDirectory()
        self.dir_from = chosenFromDir + "/*"
        self.ui.textFrom.setText(self.dir_from)
        pass

    def toOpen(self):
        chosenToDir = self.getDirectory()
        self.dir_to = chosenToDir + "/"
        self.ui.textTo.setText(self.dir_to)
        pass

    def sync(self):
        self.processo = subprocess.Popen(
            ["rsync", "-av", "--progress", "--size-only", "%s" %
             self.dir_from, "%s" % self.dir_to], shell=False, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        self.threadProgress = CheckProgress(
            self.processo, self.ui.textStatus, self.queue)
        self.threadProgress.start()
#        self.threadProgress.join()
        self.statusUpdate()
        pass

    def statusUpdate(self):
        while True:
            line = None
            if self.queue.unfinished_tasks >= 0:
                line = self.queue.get()
                print line
                self.queue.task_done()
                print self.queue.unfinished_tasks
                self.ui.textStatus.append(line)
            else:
                break

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

import sys

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from function1 import gui1_1
from function2 import gui2
from function3 import gui3
from function4 import gui4

qtCreatorFile = "homepage.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class Homepage(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.center()
        self.show()
        self.btn_funct1.clicked.connect(self.switch_to_funct1_1)
        self.btn_funct2.clicked.connect(self.switch_to_funct2)
        self.btn_funct3.clicked.connect(self.switch_to_funct3)
        self.btn_funct4.clicked.connect(self.switch_to_funct4)

    def center(self):
        frameGm = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def switch_to_funct1_1(self):
        pos = self.pos()
        self.main = gui1_1.Funct1_1()
        self.main.move(pos)
        self.main.show()
        self.close()

    def switch_to_funct2(self):
        pos = self.pos()
        self.main = gui2.Funct2()
        self.main.move(pos)
        self.main.show()
        self.close()

    def switch_to_funct3(self):
        pos = self.pos()
        self.main = gui3.Funct3()
        self.main.move(pos)
        self.main.show()
        self.close()

    def switch_to_funct4(self):
        pos = self.pos()
        self.main = gui4.Funct4()
        self.main.move(pos)
        self.main.show()
        self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Homepage()
    sys.exit(app.exec_())

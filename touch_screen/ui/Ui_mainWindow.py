# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/pi/charlesUI/touch_screen/ui/mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 480)
        MainWindow.setStyleSheet("background-color: rgb(52, 52, 52)")
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.openBox = QtWidgets.QPushButton(self.centralWidget)
        self.openBox.setGeometry(QtCore.QRect(450, 270, 230, 150))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.openBox.setFont(font)
        self.openBox.setStyleSheet("#openBox {\n"
"color: rgb(255, 255, 127);\n"
"background-color: rgb(242, 242, 242, 20) ;\n"
"border-radius: 20px\n"
"}")
        self.openBox.setObjectName("openBox")
        self.time = QtWidgets.QLineEdit(self.centralWidget)
        self.time.setGeometry(QtCore.QRect(150, 100, 500, 45))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.time.setFont(font)
        self.time.setStyleSheet("#time\n"
"{\n"
"color: rgb(255, 255, 255);\n"
"}")
        self.time.setAlignment(QtCore.Qt.AlignCenter)
        self.time.setObjectName("time")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(105, 20, 590, 51))
        font = QtGui.QFont()
        font.setFamily("Piboto [Goog]")
        font.setPointSize(28)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255)")
        self.label.setObjectName("label")
        self.go = QtWidgets.QPushButton(self.centralWidget)
        self.go.setGeometry(QtCore.QRect(120, 270, 230, 150))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.go.setFont(font)
        self.go.setStyleSheet("#go {\n"
"color: rgb(0, 170, 0); \n"
"background-color: rgb(242, 242, 242, 20) ;\n"
"border-radius: 20px\n"
"}")
        self.go.setObjectName("go")
        self.comboBox = QtWidgets.QComboBox(self.centralWidget)
        self.comboBox.setGeometry(QtCore.QRect(120, 180, 120, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.comboBox.setFont(font)
        self.comboBox.setStyleSheet("#comboBox\n"
"{\n"
"color: white;\n"
"background:  rgb(52, 52, 52)\n"
"}")
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.progressBar = QtWidgets.QProgressBar(self.centralWidget)
        self.progressBar.setGeometry(QtCore.QRect(340, 180, 120, 24))
        self.progressBar.setStyleSheet("#progressBar\n"
"{\n"
"text-align: center; \n"
"}\n"
"#progressBar::chunk\n"
"{\n"
"background-color: rgb(0, 234, 0);\n"
"width: 7px; \n"
"margin: 1px;  \n"
"}")
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Robot Charles"))
        self.openBox.setText(_translate("MainWindow", "Open Box"))
        self.label.setText(_translate("MainWindow", "Charles Autonomous Service Robot"))
        self.go.setText(_translate("MainWindow", "GO"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Room 220"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Room 221"))
        self.comboBox.setItemText(2, _translate("MainWindow", "Room 222"))
        self.comboBox.setItemText(3, _translate("MainWindow", "Room 223"))
        self.comboBox.setItemText(4, _translate("MainWindow", "Room 224"))
        self.comboBox.setItemText(5, _translate("MainWindow", "Room 225"))
        self.comboBox.setItemText(6, _translate("MainWindow", "Room 226"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


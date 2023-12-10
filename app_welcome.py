# -*- coding: utf-8 -*-
import webbrowser

from PyQt5 import QtCore, QtGui, QtWidgets

__all__ = ()


class UiMainwindow(object):
    def setup_ui(self, main_window):
        main_window.setObjectName("MainWindow")
        main_window.resize(582, 105)
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(120, 50, 331, 41))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 50, 101, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(460, 50, 101, 41))
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton.clicked.connect(lambda x: self.start_checker())
        self.pushButton_2.clicked.connect(lambda x: self.exit_code())
        self.pushButton_3.clicked.connect(lambda x: self.redirect())

        main_window.setCentralWidget(self.centralwidget)

        self.retranslate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Identify me"))
        self.label.setText(_translate("MainWindow", "Face Recognizer"))
        self.pushButton_2.setText(_translate("MainWindow", "Exit"))
        self.pushButton_3.setText(_translate("MainWindow", "Help"))

    def start_checker(self):
        QtCore.QCoreApplication.quit()

    def redirect(self):
        webbrowser.open(
            "https://github.com/TabarakoAkula/FaceRecognizerProject",
            new=2,
        )

    def exit_code(self):
        exit()


def welcome_app_starter():
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = UiMainwindow()
    ui.setup_ui(main_window)
    main_window.show()
    app.exec_()
    return


if __name__ == "__main__":
    welcome_app_starter()

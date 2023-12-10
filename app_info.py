# -*- coding: utf-8 -*-
import webbrowser

from PyQt5 import QtCore, QtGui, QtWidgets

__all__ = ()


class UiMainwindow(object):
    def setup_ui(self, main_window, data):
        main_window.setObjectName("MainWindow")
        main_window.resize(582, 239)
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 180, 101, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(460, 180, 101, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 471, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 100, 511, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 140, 621, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        main_window.setCentralWidget(self.centralwidget)
        self.retranslate_ui(main_window)
        if data["predicted_user"] != "Unknown":
            self.label_4.setText(self.label_4.text() + " " + "Access granted")
        else:
            self.label_4.setText(self.label_4.text() + " " + "Access denied")
        self.label_2.setText(
            self.label_2.text() + " " + data["predicted_user"],
        )
        self.label_3.setText(
            self.label_3.text() + " " + str(round(data["confidence"], 2)),
        )

        self.pushButton_2.clicked.connect(lambda x: self.exit_checker())
        self.pushButton_3.clicked.connect(lambda x: self.redirect())

        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Face Recognizer"))
        self.pushButton_2.setText(_translate("MainWindow", "Exit"))
        self.pushButton_3.setText(_translate("MainWindow", "Help"))
        self.label_2.setText(
            _translate("MainWindow", "You have been identified as:"),
        )
        self.label_3.setText(_translate("MainWindow", "Confidence:"))
        self.label_4.setText(_translate("MainWindow", "Status:"))

    def exit_checker(self):
        QtCore.QCoreApplication.quit()

    def redirect(self):
        webbrowser.open(
            "https://github.com/TabarakoAkula/FaceRecognizerProject",
            new=2,
        )


def info_app_starter(data):
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = UiMainwindow()
    ui.setup_ui(main_window, data)
    main_window.show()
    app.exec_()
    return

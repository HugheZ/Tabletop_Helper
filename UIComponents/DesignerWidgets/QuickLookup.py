# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QuickLookup.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_QuickLookup(object):
    def setupUi(self, QuickLookup):
        QuickLookup.setObjectName("QuickLookup")
        QuickLookup.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(QuickLookup)
        self.gridLayout.setObjectName("gridLayout")
        self.overallLayout = QtWidgets.QVBoxLayout()
        self.overallLayout.setObjectName("overallLayout")
        self.searchLayout = QtWidgets.QHBoxLayout()
        self.searchLayout.setObjectName("searchLayout")
        self.categorySelect = QtWidgets.QComboBox(QuickLookup)
        self.categorySelect.setObjectName("categorySelect")
        self.searchLayout.addWidget(self.categorySelect)
        self.searchBox = QtWidgets.QLineEdit(QuickLookup)
        self.searchBox.setObjectName("searchBox")
        self.searchLayout.addWidget(self.searchBox)
        self.overallLayout.addLayout(self.searchLayout)
        self.endpoint = QtWidgets.QLineEdit(QuickLookup)
        self.endpoint.setObjectName("endpoint")
        self.overallLayout.addWidget(self.endpoint)
        self.searchProgress = QtWidgets.QProgressBar(QuickLookup)
        self.searchProgress.setProperty("value", 0)
        self.searchProgress.setInvertedAppearance(False)
        self.searchProgress.setObjectName("searchProgress")
        self.overallLayout.addWidget(self.searchProgress)
        self.output = QtWidgets.QPlainTextEdit(QuickLookup)
        self.output.setAcceptDrops(False)
        self.output.setReadOnly(True)
        self.output.setObjectName("output")
        self.overallLayout.addWidget(self.output)
        self.gridLayout.addLayout(self.overallLayout, 0, 0, 1, 1)

        self.retranslateUi(QuickLookup)
        QtCore.QMetaObject.connectSlotsByName(QuickLookup)

    def retranslateUi(self, QuickLookup):
        _translate = QtCore.QCoreApplication.translate
        QuickLookup.setWindowTitle(_translate("QuickLookup", "Form"))
        self.searchBox.setPlaceholderText(_translate("QuickLookup", "Enter Search Term for Category"))
        self.endpoint.setStatusTip(_translate("QuickLookup", "Pull from \"http://dnd5eapi.co/api/\" and \"https://api.open5e.com/\""))
        self.endpoint.setWhatsThis(_translate("QuickLookup", "Pulls from \"http://dnd5eapi.co/api/\" and \"https://api.open5e.com/\" using the REST framework\n"
"\n"
"If you want to know which endpoints to use, input the given URLs first and the return should tell you how to go deeper. Alternatively, you can visit these sights on your web browser."))
        self.endpoint.setPlaceholderText(_translate("QuickLookup", "Enter Custom Endpoint"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    QuickLookup = QtWidgets.QWidget()
    ui = Ui_QuickLookup()
    ui.setupUi(QuickLookup)
    QuickLookup.show()
    sys.exit(app.exec_())

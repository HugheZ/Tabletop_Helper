

from PyQt5.QtWidgets import QWidget, QProgressBar, QPlainTextEdit, QPushButton, QComboBox
from PyQt5.QtCore import pyqtSlot
import requests, pprint
from .DesignerWidgets.QuickLookup import *
from .Backend.APIConnector import *
import threading

'''
Wrapper class to implement functionality of 5e API requests
'''
class Lookup(QWidget, Ui_QuickLookup):
    def __init__(self):
        super(QWidget, self).__init__()
        self.setupUi(self)
        
        #set up the ui components
        for v in TERMS.keys():
            self.categorySelect.addItem(v)
        
        #connect all of the UI components
        self.searchBox.returnPressed.connect(self.submit)
        self.searchProgress.valueChanged.connect(self.onProgressChanged)
    
    
    @pyqtSlot()
    def submit(self):
        #t = threading.Thread(target = searchTerm, args=(str(self.categorySelect.currentText()), str(self.searchBox.text()), self.searchProgress.valueChanged, self.output), daemon=True)
        #t.start()
        searchTerm(str(self.categorySelect.currentText()), str(self.searchBox.text()), self.searchProgress.valueChanged, self.output)
    
    @pyqtSlot(int)
    def onProgressChanged(self, val):
        self.searchProgress.setValue(val)
        if self.searchProgress.maximum() == val:
            self.searchProgress.setValue(0)
        
        
        

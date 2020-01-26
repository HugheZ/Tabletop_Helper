from PyQt5.QtWidgets import QWidget, QDialog, QTabWidget, QPlainTextEdit, QGridLayout

import json

'''
A simple helper window for the application. It is divided into taps described below:

About: the about tab tells the use of this application, who made it, etc.

Use: this tab tells the user how to use the app's functionality, which windows do what, and how widgets link

Format: the format tab explains how fields should be formatted in order to allow the app to automatically roll, fill out fields, etc.

'''

class HelpDialog(QDialog):
    #dest: file destination
    def __init__(self, dest):
        super(HelpDialog, self).__init__()
        
        #set layout with tab
        self.tab = QTabWidget()
        self.layout = QGridLayout()
        self.layout.addWidget(self.tab)
        self.setLayout(self.layout)
        self.setWindowTitle("Help")
        
        #add tabs
        #read json data
        try:
            with open(dest) as f:
                helpDict = json.load(f)
                for (key,val) in helpDict.items():
                    edit = QPlainTextEdit()
                    edit.setPlainText(val)
                    edit.setReadOnly(True)
                    self.tab.addTab(edit, key)
        except (IOError, FileNotFoundError )as e:
            if type(e) == IOError:
                raise IOError("The help file could not be read. Perhaps it is corrupted?")
            else:
                raise FileNotFoundError("The help file could not be found. Please replace the help.json file in DNDHelper/UIComponents/Backend.")
        
        #resize
        self.resize(500,600)

'''
A simple initiative tracker, allows the user to add new members to the
initiative order, remove selected members, or delete the list

TODO: drag/drop ordering messes up tab order
TODO: add simpler way to add/remove members

'''

from PyQt5.QtWidgets import QWidget, QPushButton, QListWidget, QAbstractItemView, QBoxLayout, QVBoxLayout, QStyle, QLineEdit, QLabel, QListWidgetItem, QSizePolicy, QHBoxLayout
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtCore import QSize, pyqtSlot, Qt
from .DesignerWidgets.InitiativeMember import *
from .DesignerWidgets.InitiativeTracker import *

'''
DEPRECATED

class InitiativeTracker(QWidget):
    def __init__(self):
        super().__init__()
        
        #define control buttons
        self.addButton = QPushButton("+")
        self.deleteSelected = QPushButton("-")
        self.deleteAll = QPushButton("")
        self.deleteAll.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
        
        #define list
        self.initList = QListWidget()
        #allow drag and drop of items
        self.initList.setDragDropMode(QAbstractItemView.InternalMove)
        
        
        #define button layout
        self.buttonLayout = QBoxLayout(QBoxLayout.LeftToRight)
        self.buttonLayout.addWidget(self.addButton)
        self.buttonLayout.addWidget(self.deleteSelected)
        self.buttonLayout.addWidget(self.deleteAll)
        self.buttons = QWidget()
        self.buttons.setLayout(self.buttonLayout)
        
        #define composing layout
        self.overallLayout = QVBoxLayout()
        self.overallLayout.addWidget(self.buttons)
        self.overallLayout.addWidget(self.initList)
        self.setLayout(self.overallLayout)
        
        
        #set initial state
        self.deleteSelected.setEnabled(False)
        self.deleteAll.setEnabled(False)
        
        #define style
        self.setStyleSheet("QListWidget::item { border: 1px solid black; }")
        
        #connect buttons
        self.addButton.clicked.connect(self.addItem)
        self.deleteAll.clicked.connect(self.clear)
        self.deleteSelected.clicked.connect(self.removeSelected)
        self.initList.itemClicked.connect(self.enableRemoval)
        self.initList.itemSelectionChanged.connect(self.disableRemoval)
    
    
    ''
    Adds a single item to the initiative list
    
    ''
    @pyqtSlot()
    def addItem(self):
        initMember = InitMem()
        item = QListWidgetItem(self.initList)
        item.setSizeHint(initMember.sizeHint())
        self.initList.addItem(item)
        self.initList.setItemWidget(item, initMember)
        self.deleteAll.setEnabled(True)
        
    
    ''
    Removes all items from the initiative list
    
    ''
    @pyqtSlot()
    def clear(self):
        self.initList.clear()
        self.deleteAll.setEnabled(False)
        self.deleteSelected.setEnabled(False)
    
    ''
    Removes a selected item from the list
    
    ''
    @pyqtSlot()
    def removeSelected(self):
        #remove selected
        for item in self.initList.selectedItems():
            self.initList.takeItem(self.initList.row(item))
        
        #disable remove all if count is empty
        if self.initList.count() == 0:
            self.deleteAll.setEnabled(False)
        
        #disable button
        self.deleteSelected.setEnabled(False)
    
    ''
    Enables the clear selected when list has gained focus
    
    ''
    @pyqtSlot()
    def enableRemoval(self):
        self.deleteSelected.setEnabled(True)
    
    ''
    Disables the clear selected when list has lost focus
    
    ''
    @pyqtSlot()
    def disableRemoval(self):
        if self.initList.count() == 0:
            self.deleteSelected.setEnabled(False)'''
            
'''
The Initiative Tracker docker internal widget. Contains info and handling
buttons for manipulating the list of initiative
'''
class InitiativeTracker(QWidget, Ui_InitTracker):
    def __init__(self):
        super(QWidget, self).__init__()
        self.setupUi(self)

            #set initial state
        self.deleteSelected.setEnabled(False)
        self.deleteAll.setEnabled(False)
        
        #define style
        self.setStyleSheet("QListWidget::item { border: 1px solid black; }")
        
        #connect buttons
        self.addButton.clicked.connect(self.addItem)
        self.deleteAll.clicked.connect(self.clear)
        self.deleteSelected.clicked.connect(self.removeSelected)
        self.initList.itemClicked.connect(self.enableRemoval)
        self.initList.itemSelectionChanged.connect(self.disableRemoval)
    
    
    '''
    Adds a single item to the initiative list
    
    '''
    @pyqtSlot()
    def addItem(self):
        initMember = InitMem()
        item = QListWidgetItem(self.initList)
        item.setSizeHint(initMember.sizeHint())
        self.initList.addItem(item)
        self.initList.setItemWidget(item, initMember)
        self.deleteAll.setEnabled(True)
        
    
    '''
    Removes all items from the initiative list
    
    '''
    @pyqtSlot()
    def clear(self):
        self.initList.clear()
        self.deleteAll.setEnabled(False)
        self.deleteSelected.setEnabled(False)
    
    '''
    Removes a selected item from the list
    
    '''
    @pyqtSlot()
    def removeSelected(self):
        #remove selected
        for item in self.initList.selectedItems():
            self.initList.takeItem(self.initList.row(item))
        
        #disable remove all if count is empty
        if self.initList.count() == 0:
            self.deleteAll.setEnabled(False)
        
        #disable button
        self.deleteSelected.setEnabled(False)
    
    '''
    Enables the clear selected when list has gained focus
    
    '''
    @pyqtSlot()
    def enableRemoval(self):
        self.deleteSelected.setEnabled(True)
    
    '''
    Disables the clear selected when list has lost focus
    
    '''
    @pyqtSlot()
    def disableRemoval(self):
        if self.initList.count() == 0:
            self.deleteSelected.setEnabled(False)


'''
Simple widget to contain a name 
'''
class InitMem(QWidget, Ui_InitiativeMember):
    def __init__(self):
        super(QWidget, self).__init__()
        self.setupUi(self)
    
    def sizeHint(self):
        return QSize(100,100)

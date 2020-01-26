from .DesignerWidgets.MainWindow import *
from .Initiative import *
from .Form import *
from .Lookup import *
from .Spell import *
from PyQt5.QtWidgets import QWidget, QDockWidget, QMainWindow, QScrollArea, QFileDialog, QMessageBox, QLineEdit, QPlainTextEdit, QSpinBox, QCheckBox, QMdiArea, QTabWidget, QColorDialog
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, pyqtSlot, QSettings, QPoint
from .Help import *
from functools import partial

import os


'''TODO

- Bind underlying object to UI
- Set up new character on run
- Mechanism for multiple characters open at once:
    - QMdiArea, QTabWidget for DM stuff with tabs on west
- implement saving and saving as
- DM features

'''


'''NOTE

- Currently removing the underlying Character object as it is not needed

'''


'''
Defines a wrapper class for the designer widget main window

'''
class CentralWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        #dirty boolean to alert on closes before saving
        self.dirtyList = []
        #set up member values
        #self.characters = []
        self.saveLocs = [] #save location
        
        #set up UI
        super(QWidget, self).__init__()
        self.setupUi(self)
        
        #add the docker widgets
        self.addDockers()
        
        #GET SETTINGS FOR SETUP
        settings = QSettings("Hughes", "Tabletop Helper")
        
        #main window settings
        settings.beginGroup("mainWindow")
        #get whether docks were
        initOpen = settings.value("initOpen",True,type=bool)
        lookupOpen = settings.value("lookupOpen",True,type=bool)
        #get location of docks
        initLoc = settings.value("initLocation", Qt.RightDockWidgetArea)
        lookupLoc = settings.value("lookupLocation", Qt.LeftDockWidgetArea)
        #get window size and location
        width = settings.value("windowWidth", 800)
        height = settings.value("windowHeight", 800)
        loc = settings.value("windowLocation", QPoint(50,50))
        settings.endGroup()
        
        #get color
        settings.beginGroup("preferences")
        self.diceColor = settings.value("diceColor", Qt.white)
        settings.endGroup()
        
        self.actionInitiative_Tracker.setChecked(initOpen)
        self.actionQuick_Lookup.setChecked(lookupOpen)
        
        #connect
        self.addFunctions()
        
        
        self.resize(width,height)
        self.move(loc)
        self.setCentralWidget(self.centralWidget())
        self.addDockWidget(initLoc, self.trackerDock)
        self.addDockWidget(lookupLoc, self.lookupDock)
        
        if not initOpen: self.trackerDock.hide()
        if not lookupOpen: self.lookupDock.hide()
        
    '''
    links input fields to a color changing service
    
    '''
    def linkColorChanging(self, index):
        for widget in self.centralWidget().widget(index).findChildren((QLineEdit, QPlainTextEdit, QSpinBox, QCheckBox)):
            if widget.objectName()!= 'qt_spinbox_lineedit':
                if type(widget) == QSpinBox:
                    widget.valueChanged.connect(partial(self.widgetEdited, widget))
                elif type(widget) == QPlainTextEdit:
                    widget.textChanged.connect(partial(self.widgetEdited, widget))
                elif type(widget) == QLineEdit:
                    widget.editingFinished.connect(partial(self.widgetEdited, widget))
                else: #QCheckBox
                    widget.toggled.connect(partial(self.widgetEdited, widget))
    
    
    '''
    adds dock widgets to the existing docks
    
    '''
    def addDockers(self):
        self.setCentralWidget(QTabWidget())
        self.centralWidget().setTabsClosable(True)
        self.trackerDock = QDockWidget("Initiative")
        self.trackerDock.setWidget(InitiativeTracker())
        self.lookupDock = QDockWidget("Quick Lookup")
        self.lookupDock.setWidget(Lookup())
    
    '''
    adds functions to the file menu
    
    '''
    def addFunctions(self):
        self.actionNew.triggered.connect(self.newFile)
        self.actionOpen.triggered.connect(self.openFile)
        self.actionSave.triggered.connect(self.saveFile)
        self.actionSaveAs.triggered.connect(self.saveFileAs)
        self.actionQuit.triggered.connect(self.exit)
        
        #set dock actions
        self.action_initiative = self.trackerDock.toggleViewAction()
        self.action_initiative.setText("Initiative Tracker")
        self.action_initiative.setStatusTip("Open the initiative tracker")
        self.action_initiative.setCheckable(True)
        self.action_lookup = self.lookupDock.toggleViewAction()
        self.action_lookup.setText("Quick Manual Lookup")
        self.action_lookup.setStatusTip("Open the quick lookup menu for the game guide")
        self.action_lookup.setCheckable(True)
        
        self.menuWindow.addAction(self.action_initiative)
        self.menuWindow.addAction(self.action_lookup)
        
        #connect closing to close handler for tab widget
        self.centralWidget().tabCloseRequested.connect(self.closeHandler)
        
        #connect help widget
        self.actionAbout.triggered.connect(self.openHelp)
        
        #connect color widget
        self.actionDice_Color.triggered.connect(self.getColor)
    
    
    '''
    Handles tab closing events, checking if the form has been edited before closing
    
    '''
    @pyqtSlot(int)
    def closeHandler(self, index):
        print(
            "Index: " + str(index) +
            "Dirty?: " + str(self.dirtyList[index]) +
            "SaveLoc: " + str(self.saveLocs[index])
            )
        #if dirty, save first
        if self.dirtyList[index]:
            #ask if we wished to save
            saveBox = QMessageBox()
            saveBox.setIcon(QMessageBox.Warning)
            saveBox.setText("You are attempting to close a file, but it has not been saved. Do you wish to save your changes?")
            saveBox.setWindowTitle("Unsaved Changes")
            saveBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            buttonPressed = saveBox.exec_()
            
            
            #asked to discard changes
            if buttonPressed == QMessageBox.Cancel:
                #pressed cancel, just ignore the event
                return
            elif buttonPressed == QMessageBox.Save:
                #save the index we were on
                prevIndex = self.centralWidget().currentIndex()
                self.centralWidget().setCurrentIndex(index)
                self.saveFile()
                #return to previous index
                self.centralWidget().setCurrentIndex(prevIndex)
            
            #if saved or discard changes, remove
            if buttonPressed == QMessageBox.Discard or not self.dirtyList[index]:
                self.centralWidget().widget(index).deleteLater()
                self.centralWidget().removeTab(index)
                del self.saveLocs[index]
                #del self.characters[index]
                del self.dirtyList[index]
            
        else:
            #else close it
            self.centralWidget().widget(index).deleteLater()
            self.centralWidget().removeTab(index)
            del self.saveLocs[index]
            #del self.characters[index]
            del self.dirtyList[index]
    
    
    '''
    Opens the help menu
    This method is separated to allow for better error handling
    
    '''
    @pyqtSlot()
    def openHelp(self):
        try:
            helpWindow = HelpDialog(os.path.join("UIComponents","Backend","help.json"))
            helpWindow.setModal(True)
            helpWindow.exec_()
        except Exception as e:
            er = QMessageBox()
            er.setIcon(QMessageBox.Critical)
            er.setText(str(e))
            er.setDetailedText("There appears to be an error with the help.json file. Try replacing it.\nThis file can be found in DNDHelper/UIComponents/Backend.")
            er.setWindowTitle("Help File Read Error")
            er.setStandardButtons(QMessageBox.Ok)
            er.exec_()
    
    '''
    Gets a color from the user to use for dice
    
    TODO: notify roller of color change
    '''
    @pyqtSlot()
    def getColor(self):
        self.diceColor = QColorDialog.getColor()
    
    
    '''
    Action for setting up a file
    
    '''
    @pyqtSlot()
    def newFile(self):
        indx = self.centralWidget().count()
        #open a new tab
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        form = Form()
        
        #connect form to listener
        form.nameChange.connect(self.formNameChanged)
        
        scroll.setWidget(form)
        self.centralWidget().addTab(scroll, "Character " + str(indx + 1))
        self.dirtyList.append(False)
        self.saveLocs.append(None)
        #self.characters.append(Character())
        #TODO: link to form
        self.linkColorChanging(indx)
    
    '''
    Action for opening a file
    
    '''
    @pyqtSlot()
    def openFile(self):
        fileName = QFileDialog.getOpenFileName(self, "Open Character", "", "Character Files (*.json);;Encounter Files (*.json);;Notes Files (*.txt)")
        if fileName[0] is None or fileName[0] == '':
            return
        
        #file is good, what do we need to open?
        #if character file
        #TODO: remove this line if not implementing DM files
        if fileName[1] == "Character Files (*.json)":
            indx = self.centralWidget().count()
            try:
                scroll = QScrollArea()
                scroll.setWidgetResizable(True)
                form = Form()
                
                #fill form
                form.loadFromFile(fileName[0])
                
                #link to name change listener
                form.nameChange.connect(self.formNameChanged)
                
                #add form and change form name to character name
                scroll.setWidget(form)
                name = form.characterName.text() if form.characterName.text() != "" else "Character " + str(indx + 1)
                
                self.centralWidget().addTab(scroll, name)
                self.dirtyList.append(False)
                self.linkColorChanging(indx)
                
                #append to existing arrays
                #self.characters.append(Character.load(fileName[0]))
                self.saveLocs.append(fileName[0])
            except Exception as e:
                er = QMessageBox()
                er.setIcon(QMessageBox.Critical)
                er.setText(str(e))
                er.setDetailedText("This error occurs when the file is not correctly formatted for reading. Try comparing your file to a dummy created file. Additionally, the software may have updated, making the underlying storage obsolete.")
                er.setWindowTitle("File Read Error")
                er.setStandardButtons(QMessageBox.Ok)
                er.exec_()
                #remove created tab
                #TODO: check this to see if it works
                #remove from save list if successfully added
                if self.centralWidget().count() > indx:
                    del self.dirtyList[indx]
                #try to remove tab
                try:
                    self.centralWidget().widget(indx).deleteLater()
                    self.centralWidget().removeTab(indx)
                except Exception as e:
                    pass
    
    '''
    Handles changing a tab's title depending on name change of the form
    
    NOTE: can assume the opened tab is the name to change, since a name can only be changed if its form is opened
    
    '''
    @pyqtSlot(str)
    def formNameChanged(self, name):
        self.centralWidget().setTabText(self.centralWidget().currentIndex(), name)
    
    
    
    '''
    Action for saving a file
    
    '''
    @pyqtSlot()
    def saveFile(self):
        #only do anything if dirty file
        indx = self.centralWidget().currentIndex()
        if indx > -1 and self.dirtyList[indx]:
            #if file has not yet been saved, default to saveAs
            if self.saveLocs[indx] is None:
                self.saveFileAs()
            else:
                self.centralWidget().currentWidget().widget().saveToFile(self.saveLocs[indx])
                #self.characters[indx].save(self.saveLocs[indx])
                self.dirtyList[indx] = False
                self.whiteOnSave()
    
    '''
    Action for saving a new file
    
    '''
    @pyqtSlot()
    def saveFileAs(self):
        indx = self.centralWidget().currentIndex()
        if indx > -1:
            fileName = QFileDialog.getSaveFileName(self, "Save Character", "", "Character Files (*.json);;Encounter Files (*.json);;Notes Files (*.txt)")
            if fileName[0] != '' and fileName[0] is not None:
                self.centralWidget().currentWidget().widget().saveToFile(fileName[0])
                self.saveLocs[indx] = fileName[0]
                #self.characters[indx].save(fileName[0])
                self.dirtyList[indx] = False
                self.whiteOnSave()
    
    '''
    Simply closes, the close event will handle svaing
    
    '''
    @pyqtSlot()
    def exit(self):
        print("Exiting...")
        self.close()
    
    
    '''
    Defines a color change to yellow when a widget is edited and not saved
    Additionally, sets the global 'dirty' value to ensure the program knows a value was edited
    FIXME: color change requires the entire style sheet, else it loses the indicator
    '''
    @pyqtSlot(QWidget)
    def widgetEdited(self, widget):
        self.dirtyList[self.centralWidget().currentIndex()] = True
        widget.setStyleSheet("background-color:yellow;")#QCheckBox::indicator {background: yellow;};")
    
    '''
    Reinstates a white background on widgets once saved
    
    '''
    #@pyqtSlot()
    def whiteOnSave(self):
        for widget in self.centralWidget().currentWidget().findChildren((QLineEdit, QPlainTextEdit, QSpinBox, QCheckBox)):
            if widget.objectName()!= 'qt_spinbox_lineedit':
                widget.setStyleSheet("background-color:white")
    
    
    '''
    Quits the application, but checks to see if outstanding changes must be saved first
    TODO: check implement saving other files
    
    '''
    def closeEvent(self, event):
        #if clean, exit and save UI
        if not any(self.dirtyList):
            #save UI structure
            self.saveUI()
            event.accept()
        else:
            #compound string for unsaved files
            compoundString = ""
            for i in range(0, self.centralWidget().count()):
                if self.dirtyList[i]:
                    compoundString += "> Character file unsaved: " + self.centralWidget().tabText(i)  + "\n"
                
            #not clean, need to ask if user wants to save
            #pop up message box
            saveBox = QMessageBox()
            saveBox.setIcon(QMessageBox.Warning)
            saveBox.setText("You are attempting to exit, but a file has not been saved. Do you wish to save your changes?")
            saveBox.setDetailedText(compoundString)
            saveBox.setWindowTitle("Unsaved Changes")
            saveBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            buttonPressed = saveBox.exec_()
            
            #asked to discard changes
            if buttonPressed == QMessageBox.Discard:
                event.accept()
            elif buttonPressed == QMessageBox.Cancel:
                #pressed cancel, just ignore the event
                event.ignore()
            else:
                #pressed save, launch save files events
                for i in range(0, self.centralWidget().count()):
                    self.centralWidget().setCurrentIndex(i)
                    self.saveFile()
                #if succeeded, close
                if not any(self.dirtyList):
                    event.accept()
                else:
                    #didn't work, ignore
                    event.ignore()

    '''
    Saves the UI structure for future use
    
    '''
    def saveUI(self):
        settings = QSettings("Hughes", "Tabletop Helper")
        #main window settings
        settings.beginGroup("mainWindow")
        #get whether docks were
        settings.setValue("initOpen",self.trackerDock.isVisible())
        settings.setValue("lookupOpen",self.lookupDock.isVisible())
        #get location of docks
        settings.setValue("initLocation", self.dockWidgetArea(self.trackerDock))
        settings.setValue("lookupLocation", self.dockWidgetArea(self.lookupDock))
        #get window size and location
        settings.setValue("windowWidth", self.frameGeometry().width())
        height = settings.value("windowHeight", self.frameGeometry().height())
        settings.setValue("windowLocation", self.frameGeometry().topLeft())
        settings.endGroup()

from PyQt5.QtWidgets import QWidget, QListWidget, QListWidgetItem, QSizePolicy, QPushButton, QSpinBox, QLineEdit, QCheckBox, QPlainTextEdit
from .DesignerWidgets.CharacterForm import *
from .Spell import *
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from functools import partial
import math, json
from collections import OrderedDict

'''
Wrapper class for Form.Ui_Form


NOTE: for proficiency vlaues
> 1=full
> 2=half
> 0=none

'''

class Form(QWidget, Ui_Form):
    
    #defines a signal for pressing roll buttons
    #the signal shall be of the form _d_;_d_;_d_;... , mod
    roll = pyqtSignal(str, int)
    
    #defines the signal for a name change, redirecting the name change signal to the main app
    nameChange = pyqtSignal(str)
    
    
    def __init__(self):
        super(QWidget,self).__init__()
        self.setupUi(self)
        
        #TODO define new setup for linking all buttons with their appropriate mod boxes
        #link boxes in the form: {button: (proficiencyBox, diceField, modField)}
        #an empty dice field shall be treated as a d20
        self.rollLink = {
            
            
            }
        
        #define new setup for linking all abilities with their auto-fill fields
        #link boxes in the form: {ability: [(proficiencyBox, skillField), ... ]}
        #an empty proficiency field is treated as the base mod
        self.statLink = {
            self.strScore: [
                (None, self.strMod),
                (self.strSaveProficient, self.strSaveMod),
                (self.strAthleticsProficient, self.strAthleticsMod)
                ],
            self.dexScore: [
                (None, self.dexMod),
                (self.dexSaveProficient, self.dexSaveMod),
                (self.dexAcrobaticsProficient, self.dexAcrobaticsMod),
                (self.dexSleightProficient, self.dexSleightMod),
                (self.dexStealthProficient, self.dexStealthMod)
                ],
            self.conScore: [
                (None, self.conMod),
                (self.conSaveProficient, self.conSaveMod)
                ],
            self.intScore: [
                (None, self.intMod),
                (self.intSaveProficient, self.intSaveMod),
                (self.intArcanaProficient, self.intArcanaMod),
                (self.intHistoryProficient, self.intHistoryMod),
                (self.intInvestigationProficient, self.intInvestigationMod),
                (self.intNatureProficient, self.intNatureMod),
                (self.intReligionProficient, self.intReligionMod)
                ],
            self.wisScore: [
                (None, self.wisMod),
                (self.wisSaveProficient, self.wisSaveMod),
                (self.wisAnimalProficient, self.wisAnimalMod),
                (self.wisInsightProficient, self.wisInsightMod),
                (self.wisMedicineProficient, self.wisMedicineMod),
                (self.wisPerceptionProficient, self.wisPerceptionMod),
                (self.wisSurvivalProficient, self.wisSurvivalMod)
                ],
            self.chaScore: [
                (None, self.chaMod),
                (self.chaSaveProficient, self.chaSaveMod),
                (self.chaDeceptionProficient, self.chaDeceptionMod),
                (self.chaIntimidationProficient, self.chaIntimidationMod),
                (self.chaPerformanceProficient, self.chaPerformanceMod),
                (self.chaPersuasionProficient, self.chaPersuasionMod)
                ]
            
            }
        
        #add spell subwidgets to each spell list
        self.addSpellSubWidgets()
        
        #link all buttons to the roll signal
        for item in self.findChildren(QPushButton):
            item.clicked.connect(partial(self.rollPressed, item))
        
        #link all ability fields to their auto-updates
        for item in self.statLink.keys():
            item.editingFinished.connect(partial(self.statUpdated, item))
        
        #link updating all skills when proficiency value changes
        self.proficiency.editingFinished.connect(self.updateAllSkills)
        
        #first, flatten sublists
        flatProfs = [prof for sublist in self.statLink.values() for prof in sublist]
        
        #for each item in the sublist, connect it to an updator
        for profTuple in flatProfs:
            if profTuple[0] is not None:
                profTuple[0].stateChanged.connect(partial(self.skillProficiencyChanged, profTuple[1]))
        
        #connect governing ability change for spellcasting to updater
        self.spellAbility.editingFinished.connect(self.spellAbilityChanged)
        
        
        #emit signal to main app when name changes
        self.characterName.textChanged.connect(self.nameChanged)
        
        
        
    '''
    Adds 10 spell subwidgets to the main UI
    
    '''
    def addSpellSubWidgets(self):
        spellLists = [self.spellsLevel1, self.spellsLevel2, self.spellsLevel3, self.spellsLevel4,
                      self.spellsLevel5, self.spellsLevel6, self.spellsLevel7, self.spellsLevel8, self.spellsLevel9]
        
        #for each list, add 10 spell widgets
        for i in range(len(spellLists)):
            for j in range(0,10):
                spell = Spell()
                item = QListWidgetItem(spellLists[i])
                item.setSizeHint(spell.sizeHint())
                spell.setObjectName("spellsLevel" + str(i+1) + "_" + str(j+1))
                spellLists[i].addItem(item)
                spellLists[i].setItemWidget(item, spell)
    
    
    '''TODO
    Handles rolling events and emits the signal to the roll-handling widget
    
    widget: the button that caused the press
    '''
    @pyqtSlot()
    def rollPressed(self, widget):
        print(self.chaSaveProficient.checkState())
        #statTuple = rollLink[widget]
        #mod = statTuple[0].checked()
        #roll.emit()
    
    
    '''
    Handles updating all derived values when a widget is changed
    
    widget: the widget containing the changed stat (QSpinBox)
    
    '''
    @pyqtSlot()
    def statUpdated(self, widget):
        mod = math.floor((widget.value()-10) / 2)
        prof = self.proficiency.value()
        
        #update regular mod
        self.statLink[widget][0][1].setValue(mod)
        
        #loop through derrived stats and update them (excluding first element which is the mod)
        for child in self.statLink[widget][1:]:
            #if proficient, add full proficiency
            if child[0].checkState() == 1:
                child[1].setValue(mod+prof)
            elif child[0].checkState() == 2: #if half proficient, add half proficiency
                child[1].setValue(mod + math.floor(prof/2))
            else: #else not proficient
                child[1].setValue(mod)
        
        #check initiative, and passive perception change as well
        if widget == self.wisScore: #if wis, passive perception
            if self.wisPerceptionProficient.checkState() == 1: #full proficient
                self.passivePerception.setValue(10+mod+prof)
            elif self.wisPerceptionProficient.checkState() == 2: #half proficient
                self.passivePerception.setValue(10+mod+math.floor(prof/2))
            else: #not proficient
                self.passivePerception.setValue(10+mod)
        elif widget == self.dexScore: #if dex, initiative
            self.initiative.setValue(mod)
        
        #check if spellcast needs to be updated
        if self.characterIsSpellcaster.isChecked():
            abl = self.spellAbility.text().upper()
            #if we are updating the stat that corresponds to the casting ability
            if abl == "INT" and widget == self.intScore or abl == "WIS" and widget == self.wisScore or abl == "CHA" and widget == self.chaScore:
                self.spellDC.setValue(8+mod+prof)
                self.spellAttack.setValue(mod+prof)
    
    
    '''
    Updates all skills, used after a proficiency value changes
    
    '''
    @pyqtSlot()
    def updateAllSkills(self):
        for abl in self.statLink.keys():
            self.statUpdated(abl)
    
    
    '''
    Defines a redirect slot to re-emit a name change signal from the widget to the main application
    
    '''
    @pyqtSlot()
    def nameChanged(self):
        self.nameChange.emit(self.characterName.text())
    
    
    '''
    Handles updating skill mods when a proficiency value changes
    
    state: the current state of the proficiency box
    
    skillBox: the skill line edit to be updated
    
    NOTE: do not need to add modifier, just subtract previous proficiency
    - 0 >> 1
    - 1 >> 2
    - 2 >> 0
    Follow the above transitions to subtract previous proficiency effect and recalculate
    
    '''
    @pyqtSlot(int)
    def skillProficiencyChanged(self, skillBox, state):
        mod = skillBox.value()
        prof = self.proficiency.value()
        if state == 1: #full proficient, was not proficient
            #set: mod >> mod+prof
            mod = mod+prof
        elif state == 2: #half proficient, was full proficient
            #set: mod >> mod-prof + prof/2
            mod = mod-prof + math.floor(prof/2)
        else: #not proficient, was half proficient
            #set: mod >> mod-prof/2
            mod = mod - math.floor(prof/2)
        
        #set value
        skillBox.setValue(mod)
        
        #if the skillBox is == self.wisPerceptionMod, we need to update 
        if skillBox == self.wisPerceptionMod:
            self.passivePerception.setValue(10+mod)
    
    
    
    '''
    Handles updating spellcasting abilities if the ability was changed
    
    Can assume is spellcaster, else the controls would not be visible
    
    '''
    @pyqtSlot()
    def spellAbilityChanged(self):
        prof = self.proficiency.value()
        abl = self.spellAbility.text().upper()
        mod = 0
        
        #check stat
        if abl == 'INT':
            mod = self.intMod.value()
        elif abl == 'WIS':
            mod = self.wisMod.value()
        elif abl == 'CHA':
            mod = self.chaMod.value()
        else:
            #else none of the applicable scores, leave alone for homebrew or strength casters, lol
            return
        
        #by above, only INT, WIS, or CHA casters should be here
        self.spellDC.setValue(8+prof+mod)
        self.spellAttack.setValue(prof+mod)
    
    
    
    '''
    Saves the form structure to a given file
    
    TODO: change saving/loading to go by groups, which will make the json file prettier for readers
    
    '''
    def saveToFile(self, fileName):
        #ignore underlying spinbox line, and the two 
        forbiddenList = ["qt_spinbox_lineedit", "spell", "spellPrepared"]
        #loop through attributes, link their names with their values
        saveDict = { atr.objectName(): self.genericReadWrite(atr, True) 
                    for atr in self.findChildren((QLineEdit, QSpinBox, QCheckBox, QPlainTextEdit, Spell)) 
                    if atr.objectName() not in forbiddenList}
                
        #save it yo
        with open(fileName, "w") as f:
            json.dump(saveDict, f, indent=4)
    
    
    '''
    Loads the form structure from a given file
    
    fileName: file to load from
    
    NOTE: throws exceptions if the file does not exist
    
    '''
    def loadFromFile(self, fileName):
        loadDict = None
        try:
            with open(fileName, "r") as f:
                loadDict = json.load(f)
            
            #now we have the dictionary from file, attempt to read and set fields
            for key,value in loadDict.items():
                #try to get it from self
                try:
                    #setFunction(attributeFromKey, argsFromValue)
                    self.genericReadWrite(getattr(self, key), False, value)
                except AttributeError as e:
                    #might be a dynamic widget, check spells
                    lst = getattr(self, key.split("_")[0])
                    self.genericReadWrite(lst.itemWidget(lst.item(int(key.split("_")[1]) - 1)), False, value)
                
        except (IOError, AttributeError, FileNotFoundError )as e:
            if type(e) == IOError or type(e) == AttributeError:
                raise IOError(str(e)) #"The character file could not be read. Perhaps it is corrupted?"
            else:
                raise FileNotFoundError("The character file could not be found.")
    
    
    '''
    Generic getter/setter for all savable fields, returns the callable function
    
    widget: widget to read to/write from
    
    read: true if we want to read, false if we want to write
    
    args: arguments for writing, only used when read = True
    
    '''
    def genericReadWrite(self, widget, read, args = None):
        if type(widget) == QLineEdit:
            if read:
                return widget.text()
            else:
                return widget.setText(args)
        elif type(widget) == QSpinBox:
            if read:
                return widget.value()
            else:
                return widget.setValue(args)
        elif type(widget) == QCheckBox:
            if read:
                #works for 2 and 3 state, but with int only
                return widget.checkState()
            else:
                #same as above
                return widget.setCheckState(args)
        elif type(widget) == QPlainTextEdit:
            if read:
                return widget.toPlainText()
            else:
                return widget.setPlainText(args)
        elif type(widget) == Spell:
            if read:
                return {"spell": widget.getSpell(), "prepared": widget.getPrepared()}
            else:
                widget.setSpell(args["spell"])
                widget.setPrepared(args["prepared"])
        else:
            raise TypeError("Generic reading and writing for character forms only supports savable fields: QLineEdit, QSpinBox, QCheckBox, QPlainTextEdit, Spell, given type " + str(type(widget)))

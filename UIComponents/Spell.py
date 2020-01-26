from .DesignerWidgets.SpellItem import *
from PyQt5.QtWidgets import QWidget, QSizePolicy
from PyQt5.QtCore import QSize

'''
A simple wrapper class to implement easier getter methods for fields

'''
class Spell(QWidget, Ui_spellItem):
    def __init__(self):
        super(QWidget, self).__init__()
        self.setupUi(self)
    
    
    def getSpell(self):
        return self.spell.text()
    
    def setSpell(self, val):
        self.spell.setText(val)
    
    def getPrepared(self):
        return self.spellPrepared.isChecked()
    
    def setPrepared(self, val):
        self.spellPrepared.setChecked(val)
    
    def sizeHint(self):
        return  QSize(30, 45)

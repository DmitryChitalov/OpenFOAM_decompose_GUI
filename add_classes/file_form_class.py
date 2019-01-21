# -*- coding: utf-8 -*-
from PyQt5 import QtSql
from PyQt5 import QtCore
import os

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QFormLayout, QTableWidget, QComboBox, \
    QSpinBox, QPushButton, QListWidgetItem, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout

#---------------------------Импорт модулей и внешних форм-------------------------

from forms.constant_forms.g_form import g_form_class
from forms.constant_forms.thermophysicalProperties_form import thermophysicalProperties_form_class
from forms.constant_forms.turbulenceProperties_form import turbulenceProperties_form_class
from forms.constant_forms.thermophysicalProperties_air_form import thermophysicalProperties_air_form_class
from forms.constant_forms.thermophysicalProperties_water_form import thermophysicalProperties_water_form_class

from forms.system_forms.controlDict_form import controlDict_form_class
from forms.system_forms.fvSchemes_form import fvSchemes_form_class
from forms.system_forms.decomposeParDict_form import decomposeParDict_form_class

from forms.forms_0.file_0_form import file_0_form_class
    
#-------------------------Возврат ссылок на формы параметров----------------------
    
class file_form_class:
    def inp_file_form_func(self, file_name, con):
        global file_form
        global file_name_gl
        
        file_name_gl = file_name
        connection = con
        par = self

        if  file_name_gl == "g":
            file_form = g_form_class(self)
		            
        elif  file_name_gl == "thermophysicalProperties":
            file_form = thermophysicalProperties_form_class(self)
			
        elif  file_name_gl == "thermophysicalProperties.air":
            file_form = thermophysicalProperties_air_form_class(self)
			
        elif  file_name_gl == "thermophysicalProperties.water":
            file_form = thermophysicalProperties_water_form_class(self)
		
        elif  file_name_gl == "turbulenceProperties":
            file_form = turbulenceProperties_form_class(self)
			
        elif  file_name_gl == "controlDict":
            file_form = controlDict_form_class(self)
			
        elif  file_name_gl == "fvSchemes":
            file_form = fvSchemes_form_class(self)
			
        elif  file_name_gl == "decomposeParDict":
            file_form = decomposeParDict_form_class(self)
		
        elif os.path.exists(par.full_dir + '/' + file_name_gl + '/'):
            file_name_gl = None
            file_form = None
			
        elif file_name_gl == "blockMeshDict" or file_name_gl == "snappyHexMeshDict":
            file_name_gl = 'md'
            file_form = None

        else:
            file_form = file_0_form_class(self)
          
    def out_file_name_func(): return file_name_gl
    def out_file_form_func(): return file_form



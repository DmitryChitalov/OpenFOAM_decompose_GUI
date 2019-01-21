# -*- coding: utf-8 -*-
#---------------------------Импорт модулей и внешних форм-------------------------#

from PyQt5 import QtCore
from PyQt5 import QtSql
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, QObject


from PyQt5.QtWidgets import QWidget, QFileDialog, QLineEdit, QLabel, \
    QHBoxLayout, QLineEdit, QPushButton, QGridLayout, \
    QFrame, QVBoxLayout, QFormLayout, QRadioButton, QDoubleSpinBox, \
	QSpinBox, QCheckBox, QGroupBox, QComboBox

import pickle
import os
import shutil
import re
import signal

from windows.msh_window import msh_window_class

from threads.msh_threads import msh_generation_thread
from threads.msh_threads import msh_visualisation_thread
from threads.solv_threads import solv_threads
from threads.solv_threads import solv_stop_thread
from threads.solv_threads import solv_visualisation_threads

from functions.solv_functions import solv_functions_class
from functions.msh_functions import msh_functions_class

class second_toolbar_functions_class():
	    
	#.......................Функция открытия окна выбора директории расчетной сетки.......................

    def on_msh_open(par):
        msh_win = msh_window_class(par)
        if par.interface_lng_val == 'Russian':
            msh_win.setWindowTitle('Окно выбора директории расчетной сетки')
        elif par.interface_lng_val == 'English':
            msh_win.setWindowTitle('Mesh directory selection window')
        msh_win.show()
		
    #...........................Функция запуска генерации расчетной сетки........................

    def on_msh_run(prj_path_val, mesh_name_txt_val, pp_dir, par, interface_lng_val, msh_type): 
        par.bm = msh_generation_thread(prj_path_val, mesh_name_txt_val, pp_dir, par, interface_lng_val, msh_type)
        par.bm.msh_start_sig.connect(msh_functions_class.on_msh_start, QtCore.Qt.QueuedConnection)
        par.bm.msh_fin_sig.connect(msh_functions_class.on_msh_finished, QtCore.Qt.QueuedConnection)
        par.bm.start()
		
	#...........................Функция запуска визуализации расчетной сетки.....................         

    def on_visual_msh_run(prj_path_val, mesh_name_txt_val, pp_dir, par, interface_lng_val, msh_type):
        par.mv = msh_visualisation_thread(prj_path_val, mesh_name_txt_val, pp_dir, par, interface_lng_val, msh_type)
        par.mv.msh_run_vis_start_sig.connect(msh_functions_class.on_msh_visual_run, QtCore.Qt.QueuedConnection)
        par.mv.msh_run_vis_finish_sig.connect(msh_functions_class.on_msh_visual_finished, QtCore.Qt.QueuedConnection)
        par.mv.start()
		
	#...............................Функция запуска решения...............................

    def on_solv_run(prj_path_val, mesh_name_txt_val, pp_dir, par, interface_lng_val, msh_type): 
		
        par.sr = solv_threads(prj_path_val, mesh_name_txt_val, pp_dir, par, interface_lng_val, msh_type)
        par.sr.solv_sig_start.connect(solv_functions_class.on_solv_start, QtCore.Qt.QueuedConnection)
        par.sr.solv_sig_fin.connect(solv_functions_class.on_solv_fin, QtCore.Qt.QueuedConnection)
        par.sr.start()
		
	#...............................Функция останова решения...............................
		
    def on_solv_stop(prj_path_val, mesh_name_txt_val, pp_dir, par, interface_lng_val, msh_type): 
		
        par.ss = solv_stop_thread(prj_path_val, mesh_name_txt_val, pp_dir, par, interface_lng_val, msh_type)
        par.ss.solv_stop_sig.connect(solv_functions_class.on_solv_stop_fin, QtCore.Qt.QueuedConnection)
        par.ss.start()
		
	#...........................Функция запуска визуализации результатов стресс-анализа.....................         

    def on_solv_vis(prj_path_val, mesh_name_txt_val, pp_dir, par, interface_lng_val, msh_type):

        par.sv = solv_visualisation_threads(prj_path_val, mesh_name_txt_val, pp_dir, par, interface_lng_val, msh_type)
        par.sv.solv_vis_start_sig.connect(solv_functions_class.on_solv_vis_start, QtCore.Qt.QueuedConnection)
        par.sv.solv_vis_fin_sig.connect(solv_functions_class.on_solv_vis_fin, QtCore.Qt.QueuedConnection)
        par.sv.start()
		

	
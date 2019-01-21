# -*- coding: utf-8 -*-
#---------------------------Импорт модулей и внешних форм-------------------------#

from PyQt5 import QtCore
from PyQt5 import QtSql
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal

from PyQt5.QtWidgets import QWidget, QFileDialog, QLineEdit, QLabel, \
    QHBoxLayout, QLineEdit, QPushButton, QGridLayout, \
    QFrame, QVBoxLayout, QFormLayout, QRadioButton, QDoubleSpinBox, \
	QSpinBox, QCheckBox, QGroupBox, QComboBox, QListWidgetItem

import os
import subprocess
import time
import shutil

#--------------------------------------Поток решения задачи МСС--------------------------------------------#

class solv_threads(QtCore.QThread):
	solv_sig_start = pyqtSignal('QString', 'QString', 'PyQt_PyObject', 'QString', 'QString')
	solv_sig_fin = pyqtSignal(int, 'QString', 'QString', 'PyQt_PyObject', 'QString', 'QString')
	def __init__(self, prj_path_val, mesh_name_txt_val, pp_dir, parent, interface_lng_val, msh_type):
		QtCore.QThread.__init__(self, parent)
		
		global prj_path_val_th
		global mesh_name_txt_val_th_a
		global mesh_name_txt_val_th_new
		global pp_dir_th
		global par
		global int_lng
		global msh_t
		
		prj_path_val_th = prj_path_val
		mesh_name_txt_val_th_new = mesh_name_txt_val
		pp_dir_th = pp_dir
		par = parent
		int_lng = interface_lng_val
		msh_t = msh_type
		
	def run(self):
		contDict_file = os.path.exists(par.full_dir + '/system/controlDict')
		if os.path.exists(contDict_file) == True:
			
				if msh_t == 'blockMesh':
					mesh_name_txt_val_th_a = mesh_name_txt_val_th_new + '_blockMesh'
				elif msh_t == 'snappyHexMesh':
					mesh_name_txt_val_th_a = mesh_name_txt_val_th_new + '_snappyHexMesh'
				
				#1

				solv_bash_file = open(prj_path_val_th + '/' + mesh_name_txt_val_th_a + '/' + 'solv_script', 'w')
				solv_bash_file.write('#!/bin/sh' + '\n' + '. /opt/openfoam6/etc/bashrc' + '\n' + 'setFields' + '\n' + 'exit')
				solv_bash_file.close()

				solv_out_file = open(prj_path_val_th + '/' + mesh_name_txt_val_th_a + '/' + 'solv_script.log', "w")
				solv_run_subprocess_a = subprocess.Popen(["bash " + prj_path_val_th + '/' + mesh_name_txt_val_th_a + "/" + "solv_script"], cwd = pp_dir_th, shell=True, stdout=solv_out_file, stderr=solv_out_file)
				solv_out_file.close()
				
				self.solv_sig_start.emit(prj_path_val_th, mesh_name_txt_val_th_a, par, int_lng, msh_t)
				
				#2
				
				solv_bash_file = open(prj_path_val_th + '/' + mesh_name_txt_val_th_a + '/' + 'solv_script', 'w')
				solv_bash_file.write('#!/bin/sh' + '\n' + '. /opt/openfoam6/etc/bashrc' + '\n' + 'decomposePar' + '\n' + 'exit')
				solv_bash_file.close()

				solv_out_file = open(prj_path_val_th + '/' + mesh_name_txt_val_th_a + '/' + 'solv_script.log', "w")
				solv_run_subprocess_b = subprocess.Popen(["bash " + prj_path_val_th + '/' + mesh_name_txt_val_th_a + "/" + "solv_script"], cwd = pp_dir_th, shell=True, stdout=solv_out_file, stderr=solv_out_file)
				solv_out_file.close()
				
				#3
				
				solv_bash_file = open(prj_path_val_th + '/' + mesh_name_txt_val_th_a + '/' + 'solv_script', 'w')
				solv_bash_file.write('#!/bin/sh' + '\n' + '. /opt/openfoam6/etc/bashrc' + '\n' + par.application + '\n' + 'exit')
				solv_bash_file.close()

				solv_out_file = open(prj_path_val_th + '/' + mesh_name_txt_val_th_a + '/' + 'solv_script.log', "w")
				solv_run_subprocess = subprocess.Popen(["bash " + prj_path_val_th + '/' + mesh_name_txt_val_th_a + "/" + "solv_script"], cwd = pp_dir_th, shell=True, stdout=solv_out_file, stderr=solv_out_file)
				solv_out_file.close()
				
				while solv_run_subprocess.poll() is None:
					pass
				return_code_1 = solv_run_subprocess.returncode
				
				if return_code_1 == 0:
					solv_bash_file = open(prj_path_val_th + '/' + mesh_name_txt_val_th_a + '/' + 'solv_script', 'w')
					solv_bash_file.write('#!/bin/sh' + '\n' + '. /opt/openfoam6/etc/bashrc' + '\n' + 'reconstructPar' + '\n' + 'exit')
					solv_bash_file.close()
					
					solv_out_file = open(prj_path_val_th + '/' + mesh_name_txt_val_th_a + '/' + 'solv_script.log', "w")
					solv_run_subprocess = subprocess.Popen(["bash " + prj_path_val_th + '/' + mesh_name_txt_val_th_a + "/" + "solv_script"], cwd = pp_dir_th, shell=True, stdout=solv_out_file, stderr=solv_out_file)
					solv_out_file.close()
					
					while solv_run_subprocess.poll() is None:
						pass
					return_code = solv_run_subprocess.returncode

					self.solv_sig_fin.emit(return_code, prj_path_val_th, mesh_name_txt_val_th_a, par, int_lng, msh_t)
				else:
					self.solv_sig_fin.emit(return_code_1, prj_path_val_th, mesh_name_txt_val_th_a, par, int_lng, msh_t)

		else:
			if int_lng == 'Russian':
				msg_lbl = QLabel('<span style="color:blue">' + "Сначала выполните сохранение файла controlDict" + '</span>')
			elif int_lng == 'English':
				msg_lbl = QLabel('<span style="color:blue">' + "First save the controlDict file"+ '</span>')

			par.listWidget.clear()
			par.item = QListWidgetItem()
			par.listWidget.addItem(par.item)
			par.listWidget.setItemWidget(par.item, msg_lbl)

#----------------------------------Поток останова решения------------------------------------#
			
class solv_stop_thread(QtCore.QThread):
    solv_stop_sig = pyqtSignal(int, 'QString', 'QString', 'PyQt_PyObject', 'QString', 'QString')
    def __init__(self, prj_path_val, mesh_name_txt_val, pp_dir, parent, interface_lng_val, msh_type):
        QtCore.QThread.__init__(self, parent)

        global prj_path_val_th
        global mesh_name_txt_val_th
        global pp_dir_th
        global par
        global int_lng
        global msh_t

        prj_path_val_th = prj_path_val
        mesh_name_txt_val_th_new = mesh_name_txt_val
        pp_dir_th = pp_dir
        par = parent
        int_lng = interface_lng_val
        msh_t = msh_type
    def run(self):
        if msh_t == 'blockMesh':
            mesh_name_txt_val_th_a = mesh_name_txt_val_th_new + '_blockMesh'
        elif msh_t == 'snappyHexMesh':
            mesh_name_txt_val_th_a = mesh_name_txt_val_th_new + '_snappyHexMesh'
		
        vspom = open(prj_path_val_th + '/' + mesh_name_txt_val_th_a + '/' + 'KILL_PROC_BASH', 'w')
        vspom.write('#!/bin/sh' + '\n' + '. /opt/openfoam6/etc/bashrc' + '\n' + 'pidof ' + par.application + '\n' + 'exit')
        vspom.close()

        vspom_file = open(prj_path_val_th + '/' + mesh_name_txt_val_th_a + '/' + "out_kill.log", "w")
        vspom_proc = subprocess.Popen(["bash " + prj_path_val_th + '/' + mesh_name_txt_val_th_a + '/' + "KILL_PROC_BASH"], cwd = prj_path_val_th + '/' + mesh_name_txt_val_th_a, shell = True, stdout=vspom_file, stderr=vspom_file)
        while vspom_proc.poll() is None:
            pass
			
        return_code = vspom_proc.returncode	
		
        self.solv_stop_sig.emit(return_code, prj_path_val_th, mesh_name_txt_val_th_a, par, int_lng, msh_t)

#--------------------------------------Поток визуализации результатов---------------------------------------#
			
class solv_visualisation_threads(QtCore.QThread):
	solv_vis_start_sig = pyqtSignal('PyQt_PyObject', 'QString', 'QString')
	solv_vis_fin_sig = pyqtSignal(int, 'QString', 'QString', 'PyQt_PyObject', 'QString', 'QString')
	def __init__(self, prj_path_val, mesh_name_txt_val, pp_dir, parent, interface_lng_val, msh_type):
		QtCore.QThread.__init__(self, parent)
		
		global prj_path_val_th
		global mesh_name_txt_val_th
		global pp_dir_th
		global par
		global int_lng
		global msh_t

		prj_path_val_th = prj_path_val
		mesh_name_txt_val_th_new = mesh_name_txt_val
		pp_dir_th = pp_dir
		par = parent
		int_lng = interface_lng_val
		msh_t = msh_type
		
	def run(self):
		self.solv_vis_start_sig.emit(par, int_lng, msh_t)
		if msh_t == 'blockMesh':
			mesh_name_txt_val_th_a = mesh_name_txt_val_th_new + '_blockMesh'
			
		elif msh_t == 'snappyHexMesh':
			mesh_name_txt_val_th_a = mesh_name_txt_val_th_new + '_snappyHexMesh'

		solv_vis_bash_file = open(prj_path_val_th + '/' + mesh_name_txt_val_th_a + '/' + 'solv_vis_script', 'w')
		solv_vis_bash_file.write('#!/bin/sh' + '\n' + '. /opt/openfoam6/etc/bashrc' + '\n' + 'paraFoam' + '\n' + 'exit')
		solv_vis_bash_file.close()

		solv_vis_out_file = open(prj_path_val_th + '/' + mesh_name_txt_val_th_a + '/' + 'solv_vis_script.log', "w")
		solv_vis_run_subprocess = subprocess.Popen(["bash " + prj_path_val_th + '/' + mesh_name_txt_val_th_a + "/" + "solv_vis_script"], cwd = pp_dir_th, shell=True, stdout=solv_vis_out_file, stderr=solv_vis_out_file)
		solv_vis_out_file.close()

		while solv_vis_run_subprocess.poll() is None:
			time.sleep(0.3)

		return_code = solv_vis_run_subprocess.returncode

		self.solv_vis_fin_sig.emit(return_code, prj_path_val_th, mesh_name_txt_val_th_a, par, int_lng, msh_t)

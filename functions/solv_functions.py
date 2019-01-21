# -*- coding: utf-8 -*-
#---------------------------Импорт модулей и внешних форм-------------------------#

from PyQt5 import QtCore
from PyQt5 import QtSql
from PyQt5 import QtGui

from PyQt5.QtWidgets import QWidget, QFileDialog, QLineEdit, QLabel, \
    QHBoxLayout, QLineEdit, QPushButton, QGridLayout, \
    QFrame, QVBoxLayout, QFormLayout, QRadioButton, QDoubleSpinBox, \
	QSpinBox, QCheckBox, QGroupBox, QComboBox, QListWidgetItem

import pickle
import os
import shutil
import re
import signal

class solv_functions_class():		
	
	###..............................Функция при старте решения..........................### 
	
	def on_solv_start(prj_path_val_th, mesh_name_txt_val_th, par, int_lng, msh_t):

		if int_lng == 'Russian':
			msg_lbl = QLabel('<span style="color:blue">' + "Выполняется решение задачи" + '</span>')
		elif int_lng == 'English':
			msg_lbl = QLabel('<span style="color:blue">' + "Solving the problem" + '</span>')
			
		par.solv_stop.setEnabled(True)

		par.listWidget.clear()
		par.item = QListWidgetItem()
		par.listWidget.addItem(par.item)
		par.listWidget.setItemWidget(par.item, msg_lbl)
	
	###..............................Функция при останове решения..........................### 
		
	def on_solv_stop_fin(return_code, prj_path_val_th, mesh_name_txt_val_th, par, int_lng, msh_t):

		if return_code == 0:
			       
			f_o = open(prj_path_val_th + '/' + mesh_name_txt_val_th + '/' + "out_kill.log", "r")
			data = f_o.read()
			f_o.close()

			con_reg = re.compile(r"\d*")
			con_mas = con_reg.findall(data)
			proc_to_kill = con_mas[0]

			os.kill(int(proc_to_kill), signal.SIGKILL)

			if int_lng == 'Russian':
				msg_lbl = QLabel('<span style="color:red">' + "Процесс решения остановлен" + '</span>')
			elif int_lng == 'English':
				msg_lbl = QLabel('<span style="color:red">' + "Process of solving stopped" + '</span>')

			par.listWidget.clear()
			par.item = QListWidgetItem()
			par.listWidget.addItem(par.item)
			par.listWidget.setItemWidget(par.item, msg_lbl)
			
	###..............................Функция при завершении решения..........................### 
	
	def on_solv_fin(return_code, prj_path_val_th, mesh_name_txt_val_th, par, int_lng, msh_t):

		solv_fin_read_file = open(prj_path_val_th + '/' + mesh_name_txt_val_th + "/solv_script.log")
		data = solv_fin_read_file.read()

		if int_lng == 'Russian':
			par.outf_lbl.setText('Результаты решения задачи') 
		elif int_lng == 'English':
			par.outf_lbl.setText('The results of solving the problem') 
		par.cdw.setWidget(par.outf_scroll)
		par.cdw.setTitleBarWidget(par.cdw_frame)
		par.outf_edit.setText(data)

		if return_code == 0:
			if int_lng == 'Russian':
				msg_lbl = QLabel('<span style="color:green">' + "Решение задачи успешно завершено" + '</span>')
			elif int_lng == 'English':
				msg_lbl = QLabel('<span style="color:green">' + "Problem solving completed successfully" + '</span>')

			par.msh_visual.setEnabled(True)
			par.solv_run_vis.setEnabled(True)

		else:
			if int_lng == 'Russian':
				msg_lbl = QLabel('<span style="color:red">' + "Решение задачи завершено с ошибками" + '</span>')
			elif int_lng == 'English':
				msg_lbl = QLabel('<span style="color:red">' + "Problem solving completed with errors" + '</span>')
					
		par.listWidget.clear()
		par.item = QListWidgetItem()
		par.listWidget.addItem(par.item)
		par.listWidget.setItemWidget(par.item, msg_lbl)
		
		if os.path.exists(par.full_dir + '/solv_script'):
			os.remove(par.full_dir + '/solv_script')
		if os.path.exists(par.full_dir + '/solv_script.log'):
			os.remove(par.full_dir + '/solv_script.log')
			
	###..............................Функция при старте визуализации результатов решения..........................### 
		
	def on_solv_vis_start(par, int_lng, msh_t):
		
		if int_lng == 'Russian':
			msg_lbl = QLabel('<span style="color:blue">' + "Визуализация результатов решения запущена" + '</span>')
		elif int_lng == 'English':
			msg_lbl = QLabel('<span style="color:blue">' + "Solution results visualization started" + '</span>')
					
		par.listWidget.clear()
		par.item = QListWidgetItem()
		par.listWidget.addItem(par.item)
		par.listWidget.setItemWidget(par.item, msg_lbl)
		
	###..............................Функция при завершении визуализации результатов решения..........................### 
		
	def on_solv_vis_fin(return_code, prj_path_val_th, mesh_name_txt_val_th, par, int_lng, msh_t):

		solv_vis_read_file = open(prj_path_val_th + '/' + mesh_name_txt_val_th + "/solv_vis_script.log")
		data = solv_vis_read_file.read()

		if int_lng == 'Russian':
			par.outf_lbl.setText('Результаты визуализации') 
		elif int_lng == 'English':
			par.outf_lbl.setText('Visualisation results') 
		par.cdw.setWidget(par.outf_scroll)
		par.cdw.setTitleBarWidget(par.cdw_frame)
		par.outf_edit.setText(data)

		if return_code == 0:
			if int_lng == 'Russian':
				msg_lbl = QLabel('<span style="color:green">' + "Визуализация результатов решения успешно завершена" + '</span>')
			elif int_lng == 'English':
				msg_lbl = QLabel('<span style="color:green">' + "Visualization of the solution results completed successfully" + '</span>')

		else:
			if int_lng == 'Russian':
				msg_lbl = QLabel('<span style="color:red">' + "При отображении результатов решения возникли проблемы" + '</span>')
			elif int_lng == 'English':
				msg_lbl = QLabel('<span style="color:red">' + "There are problems when displaying solution results." + '</span>')
			color = QtGui.QColor("red")

		par.listWidget.clear()
		par.item = QListWidgetItem()
		par.listWidget.addItem(par.item)
		par.listWidget.setItemWidget(par.item, msg_lbl)	
		
		if os.path.exists(par.full_dir + '/solv_vis_script'):
			os.remove(par.full_dir + '/solv_vis_script')
		if os.path.exists(par.full_dir + '/solv_vis_script.log'):
			os.remove(par.full_dir + '/solv_vis_script.log')
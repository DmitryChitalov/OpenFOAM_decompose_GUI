# -*- coding: utf-8 -*-
# -------------------------------Импорт модулей----------------------------------

import shutil
import sys
import re
import os
import os.path

from PyQt5 import QtCore
from PyQt5 import QtSql
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QFileDialog, QLineEdit, QLabel, \
    QHBoxLayout, QLineEdit, QPushButton, QGridLayout, \
    QFrame, QVBoxLayout, QFormLayout, QFileDialog, QRadioButton, QStyle, \
    QComboBox, QFrame, QListWidgetItem 

# ---------------------------Главная форма проекта-------------------------------

class files_0_window_class(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowSystemMenuHint)
        self.setWindowModality(QtCore.Qt.WindowModal)

        global par
        par = parent

        global int_lng
        int_lng = par.interface_lng_val
		
		# ------------------------------------Первый блок формы--------------------------------------
		
        if int_lng == 'Russian':
            file_create_lbl = QLabel("Укажите имя файла:")
        elif int_lng == 'English':
            file_create_lbl = QLabel("Enter file name:")
        file_hbox = QHBoxLayout()
        file_hbox.addWidget(file_create_lbl)
        self.file_edit = QLineEdit()
        self.file_edit.setFixedSize(200, 27)
        file_hbox.addWidget(self.file_edit)
		
        if int_lng == 'Russian':
            object_create_lbl = QLabel("Укажите имя объекта:")
        elif int_lng == 'English':
            object_create_lbl = QLabel("Enter object name:")
        object_hbox = QHBoxLayout()
        object_hbox.addWidget(object_create_lbl)
        self.object_edit = QLineEdit()
        self.object_edit.setFixedSize(200, 27)
        object_hbox.addWidget(self.object_edit)
		
        block_grid = QGridLayout()
        block_grid.addLayout(file_hbox, 0, 0)
        block_grid.addLayout(object_hbox, 1, 0)
		
        # ---------------------Кнопки сохранения и отмены и их блок-------------------------
		
        if int_lng == 'Russian':
            save_button = QPushButton("Сохранить")
            cancel_button = QPushButton("Отмена")
        elif int_lng == 'English':
            save_button = QPushButton("Save")
            cancel_button = QPushButton("Cancel")

        save_button.setFixedSize(80, 25)
        save_button.clicked.connect(self.on_save_clicked)
        cancel_button.setFixedSize(80, 25)
        cancel_button.clicked.connect(self.on_cancel_clicked)
        buttons_hbox = QHBoxLayout()
        buttons_hbox.addWidget(save_button)
        buttons_hbox.addWidget(cancel_button)

        # -------------------------Фрейм формы---------------------------

        bound_grid = QGridLayout()
        bound_grid.addLayout(block_grid, 0, 0, alignment=QtCore.Qt.AlignCenter)
        bound_grid.addLayout(buttons_hbox, 1, 0, alignment=QtCore.Qt.AlignCenter)
        bound_frame = QFrame()
        bound_frame.setStyleSheet(open("./styles/properties_form_style.qss", "r").read())
        bound_frame.setLayout(bound_grid)
        bound_vbox = QVBoxLayout()
        bound_vbox.addWidget(bound_frame)

        # --------------------Размещение на форме всех компонентов---------

        form_1 = QFormLayout()
        form_1.addRow(bound_vbox)
        self.setLayout(form_1)

	# .....................Функция, запускаемая при нажатии кнопки "отмена"......................

    def on_cancel_clicked(self):
        self.close()
		
	# .....................Функция, запускаемая при нажатии кнопки "сохранить"......................
		
    def on_save_clicked(self):
        file_edit_txt = self.file_edit.text()
        object_edit_txt = self.object_edit.text()

        if file_edit_txt != '':
            if not os.path.exists(par.full_dir + '/0/' + file_edit_txt):
               
                dir_0_name = os.path.basename(par.full_dir + '/0')
                item = par.treeview.model.item(2, 0)
                child_item_0 = QtGui.QStandardItem(file_edit_txt)
                child_item_0.setForeground(QtGui.QColor('navy'))
                count = len([f for f in os.listdir(par.full_dir + '/0/') if os.path.isfile(os.path.join(par.full_dir + '/0/', f))])

                if count == 0:
                    item.setChild(0, 0, child_item_0)
                else:
                    item.setChild(count, 0, child_item_0)
				 
                index_0 = par.treeview.model.index(2, 0)
                par.treeview.expand(index_0)
				
                par.file_0_name = file_edit_txt	
                query = QtSql.QSqlQuery()
                if 'objects_pars' not in par.con.tables():	
                    
                    query.exec("CREATE TABLE objects_pars(file_name, object_name)")

                query.exec("INSERT INTO objects_pars(file_name, object_name) VALUES ('%s','%s')" % (file_edit_txt, object_edit_txt))
					
                self.close()

            else:
                if int_lng == 'Russian':
                    msg_lbl = QLabel(
                        '<span style="color:red">Указанный файл уже существует</span>')
                elif int_lng == 'English':
                    msg_lbl = QLabel(
                        '<span style="color:red">That file exists</span>')
					
                par.listWidget.clear()
                par.item = QListWidgetItem()
                par.listWidget.addItem(par.item)
                par.listWidget.setItemWidget(par.item, msg_lbl)

        else:
            if int_lng == 'Russian':
                msg_lbl = QLabel(
                    '<span style="color:red">Укажите имя файла</span>')
            elif int_lng == 'English':
                msg_lbl = QLabel(
                    '<span style="color:red">Set the file name</span>')

            par.listWidget.clear()
            par.item = QListWidgetItem()
            par.listWidget.addItem(par.item)
            par.listWidget.setItemWidget(par.item, msg_lbl)
				
            
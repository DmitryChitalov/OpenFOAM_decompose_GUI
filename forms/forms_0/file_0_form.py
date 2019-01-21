# -*- coding: utf-8 -*-
# -----------------------------Импорт модулей-----------------------------------

from PyQt5 import QtSql
from PyQt5 import QtCore

import os
import os.path
import shutil
import re

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QFormLayout, QTableWidget, QComboBox, \
    QSpinBox, QPushButton, QListWidgetItem, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout

# -----------------------------------Форма--------------------------------------

class file_0_form_class(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
		
        self.interface_lng_val = parent.interface_lng_val
        self.con = parent.con
        self.full_dir = parent.full_dir
        self.par = parent
		
        if self.con.open():
            if 'patches' in self.con.tables():
                self.patches_lst = []
                query = QtSql.QSqlQuery('SELECT * FROM patches')
                query.exec_()
                while query.next():
                    rec = query.value('patch_name')
                    self.patches_lst.append(rec)

                self.table = QTableWidget(len(self.patches_lst) + 3, 2)
                self.table.setColumnWidth(0, 150)
                self.table.setColumnWidth(1, 460)
                self.table.setFixedSize(674, 480)
                if self.interface_lng_val == 'Russian':
                    self.table.setHorizontalHeaderLabels(["Параметр", "Значение"])
                elif self.interface_lng_val == 'English':
                    self.table.setHorizontalHeaderLabels(["Parameter", "Value"])

                # dimensions
                dimensions_lbl = QLabel('dimensions')
                self.d_1 = QLineEdit()
                self.d_1.setFixedSize(40, 25)
                self.d_2 = QLineEdit()
                self.d_2.setFixedSize(40, 25)
                self.d_3 = QLineEdit()
                self.d_3.setFixedSize(40, 25)
                self.d_4 = QLineEdit()
                self.d_4.setFixedSize(40, 25)
                self.d_5 = QLineEdit()
                self.d_5.setFixedSize(40, 25)
                self.d_6 = QLineEdit()
                self.d_6.setFixedSize(40, 25)
                self.d_7 = QLineEdit()
                self.d_7.setFixedSize(40, 25)
                self.dimensions_hbox = QHBoxLayout()
                self.dimensions_hbox.addWidget(self.d_1)
                self.dimensions_hbox.addWidget(self.d_2)
                self.dimensions_hbox.addWidget(self.d_3)
                self.dimensions_hbox.addWidget(self.d_4)
                self.dimensions_hbox.addWidget(self.d_5)
                self.dimensions_hbox.addWidget(self.d_6)
                self.dimensions_hbox.addWidget(self.d_7)
                self.dimensions_w = QWidget()
                self.dimensions_w.setLayout(self.dimensions_hbox)
                self.table.setCellWidget(0, 1, self.dimensions_w)
                self.table.setCellWidget(0, 0, dimensions_lbl)
                self.table.setRowHeight(0, 40)

                # internalField
                internalField_lbl = QLabel('internalField')
                self.internalField = QComboBox()
                self.internalField.setFixedSize(100, 25)
                internalField_list = ["uniform"]
                self.internalField.addItems(internalField_list)
                self.x = QLineEdit()
                self.x.setFixedSize(40, 25)
                self.y = QLineEdit()
                self.y.setFixedSize(40, 25)
                self.z = QLineEdit()
                self.z.setFixedSize(40, 25)
                self.internalField_hbox = QHBoxLayout()
                self.internalField_hbox.addWidget(self.internalField)
                self.internalField_hbox.addWidget(self.x)
                self.internalField_hbox.addWidget(self.y)
                self.internalField_hbox.addWidget(self.z)
                self.internalField_w = QWidget()
                self.internalField_w.setLayout(self.internalField_hbox)
                self.table.setCellWidget(1, 1, self.internalField_w)
                self.table.setCellWidget(1, 0, internalField_lbl)
                self.table.setRowHeight(1, 40)
				
                # вывод значений параметров
                if self.par.file_name in self.con.tables() and self.par.lock_bool == True:						
                    query = QtSql.QSqlQuery()
                    query.exec("SELECT * FROM " + self.par.file_name)
                    if query.isActive():
                        query.first()
                        value_list = []
                        while query.isValid():
                            value_res = query.value('value')
                            value_list.append(value_res)
                            query.next()
							
                        # dimensions
                        self.d_1.setText(value_list[0].split(' ')[0])
                        self.d_2.setText(value_list[0].split(' ')[1])
                        self.d_3.setText(value_list[0].split(' ')[2])
                        self.d_4.setText(value_list[0].split(' ')[3])
                        self.d_5.setText(value_list[0].split(' ')[4])
                        self.d_6.setText(value_list[0].split(' ')[5])
                        self.d_7.setText(value_list[0].split(' ')[6])
						
                        # internalField
                        internalField_mas = self.internalField.count()   
                        for i in range(internalField_mas):
                            if self.internalField.itemText(i) == value_list[1].split(', ')[0]:
                                self.internalField.setCurrentIndex(i)
                        #print(value_list[1])
                        #!!!!!
                        if len(value_list[1].split(', ')) == 4: 
                            self.x.setText(value_list[1].split(', ')[1])
                            self.y.setText(value_list[1].split(', ')[2])
                            self.z.setText(value_list[1].split(', ')[3])
                        else:
                            self.x.setText(value_list[1].split(', ')[1])
							
                # boundaryField
                boundaryField_lbl = QLabel('boundaryField')
                self.table.setCellWidget(2, 0, boundaryField_lbl)

                # patches
                k = 3
                self.type_list_main = []
                self.main_grid_list = []
                self.traction_list = []
                self.xyz_1_list_main = []
                self.pressure_list = []
                self.koord_list = []
                self.value_list = []
                self.xyz_2_list_main = []
                self.traction_lbl_list = []
                self.pressure_lbl_list = []
                self.value_lbl_list = []
                self.main_koord_list = []
                j = 2
                bvc = 0
                for el_p in self.patches_lst:
                    el_p_lbl = QLabel(el_p)

                    # type
                    self.type_lbl = QLabel('type:')
                    self.type = QComboBox()
                    self.type.setFixedSize(150, 25)
                    self.type_list = ["symmetryPlane", "tractionDisplacement", "empty", "zeroGradient", "noSlip", "calculated"]
                    self.type.addItems(self.type_list)
                    self.main_grid = QGridLayout()
                    self.main_grid.addWidget(self.type_lbl, 0, 0, alignment=QtCore.Qt.AlignLeft)
                    self.main_grid.addWidget(self.type, 0, 1, alignment=QtCore.Qt.AlignLeft)
                    self.main_grid.setRowStretch(0, 6500)
                    self.table.setRowHeight(k, 40)
                    self.type_list_main.append(self.type)
                    self.main_grid_list.append(self.main_grid)

                    # traction
                    traction_lbl = QLabel('traction:')
                    self.traction_lbl_list.append(traction_lbl)
                    traction = QComboBox()
                    traction_list = ["uniform", "demo"]
                    traction.addItems(traction_list)
                    x_1 = QLineEdit()
                    x_1.setFixedSize(40, 25)
                    y_1 = QLineEdit()
                    y_1.setFixedSize(40, 25)
                    z_1 = QLineEdit()
                    z_1.setFixedSize(40, 25)
                    xyz_1_list = [x_1, y_1, z_1]
                    self.traction_list.append(traction)
                    self.xyz_1_list_main.append(xyz_1_list)

                    # pressure
                    pressure_lbl = QLabel('pressure:')
                    self.pressure_lbl_list.append(pressure_lbl)
                    pressure = QComboBox()
                    pressure_list = ["uniform", "demo"]
                    pressure.addItems(pressure_list)
                    koord = QLineEdit()
                    koord.setFixedSize(40, 25)
                    self.pressure_list.append(pressure)
                    self.koord_list.append(koord)

                    # value
                    value_lbl = QLabel('value:')
                    self.value_lbl_list.append(value_lbl)
                    value = QComboBox()
                    value_list_el = ["uniform", "demo"]
                    value.addItems(value_list_el)
                    x_2 = QLineEdit()
                    x_2.setFixedSize(40, 25)
                    y_2 = QLineEdit()
                    y_2.setFixedSize(40, 25)
                    z_2 = QLineEdit()
                    z_2.setFixedSize(40, 25)
                    xyz_2_list = [x_2, y_2, z_2]
                    main_koord = QLineEdit()
                    main_koord.setFixedSize(40, 25)
                    self.value_list.append(value)
                    self.xyz_2_list_main.append(xyz_2_list)
                    self.main_koord_list.append(main_koord)
					
                    # вывод значений параметров
                    if self.par.file_name in self.con.tables():						
                        query = QtSql.QSqlQuery()
                        query.exec("SELECT * FROM " + self.par.file_name)
                        if query.isActive():
                            query.first()
                            value_list = []
                            while query.isValid():
                                value_res = query.value('value')
                                value_list.append(value_res)
                                query.next()

                            type_mas = self.main_grid_list[bvc].itemAtPosition(0, 1).widget().count()   
                            for i in range(type_mas):
                                if ',' in value_list[j]:
                                    if self.main_grid_list[bvc].itemAtPosition(0, 1).widget().itemText(i) == value_list[j].split(', ')[0]:
                                        self.main_grid_list[bvc].itemAtPosition(0, 1).widget().setCurrentIndex(i)
                                else:
                                    if self.main_grid_list[bvc].itemAtPosition(0, 1).widget().itemText(i) == value_list[j]:
                                        self.main_grid_list[bvc].itemAtPosition(0, 1).widget().setCurrentIndex(i)
										
                            if self.main_grid_list[bvc].itemAtPosition(0, 1).widget().currentText() == 'tractionDisplacement':										
                                self.main_grid_list[bvc].addWidget(self.traction_lbl_list[bvc], 1, 0, alignment=QtCore.Qt.AlignLeft)
                                self.main_grid_list[bvc].addWidget(self.traction_list[bvc], 1, 1, alignment=QtCore.Qt.AlignLeft)
                                self.main_grid_list[bvc].addWidget(self.xyz_1_list_main[bvc][0], 1, 2, alignment=QtCore.Qt.AlignLeft)
                                self.main_grid_list[bvc].addWidget(self.xyz_1_list_main[bvc][1], 1, 3, alignment=QtCore.Qt.AlignLeft)
                                self.main_grid_list[bvc].addWidget(self.xyz_1_list_main[bvc][2], 1, 4, alignment=QtCore.Qt.AlignLeft)

                                self.main_grid_list[bvc].addWidget(self.pressure_lbl_list[bvc], 2, 0, alignment=QtCore.Qt.AlignLeft)
                                self.main_grid_list[bvc].addWidget(self.pressure_list[bvc], 2, 1, alignment=QtCore.Qt.AlignLeft)
                                self.main_grid_list[bvc].addWidget(self.koord_list[bvc], 2, 2, alignment=QtCore.Qt.AlignLeft)

                                self.main_grid_list[bvc].addWidget(self.value_lbl_list[bvc], 3, 0, alignment=QtCore.Qt.AlignLeft)
                                self.main_grid_list[bvc].addWidget(self.value_list[bvc], 3, 1, alignment=QtCore.Qt.AlignLeft)
                                if len(value_list[j].split(', ')) == 3:
                                    self.main_grid_list[bvc].addWidget(self.xyz_2_list_main[bvc][0], 3, 2, alignment=QtCore.Qt.AlignLeft)
                                    self.main_grid_list[bvc].addWidget(self.xyz_2_list_main[bvc][1], 3, 3, alignment=QtCore.Qt.AlignLeft)
                                    self.main_grid_list[bvc].addWidget(self.xyz_2_list_main[bvc][2], 3, 4, alignment=QtCore.Qt.AlignLeft)
                                    
                                    self.table.setRowHeight(bvc + 3, 120)
                                    self.main_grid_list[bvc].itemAtPosition(3, 2).widget().setText(value_list[j].split(', ')[8])
                                    self.main_grid_list[bvc].itemAtPosition(3, 3).widget().setText(value_list[j].split(', ')[9])
                                    self.main_grid_list[bvc].itemAtPosition(3, 4).widget().setText(value_list[j].split(', ')[10])
                                else:
                                    self.main_grid_list[bvc].addWidget(self.main_koord_list[bvc], 3, 2, alignment=QtCore.Qt.AlignLeft)
                                    self.main_grid_list[bvc].itemAtPosition(3, 2).widget().setText(value_list[j])
							
                                # traction
                            
                                traction_mas = self.main_grid_list[bvc].itemAtPosition(1, 1).widget().count()   
                                for i in range(traction_mas):
                                    if self.main_grid_list[bvc].itemAtPosition(1, 1).widget().itemText(i) == value_list[j].split(', ')[1]:
                                        self.main_grid_list[bvc].itemAtPosition(1, 1).widget().setCurrentIndex(i)
										
                                self.main_grid_list[bvc].itemAtPosition(1, 2).widget().setText(value_list[j].split(', ')[2])
                                self.main_grid_list[bvc].itemAtPosition(1, 3).widget().setText(value_list[j].split(', ')[3])
                                self.main_grid_list[bvc].itemAtPosition(1, 4).widget().setText(value_list[j].split(', ')[4])
										
                                # pressure
                                pressure_mas = self.main_grid_list[bvc].itemAtPosition(2, 1).widget().count()   
                                for i in range(pressure_mas):
                                    if self.main_grid_list[bvc].itemAtPosition(2, 1).widget().itemText(i) == value_list[j].split(', ')[5]:
                                        self.main_grid_list[bvc].itemAtPosition(2, 1).widget().setCurrentIndex(i)
										 
                                self.main_grid_list[bvc].itemAtPosition(2, 2).widget().setText(value_list[j].split(', ')[6])
                            
                            # value
                            if self.main_grid_list[bvc].itemAtPosition(0, 1).widget().currentText() == 'calculated':
								
                                self.main_grid_list[bvc].addWidget(self.value_lbl_list[bvc], 3, 0, alignment=QtCore.Qt.AlignLeft)
                                self.main_grid_list[bvc].addWidget(self.value_list[bvc], 3, 1, alignment=QtCore.Qt.AlignLeft)
                                self.main_grid_list[bvc].addWidget(self.main_koord_list[bvc], 3, 2, alignment=QtCore.Qt.AlignLeft)
                                self.table.setRowHeight(bvc + 3, 70)
			
                                value_mas = self.main_grid_list[bvc].itemAtPosition(3, 1).widget().count()   
                                for i in range(value_mas):
                                    if self.main_grid_list[bvc].itemAtPosition(3, 1).widget().itemText(i) == value_list[j].split(', ')[1]:
                                        self.main_grid_list[bvc].itemAtPosition(3, 1).widget().setCurrentIndex(i)
									
                                self.main_grid_list[bvc].itemAtPosition(3, 2).widget().setText(value_list[j].split(', ')[2])                           

                    self.main_w = QWidget()
                    self.main_w.setLayout(self.main_grid)
                    self.table.setCellWidget(k, 0, el_p_lbl)
                    self.table.setCellWidget(k, 1, self.main_w)

                    k = k + 1
                    j = j + 1
                    bvc = bvc + 1

                btnSave = QPushButton()
                btnSave.setFixedSize(80, 25)
                btnSave.clicked.connect(self.on_btnSave_clicked)

                if self.interface_lng_val == 'Russian':
                    btnSave.setText("Сохранить")
                elif self.interface_lng_val == 'English':
                    btnSave.setText("Save")

                vbox = QVBoxLayout()
                vbox.addWidget(self.table)
                vbox.addWidget(btnSave)

                for bvc in range(len(self.type_list_main)):
                    self.type_chng(self.type_list_main, bvc)

                # ---------------------Размещение на форме всех компонентов-------------------------

                form = QFormLayout()
                form.addRow(vbox)
                self.setLayout(form)

    def type_chng(self, type_list_main, bvc):
        self.type_list_main[bvc].activated.connect(lambda: self.type_on_change(bvc))

    def type_on_change(self, bvc):
        type_txt = self.type_list_main[bvc].currentText()
        if type_txt == "tractionDisplacement":
            self.main_grid_list[bvc].addWidget(self.traction_lbl_list[bvc], 1, 0, alignment=QtCore.Qt.AlignLeft)
            self.main_grid_list[bvc].addWidget(self.traction_list[bvc], 1, 1, alignment=QtCore.Qt.AlignLeft)
            self.main_grid_list[bvc].addWidget(self.xyz_1_list_main[bvc][0], 1, 2, alignment=QtCore.Qt.AlignLeft)
            self.main_grid_list[bvc].addWidget(self.xyz_1_list_main[bvc][1], 1, 3, alignment=QtCore.Qt.AlignLeft)
            self.main_grid_list[bvc].addWidget(self.xyz_1_list_main[bvc][2], 1, 4, alignment=QtCore.Qt.AlignLeft)

            self.main_grid_list[bvc].addWidget(self.pressure_lbl_list[bvc], 2, 0, alignment=QtCore.Qt.AlignLeft)
            self.main_grid_list[bvc].addWidget(self.pressure_list[bvc], 2, 1, alignment=QtCore.Qt.AlignLeft)
            self.main_grid_list[bvc].addWidget(self.koord_list[bvc], 2, 2, alignment=QtCore.Qt.AlignLeft)

            self.main_grid_list[bvc].addWidget(self.value_lbl_list[bvc], 3, 0, alignment=QtCore.Qt.AlignLeft)
            self.main_grid_list[bvc].addWidget(self.value_list[bvc], 3, 1, alignment=QtCore.Qt.AlignLeft)
            self.main_grid_list[bvc].addWidget(self.xyz_2_list_main[bvc][0], 3, 2, alignment=QtCore.Qt.AlignLeft)
            self.main_grid_list[bvc].addWidget(self.xyz_2_list_main[bvc][1], 3, 3, alignment=QtCore.Qt.AlignLeft)
            self.main_grid_list[bvc].addWidget(self.xyz_2_list_main[bvc][2], 3, 4, alignment=QtCore.Qt.AlignLeft)
            self.table.setRowHeight(bvc + 3, 120)

        elif type_txt == "symmetryPlane" or type_txt == "empty" or type_txt == "noSlip" or type_txt == "zeroGradient":
            if self.main_grid_list[bvc].itemAtPosition(1, 0):
                self.main_grid_list[bvc].itemAtPosition(1, 0).widget().setParent(None)
            if self.main_grid_list[bvc].itemAtPosition(1, 1):
                self.main_grid_list[bvc].itemAtPosition(1, 1).widget().setParent(None)
            if self.main_grid_list[bvc].itemAtPosition(1, 2):
                self.main_grid_list[bvc].itemAtPosition(1, 2).widget().setParent(None)
            if self.main_grid_list[bvc].itemAtPosition(1, 3):
                self.main_grid_list[bvc].itemAtPosition(1, 3).widget().setParent(None)
            if self.main_grid_list[bvc].itemAtPosition(1, 4):
                self.main_grid_list[bvc].itemAtPosition(1, 4).widget().setParent(None)
            if self.main_grid_list[bvc].itemAtPosition(2, 0):
                self.main_grid_list[bvc].itemAtPosition(2, 0).widget().setParent(None)
            if self.main_grid_list[bvc].itemAtPosition(2, 1):
                self.main_grid_list[bvc].itemAtPosition(2, 1).widget().setParent(None)				
            if self.main_grid_list[bvc].itemAtPosition(2, 2):
                self.main_grid_list[bvc].itemAtPosition(2, 2).widget().setParent(None)
            if self.main_grid_list[bvc].itemAtPosition(3, 0):
                self.main_grid_list[bvc].itemAtPosition(3, 0).widget().setParent(None)
            if self.main_grid_list[bvc].itemAtPosition(3, 1):
                self.main_grid_list[bvc].itemAtPosition(3, 1).widget().setParent(None)
            if self.main_grid_list[bvc].itemAtPosition(3, 2):
                self.main_grid_list[bvc].itemAtPosition(3, 2).widget().setParent(None)
            if self.main_grid_list[bvc].itemAtPosition(3, 3):
                self.main_grid_list[bvc].itemAtPosition(3, 3).widget().setParent(None)
            if self.main_grid_list[bvc].itemAtPosition(3, 4):
                self.main_grid_list[bvc].itemAtPosition(3, 4).widget().setParent(None)

            self.table.setRowHeight(bvc + 3, 40)
				
        elif type_txt == "calculated":

            if self.main_grid_list[bvc].itemAtPosition(1, 0):
                self.main_grid_list[bvc].itemAtPosition(1, 0).widget().setParent(None)
            if self.main_grid_list[bvc].itemAtPosition(1, 1):
                self.main_grid_list[bvc].itemAtPosition(1, 1).widget().setParent(None)
            if self.main_grid_list[bvc].itemAtPosition(1, 2):
                self.main_grid_list[bvc].itemAtPosition(1, 2).widget().setParent(None)
            if self.main_grid_list[bvc].itemAtPosition(1, 3):
                self.main_grid_list[bvc].itemAtPosition(1, 3).widget().setParent(None)
            if self.main_grid_list[bvc].itemAtPosition(1, 4):
                self.main_grid_list[bvc].itemAtPosition(1, 4).widget().setParent(None)
            if self.main_grid_list[bvc].itemAtPosition(2, 0):
                self.main_grid_list[bvc].itemAtPosition(2, 0).widget().setParent(None)
            if self.main_grid_list[bvc].itemAtPosition(2, 1):
                self.main_grid_list[bvc].itemAtPosition(2, 1).widget().setParent(None)				
            if self.main_grid_list[bvc].itemAtPosition(2, 2):
                self.main_grid_list[bvc].itemAtPosition(2, 2).widget().setParent(None)
            if self.main_grid_list[bvc].itemAtPosition(3, 2):
                self.main_grid_list[bvc].itemAtPosition(3, 2).widget().setParent(None)
            if self.main_grid_list[bvc].itemAtPosition(3, 3):
                self.main_grid_list[bvc].itemAtPosition(3, 3).widget().setParent(None)
            if self.main_grid_list[bvc].itemAtPosition(3, 4):
                self.main_grid_list[bvc].itemAtPosition(3, 4).widget().setParent(None)
				
            if not self.main_grid_list[bvc].itemAtPosition(3, 0):
                self.main_grid_list[bvc].addWidget(self.value_lbl_list[bvc], 3, 0, alignment=QtCore.Qt.AlignLeft)
            if not self.main_grid_list[bvc].itemAtPosition(3, 1):
                self.main_grid_list[bvc].addWidget(self.value_list[bvc], 3, 1, alignment=QtCore.Qt.AlignLeft)
            if not self.main_grid_list[bvc].itemAtPosition(3, 2):
                self.main_grid_list[bvc].addWidget(self.main_koord_list[bvc], 3, 2, alignment=QtCore.Qt.AlignLeft)
            self.table.setRowHeight(bvc + 3, 70)

    def on_btnSave_clicked(self):
        dim_list = [self.d_1.text(), self.d_2.text(), self.d_3.text(), self.d_4.text(), self.d_5.text(), self.d_6.text(), self.d_7.text()]
        if not '' in dim_list and self.x.text() != '':
        # создаем таблицу self.par.file_name
            if self.par.file_name not in self.par.con.tables():
                query = QtSql.QSqlQuery()
                query.exec("CREATE TABLE " + self.par.file_name + "(param, value)")

                dimensions_perem = [self.d_1.text(), self.d_2.text(), self.d_3.text(), self.d_4.text(), self.d_5.text(),
                                self.d_6.text(), self.d_7.text()]
                dimensions_str = ' '.join(dimensions_perem)

                if self.table.cellWidget(1, 1).layout().itemAt(1).widget().text() != '' and \
                self.table.cellWidget(1, 1).layout().itemAt(2).widget().text() != '' and \
                self.table.cellWidget(1, 1).layout().itemAt(3).widget().text() != '':
                    internalField_perem = [self.internalField.currentText(), self.x.text(), self.y.text(), self.z.text()]
                    internalField_str = ', '.join(internalField_perem)
                    internalField_bl = '\n' + 'internalField   ' + self.internalField.currentText() + ' ' + '(' + self.x.text() + ' ' + self.y.text() + ' ' + self.z.text() + ')' + ';' + '\n'
                elif self.table.cellWidget(1, 1).layout().itemAt(1).widget().text() != '' and \
                self.table.cellWidget(1, 1).layout().itemAt(2).widget().text() == '' and \
                self.table.cellWidget(1, 1).layout().itemAt(3).widget().text() == '':
                    internalField_perem = [self.internalField.currentText(), self.x.text()]
                    internalField_str = ', '.join(internalField_perem)
                    internalField_bl = '\n' + 'internalField   ' + self.internalField.currentText() + ' ' + self.x.text() + ';' + '\n'

                query.exec("INSERT INTO " + self.par.file_name + "(param, value) VALUES ('%s','%s')" % ('dimensions', dimensions_str))
                query.exec("INSERT INTO " + self.par.file_name + "(param, value) VALUES ('%s','%s')" % ('internalField', internalField_str))

                # записываем файл self.par.file_name
                if os.path.exists(self.full_dir + '/0/' + self.par.file_name):
                    os.remove(self.full_dir + '/0/' + self.par.file_name)
		
                #shutil.copyfile("./matches/Shablon/0/0_file", self.full_dir + '/0/' + self.par.file_name)
                if not os.path.exists(self.par.full_dir + '/0/' + self.par.file_name):
                    shutil.copy("./matches/Shablon/0/0_file", self.par.full_dir + '/0')
                    os.rename(self.par.full_dir + '/0/0_file', self.par.full_dir + '/0/' + self.par.file_name)

				    #object      0_file;
                    file = open(self.par.full_dir + '/0/' + self.par.file_name)
                    data = file.read()
                    file.close()
                    result = re.findall(r'object      0_file', data)
    
                    #print(data)
                    if len(result) != 0:
                        new_data = re.sub(r'    object      0_file;', '    object      ' + self.par.object_edit_txt + ';', data)
                        #print(new_data)
                        file = open(self.par.full_dir + '/0/' + self.par.file_name, 'w')
                        file.write(new_data)
						
                        query.prepare("SELECT * FROM objects_pars WHERE file_name=?")
                        query.bindValue(0, self.par.file_name)
                        query.exec_()
                        query.first()
					
                        new_data = re.sub(r'    object      0_file;', '    object      ' + query.value(0) + ';', data)
                        file = open(self.par.full_dir + '/0/' + self.par.file_name, 'w')
                        file.write(new_data)
					
                        if self.par.file_name == 'U':
                            dop_U = re.sub(r'    class       volScalarField;', '    class      volVectorField;', data)
                            file.write(dop_U)
							
                        file.close()

                file_0 = open(self.full_dir + '/0/' + self.par.file_name, 'a')

                ###dimensions###
                dimensions_bl = '\n' + 'dimensions      ' + '[' + dimensions_str + ']' + ';' + '\n'
                ###internalField###
                #internalField_bl = '\n' + 'internalField   ' + self.internalField.currentText() + ' ' + '(' + self.x.text() + ' ' + self.y.text() + ' ' + self.z.text() + ')' + ';' + '\n'
                ###boundaryField###
                boundaryField_bl_start = '\n' + 'boundaryField' + '\n' + '{' + '\n'

                file_0.write(dimensions_bl + internalField_bl + boundaryField_bl_start)

                i = 0
                for el_p in self.patches_lst:
                    if self.type_list_main[i].currentText() == "symmetryPlane" or self.type_list_main[i].currentText() == "empty" or self.type_list_main[i].currentText() == "zeroGradient" or self.type_list_main[i].currentText() == "noSlip":
                        type_txt = self.main_grid_list[i].itemAtPosition(0, 1).widget().currentText()
                        query.exec("INSERT INTO " + self.par.file_name + "(param, value) VALUES ('%s','%s')" % (el_p, type_txt))

                        type_bl = '    ' + el_p + '\n' + '    ' + '{' + '\n' + '        ' + 'type' + '            ' + type_txt + ';' + '\n' + '    ' + '}' + '\n'
                        file_0.write(type_bl)

                    elif self.type_list_main[i].currentText() == "calculated":
                        type_txt = self.main_grid_list[i].itemAtPosition(0, 1).widget().currentText()

                        value_txt = self.main_grid_list[i].itemAtPosition(3, 1).widget().currentText()
                        main_koord_txt = self.main_grid_list[i].itemAtPosition(3, 2).widget().text()


                        complex_list = [type_txt, value_txt, main_koord_txt]

                        complex_str = ', '.join(complex_list)

                        query.exec("INSERT INTO " + self.par.file_name + "(param, value) VALUES ('%s','%s')" % (el_p, complex_str))

                        complex_bl = '    ' + el_p + '\n' + '    ' + '{' + '\n' + \
                                 '        ' + 'type' + '            ' + type_txt + ';' + '\n' + \
                                 '        ' + 'value' + '           ' + value_txt + ' ' + main_koord_txt + ';' + '\n' + \
                                 '    ' + '}' + '\n'
                        file_0.write(complex_bl)

                    elif self.type_list_main[i].currentText() == "tractionDisplacement":
                        type_txt = self.main_grid_list[i].itemAtPosition(0, 1).widget().currentText()

                        traction_txt = self.main_grid_list[i].itemAtPosition(1, 1).widget().currentText()
                        x_1_txt = self.main_grid_list[i].itemAtPosition(1, 2).widget().text()
                        y_1_txt = self.main_grid_list[i].itemAtPosition(1, 3).widget().text()
                        z_1_txt = self.main_grid_list[i].itemAtPosition(1, 4).widget().text()

                        pressure_txt = self.main_grid_list[i].itemAtPosition(2, 1).widget().currentText()
                        koord_txt = self.main_grid_list[i].itemAtPosition(2, 2).widget().text()

                        value_txt = self.main_grid_list[i].itemAtPosition(3, 1).widget().currentText()
                        x_2_txt = self.main_grid_list[i].itemAtPosition(3, 2).widget().text()
                        y_2_txt = self.main_grid_list[i].itemAtPosition(3, 3).widget().text()
                        z_2_txt = self.main_grid_list[i].itemAtPosition(3, 4).widget().text()

                        complex_list = [type_txt, traction_txt, x_1_txt, y_1_txt, z_1_txt, pressure_txt, koord_txt,
                                    value_txt, x_2_txt, y_2_txt, z_2_txt]

                        complex_str = ', '.join(complex_list)

                        query.exec("INSERT INTO " + self.par.file_name + "(param, value) VALUES ('%s','%s')" % (el_p, complex_str))

                        complex_bl = '    ' + el_p + '\n' + '    ' + '{' + '\n' + \
                                 '        ' + 'type' + '            ' + type_txt + ';' + '\n' + \
                                 '        ' + 'traction' + '        ' + traction_txt + ' ' + '(' + x_1_txt + ' ' + y_1_txt + ' ' + z_1_txt + ')' + ';' + '\n' + \
                                 '        ' + 'pressure' + '        ' + pressure_txt + ' ' + koord_txt + ';' + '\n' + \
                                 '        ' + 'value' + '           ' + value_txt + ' ' + '(' + x_2_txt + ' ' + y_2_txt + ' ' + z_2_txt + ')' + ';' + '\n' + \
                                 '    ' + '}' + '\n'
                        file_0.write(complex_bl)

                    i = i + 1

                boundaryField_bl_start = '}' + '\n\n'
                file_0.write(boundaryField_bl_start)

                close_str = '// ************************************************************************* //'
                file_0.write(close_str)

                file_0.close()
			
            elif self.par.file_name in self.par.con.tables():
                dimensions_perem = [self.d_1.text(), self.d_2.text(), self.d_3.text(), self.d_4.text(), self.d_5.text(),
                                self.d_6.text(), self.d_7.text()]
                dimensions_str = ' '.join(dimensions_perem)
                internalField_bl = ''

                query = QtSql.QSqlQuery()
                if self.table.cellWidget(1, 1).layout().itemAt(1).widget().text() != '' and \
                self.table.cellWidget(1, 1).layout().itemAt(2).widget().text() != '' and \
                self.table.cellWidget(1, 1).layout().itemAt(3).widget().text() != '':
                    internalField_perem = [self.internalField.currentText(), self.x.text(), self.y.text(), self.z.text()]
                    internalField_str = ', '.join(internalField_perem)
                    internalField_bl = '\n' + 'internalField   ' + self.internalField.currentText() + ' ' + '(' + self.x.text() + ' ' + self.y.text() + ' ' + self.z.text() + ')' + ';' + '\n'
					
                    query.prepare("UPDATE " + self.par.file_name + " SET value=? WHERE param='internalField'")
                    query.bindValue(0, internalField_str)
                    query.exec_()
					
                elif self.table.cellWidget(1, 1).layout().itemAt(1).widget().text() != '' and \
                self.table.cellWidget(1, 1).layout().itemAt(2).widget().text() == '' and \
                self.table.cellWidget(1, 1).layout().itemAt(3).widget().text() == '':
                    internalField_perem = [self.internalField.currentText(), self.x.text()]
                    internalField_str = ', '.join(internalField_perem)

                    internalField_bl = '\n' + 'internalField   ' + self.internalField.currentText() + ' ' + self.x.text() + ';' + '\n'

                    query.prepare("UPDATE " + self.par.file_name + " SET value=? WHERE param='internalField'")
                    query.bindValue(0, internalField_str)
                    query.exec_()

                query.prepare("UPDATE " + self.par.file_name + " SET value=? WHERE param='dimensions'")
                query.bindValue(0, dimensions_str)
                query.exec_()

                # записываем файл self.par.file_name
                if os.path.exists(self.full_dir + '/0/' + self.par.file_name):
                    os.remove(self.full_dir + '/0/' + self.par.file_name)

                shutil.copy("./matches/Shablon/0/0_file", self.par.full_dir + '/0')
                os.rename(self.par.full_dir + '/0/0_file', self.par.full_dir + '/0/' + self.par.file_name)
                
				#object      0_file;
                file = open(self.par.full_dir + '/0/' + self.par.file_name)
                data = file.read()
                file.close()
                result = re.findall(r'object      0_file', data)
    
                if len(result) != 0:
                    query.prepare("SELECT * FROM objects_pars WHERE file_name=?")
                    query.bindValue(0, self.par.file_name)
                    query.exec_()
                    query.first()
					
                    #print('вах')
                    #if query.isActive():
                        #query.first()
                        
                        #while query.isValid():
                            #value_res = query.value('object_name')
                            #value_list.append(value_res)
                            #query.next()
			
			
			
                    new_data = re.sub(r'    object      0_file;', '    object      ' + query.value(0) + ';', data)
                    #print(new_data)
                    file = open(self.par.full_dir + '/0/' + self.par.file_name, 'w')
                    file.write(new_data)
                    file.close()
					
                    if self.par.file_name == 'U':
                        file = open(self.par.full_dir + '/0/' + self.par.file_name)
                        data = file.read()
                        file.close()
                        file = open(self.par.full_dir + '/0/' + self.par.file_name, 'w')
                        dop_U = re.sub(r'    class       volScalarField;', '    class      volVectorField;', data)
                        #print(dop_U)
                        file.write(dop_U)
							
                        file.close()

                file_0 = open(self.full_dir + '/0/' + self.par.file_name, 'a')
                ###dimensions###
                dimensions_bl = '\n' + 'dimensions      ' + '[' + dimensions_str + ']' + ';' + '\n'
                ###internalField###
                #internalField_bl = '\n' + 'internalField   ' + self.internalField.currentText() + ' ' + '(' + self.x.text() + ' ' + self.y.text() + ' ' + self.z.text() + ')' + ';' + '\n'
                ###boundaryField###
                boundaryField_bl_start = '\n' + 'boundaryField' + '\n' + '{' + '\n'

                file_0.write(dimensions_bl + internalField_bl + boundaryField_bl_start)

                i = 0
                for el_p in self.patches_lst:
                    if self.type_list_main[i].currentText() == "symmetryPlane" or self.type_list_main[i].currentText() == "empty" or self.type_list_main[i].currentText() == "zeroGradient" or self.type_list_main[i].currentText() == "noSlip":
                        type_txt = self.main_grid_list[i].itemAtPosition(0, 1).widget().currentText()
                        #query.exec("REPLACE INTO " + self.par.file_name + "(param, value) VALUES ('%s','%s')" % (el_p, type_txt))
                        query.prepare("UPDATE " + self.par.file_name + " SET value=? WHERE param=?")
                        query.bindValue(1, el_p)
                        query.bindValue(0, type_txt)
                        query.exec_()

                        type_bl = '    ' + el_p + '\n' + '    ' + '{' + '\n' + '        ' + 'type' + '            ' + type_txt + ';' + '\n' + '    ' + '}' + '\n'
                        file_0.write(type_bl)
					
                    elif self.type_list_main[i].currentText() == "calculated":
                        type_txt = self.main_grid_list[i].itemAtPosition(0, 1).widget().currentText()

                        value_txt = self.main_grid_list[i].itemAtPosition(3, 1).widget().currentText()
                        main_koord_txt = self.main_grid_list[i].itemAtPosition(3, 2).widget().text()


                        complex_list = [type_txt, value_txt, main_koord_txt]

                        complex_str = ', '.join(complex_list)

                        query.prepare("UPDATE " + self.par.file_name + " SET value=? WHERE param=?")
                        query.bindValue(1, el_p)
                        query.bindValue(0, complex_str)
                        query.exec_()

                        complex_bl = '    ' + el_p + '\n' + '    ' + '{' + '\n' + \
                                 '        ' + 'type' + '            ' + type_txt + ';' + '\n' + \
                                 '        ' + 'value' + '           ' + value_txt + ' ' + main_koord_txt + ';' + '\n' + \
                                 '    ' + '}' + '\n'
                        file_0.write(complex_bl)

                    elif self.type_list_main[i].currentText() == "tractionDisplacement":
                        type_txt = self.main_grid_list[i].itemAtPosition(0, 1).widget().currentText()

                        traction_txt = self.main_grid_list[i].itemAtPosition(1, 1).widget().currentText()
                        x_1_txt = self.main_grid_list[i].itemAtPosition(1, 2).widget().text()
                        y_1_txt = self.main_grid_list[i].itemAtPosition(1, 3).widget().text()
                        z_1_txt = self.main_grid_list[i].itemAtPosition(1, 4).widget().text()

                        pressure_txt = self.main_grid_list[i].itemAtPosition(2, 1).widget().currentText()
                        koord_txt = self.main_grid_list[i].itemAtPosition(2, 2).widget().text()

                        value_txt = self.main_grid_list[i].itemAtPosition(3, 1).widget().currentText()
                        x_2_txt = self.main_grid_list[i].itemAtPosition(3, 2).widget().text()
                        y_2_txt = self.main_grid_list[i].itemAtPosition(3, 3).widget().text()
                        z_2_txt = self.main_grid_list[i].itemAtPosition(3, 4).widget().text()

                        complex_list = [type_txt, traction_txt, x_1_txt, y_1_txt, z_1_txt, pressure_txt, koord_txt,
                                    value_txt, x_2_txt, y_2_txt, z_2_txt]

                        complex_str = ', '.join(complex_list)

                        query.prepare("UPDATE " + self.par.file_name + " SET value=? WHERE param=?")
                        query.bindValue(1, el_p)
                        query.bindValue(0, complex_str)
                        query.exec_()

                        complex_bl = '    ' + el_p + '\n' + '    ' + '{' + '\n' + \
                                 '        ' + 'type' + '            ' + type_txt + ';' + '\n' + \
                                 '        ' + 'traction' + '        ' + traction_txt + ' ' + '(' + x_1_txt + ' ' + y_1_txt + ' ' + z_1_txt + ')' + ';' + '\n' + \
                                 '        ' + 'pressure' + '        ' + pressure_txt + ' ' + koord_txt + ';' + '\n' + \
                                 '        ' + 'value' + '           ' + value_txt + ' ' + '(' + x_2_txt + ' ' + y_2_txt + ' ' + z_2_txt + ')' + ';' + '\n' + \
                                 '    ' + '}' + '\n'
                        file_0.write(complex_bl)

                    i = i + 1

                boundaryField_bl_start = '}' + '\n\n'
                file_0.write(boundaryField_bl_start)

                close_str = '// ************************************************************************* //'
                file_0.write(close_str)

                file_0.close()
            
            self.par.cdw.setWidget(self.par.outf_scroll)
            outf = open(self.full_dir + '/0/' + self.par.file_name)

            if self.interface_lng_val == 'Russian':
                msg_lbl = QLabel(
                    '<span style="color:green">Файл ' + self.par.file_name + ' сохранен</span>')
            elif self.interface_lng_val == 'English':
                msg_lbl = QLabel(
                    '<span style="color:green">The ' + self.par.file_name + ' file saved</span>')
				
            self.par.listWidget.clear()
            self.par.item = QListWidgetItem()
            self.par.listWidget.addItem(self.par.item)
            self.par.listWidget.setItemWidget(self.par.item, msg_lbl)

            data = outf.read()

            if self.interface_lng_val == 'Russian':
                self.par.outf_lbl.setText("Файл " + "<font color='peru'>" + self.par.file_name + "</font>")
            elif self.interface_lng_val == 'English':
                self.par.outf_lbl.setText("<font color='peru'>" + self.par.file_name + "</font>" + " file")
            self.par.outf_edit.setText(data)

            self.par.cdw.setTitleBarWidget(self.par.cdw_frame)
            outf.close()

        else:
            msg_lbl_list = []
            if '' in dim_list:
                if self.interface_lng_val == 'Russian':
                    msg_lbl = QLabel(
                        '<span style="color:red">Укажите все параметры поля dimensions</span>')
                elif self.interface_lng_val == 'English':
                    msg_lbl = QLabel(
                        '<span style="color:red">Specify all parameters of the dimensions field</span>')
                msg_lbl_list.append(msg_lbl)	
            if self.x.text() == '':
                if self.interface_lng_val == 'Russian':
                    msg_lbl = QLabel(
                        '<span style="color:red">Укажите параметр x поля internalField</span>')
                elif self.interface_lng_val == 'English':
                    msg_lbl = QLabel(
                        '<span style="color:red">Specify the x parameter of the internalField field</span>')
                msg_lbl_list.append(msg_lbl)
				
            self.par.listWidget.clear()
            for msg_lbl in msg_lbl_list:
                
                self.par.item = QListWidgetItem()
                self.par.listWidget.addItem(self.par.item)
                self.par.listWidget.setItemWidget(self.par.item, msg_lbl)
			

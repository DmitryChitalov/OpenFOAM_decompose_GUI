# -*- coding: utf-8 -*-
# -----------------------------Импорт модулей-----------------------------------

from PyQt5 import QtSql
import os
import os.path
import shutil

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QFormLayout, QTableWidget, QComboBox, \
    QSpinBox, QPushButton, QListWidgetItem, QDoubleSpinBox, QLineEdit, QHBoxLayout

# -----------------------------------Форма--------------------------------------

class decomposeParDict_form_class(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.interface_lng_val = parent.interface_lng_val
        self.con = parent.con
        self.full_dir = parent.full_dir
        self.par = parent

        if self.con.open():

            self.table = QTableWidget(11, 2)
            self.table.setColumnWidth(0, 170)
            self.table.setColumnWidth(1, 230)
            self.table.setFixedSize(674, 480)
            if self.interface_lng_val == 'Russian':
                self.table.setHorizontalHeaderLabels(["Параметр", "Значение"])
            elif self.interface_lng_val == 'English':
                self.table.setHorizontalHeaderLabels(["Parameter", "Value"])
			
            # numberOfSubdomains
            numberOfSubdomains_lbl = QLabel('numberOfSubdomains:')
            self.numberOfSubdomains = QSpinBox()
            self.numberOfSubdomains.setFixedSize(150, 27)
            self.numberOfSubdomains.setRange(0, 10000)
            self.table.setCellWidget(0, 1, self.numberOfSubdomains)
            self.table.setCellWidget(0, 0, numberOfSubdomains_lbl)

            # method
            method_lbl = QLabel('method:')
            self.method = QComboBox()
            self.method.setFixedSize(150, 27)
            method_list = ["scotch", "simple", "hierarchical"]
            self.method.addItems(method_list)
            self.table.setCellWidget(1, 1, self.method)
            self.table.setCellWidget(1, 0, method_lbl)
			
			# simpleCoeffs
            simpleCoeffs_lbl = QLabel('simpleCoeffs')
            self.table.setCellWidget(2, 0, simpleCoeffs_lbl)
			
			# simpleCoeffs.n
            simpleCoeffs_n_lbl = QLabel('n:')
            self.x_1 = QLineEdit()
            self.x_1.setFixedSize(40, 25)
            self.y_1 = QLineEdit()
            self.y_1.setFixedSize(40, 25)
            self.z_1 = QLineEdit()
            self.z_1.setFixedSize(40, 25)
            self.dimensions_hbox = QHBoxLayout()
            self.dimensions_hbox.addWidget(self.x_1)
            self.dimensions_hbox.addWidget(self.y_1)
            self.dimensions_hbox.addWidget(self.z_1)
            self.dimensions_w = QWidget()
            self.dimensions_w.setLayout(self.dimensions_hbox)
            self.table.setCellWidget(3, 1, self.dimensions_w)
            self.table.setCellWidget(3, 0, simpleCoeffs_n_lbl)
            self.table.setRowHeight(3, 40)
			
			# simpleCoeffs.delta
            simpleCoeffs_delta_lbl = QLabel('delta:')
            self.simpleCoeffs_delta = QLineEdit()
            self.simpleCoeffs_delta.setFixedSize(150, 27)
            self.table.setCellWidget(4, 1, self.simpleCoeffs_delta)
            self.table.setCellWidget(4, 0, simpleCoeffs_delta_lbl)
			
		    # hierarchicalCoeffs
            hierarchicalCoeffs_lbl = QLabel('hierarchicalCoeffs')
            self.table.setCellWidget(5, 0, hierarchicalCoeffs_lbl)
			
		    # hierarchicalCoeffs.n
            hierarchicalCoeffs_n_lbl = QLabel('n:')
            self.x_2 = QLineEdit()
            self.x_2.setFixedSize(40, 25)
            self.y_2 = QLineEdit()
            self.y_2.setFixedSize(40, 25)
            self.z_2 = QLineEdit()
            self.z_2.setFixedSize(40, 25)
            self.dimensions_hbox = QHBoxLayout()
            self.dimensions_hbox.addWidget(self.x_2)
            self.dimensions_hbox.addWidget(self.y_2)
            self.dimensions_hbox.addWidget(self.z_2)
            self.dimensions_w = QWidget()
            self.dimensions_w.setLayout(self.dimensions_hbox)
            self.table.setCellWidget(6, 1, self.dimensions_w)
            self.table.setCellWidget(6, 0, hierarchicalCoeffs_n_lbl)
            self.table.setRowHeight(6, 40)
			
			# hierarchicalCoeffs.delta
            hierarchicalCoeffs_delta_lbl = QLabel('delta:')
            self.hierarchicalCoeffs_delta = QLineEdit()
            self.hierarchicalCoeffs_delta.setFixedSize(150, 27)
            self.table.setCellWidget(7, 1, self.hierarchicalCoeffs_delta)
            self.table.setCellWidget(7, 0, hierarchicalCoeffs_delta_lbl)
			
			# manualCoeffs
            manualCoeffs_lbl = QLabel('manualCoeffs')
            self.table.setCellWidget(8, 0, manualCoeffs_lbl)
			
			# manualCoeffs.dataFile
            manualCoeffs_dataFile_lbl = QLabel('dataFile:')
            self.manualCoeffs_dataFile = QLineEdit()
            self.manualCoeffs_dataFile.setFixedSize(150, 27)
            self.table.setCellWidget(9, 1, self.manualCoeffs_dataFile)
            self.table.setCellWidget(9, 0, manualCoeffs_dataFile_lbl)
			
			# distributed
            distributed_lbl = QLabel('distributed:')
            self.distributed = QComboBox()
            self.distributed.setFixedSize(150, 27)
            distributed_list = ["yes", "no"]
            self.distributed.addItems(distributed_list)
            self.table.setCellWidget(10, 1, self.distributed)
            self.table.setCellWidget(10, 0, distributed_lbl)
			
            # вывод значений параметров
            if 'decomposeParDict' in self.con.tables():						
                query = QtSql.QSqlQuery()
                query.exec("SELECT * FROM decomposeParDict")
                if query.isActive():
                    query.first()
                    value_list = []
                    while query.isValid():
                        value_res = query.value('value')
                        value_list.append(value_res)
                        query.next()
					
					# numberOfSubdomains
                    self.numberOfSubdomains.setValue(value_list[0])
					
                    # method
                    method_mas = self.method.count()   
                    for i in range(method_mas):
                        if self.method.itemText(i) == value_list[1]:
                            self.method.setCurrentIndex(i)
							
					# simpleCoeffs
                    self.x_1.setText(value_list[2].split(' ')[0])
                    self.y_1.setText(value_list[2].split(' ')[1])
                    self.z_1.setText(value_list[2].split(' ')[2])
                    self.simpleCoeffs_delta.setText(value_list[3])
					
					# hierarchicalCoeffs
                    self.x_2.setText(value_list[4].split(' ')[0])
                    self.y_2.setText(value_list[4].split(' ')[1])
                    self.z_2.setText(value_list[4].split(' ')[2])
                    self.hierarchicalCoeffs_delta.setText(value_list[5])
					
					# manualCoeffs
                    self.manualCoeffs_dataFile.setText(value_list[6])
					
					# distributed
                    distributed_mas = self.distributed.count()   
                    for i in range(distributed_mas):
                        if self.distributed.itemText(i) == value_list[7]:
                            self.distributed.setCurrentIndex(i)

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

# ---------------------Размещение на форме всех компонентов-------------------------

            form = QFormLayout()
            form.addRow(vbox)
            self.setLayout(form)

    def on_btnSave_clicked(self):
        numberOfSubdomains_txt = self.numberOfSubdomains.value()
        method_txt = self.method.currentText()
		
        x_1_txt = self.x_1.text()
        y_1_txt = self.y_1.text()
        z_1_txt = self.z_1.text()
        simpleCoeffs_delta_txt = self.simpleCoeffs_delta.text()
		
        x_2_txt = self.x_1.text()
        y_2_txt = self.y_1.text()
        z_2_txt = self.z_1.text()
        hierarchicalCoeffs_delta_txt = self.hierarchicalCoeffs_delta.text()
		
        corr_list = [x_1_txt, y_1_txt, z_1_txt, simpleCoeffs_delta_txt, x_2_txt, y_2_txt, z_2_txt, hierarchicalCoeffs_delta_txt]
		
        manualCoeffs_dataFile_txt = self.manualCoeffs_dataFile.text()
        distributed_txt = self.distributed.currentText()
		
        xyz_1_perem = [x_1_txt, y_1_txt, z_1_txt]
        xyz_1_str = ' '.join(xyz_1_perem)
		
        xyz_2_perem = [x_2_txt, y_2_txt, z_2_txt]
        xyz_2_str = ' '.join(xyz_2_perem)

        if 'decomposeParDict' not in self.con.tables():
            query = QtSql.QSqlQuery()
            query.exec("CREATE TABLE decomposeParDict(param, value)")

            query.exec("INSERT INTO decomposeParDict(param, value) VALUES ('%s','%s')" % ('numberOfSubdomains', ''))
            query.exec("INSERT INTO decomposeParDict(param, value) VALUES ('%s','%s')" % ('method', ''))
			
            query.exec("INSERT INTO decomposeParDict(param, value) VALUES ('%s','%s')" % ('simpleCoeffs_xyz', ''))
            query.exec("INSERT INTO decomposeParDict(param, value) VALUES ('%s','%s')" % ('simpleCoeffs_delta', ''))
			
            query.exec("INSERT INTO decomposeParDict(param, value) VALUES ('%s','%s')" % ('hierarchicalCoeffs_xyz', ''))
            query.exec("INSERT INTO decomposeParDict(param, value) VALUES ('%s','%s')" % ('hierarchicalCoeffs_delta', ''))
			
            query.exec("INSERT INTO decomposeParDict(param, value) VALUES ('%s','%s')" % ('manualCoeffs_dataFile', ''))
            query.exec("INSERT INTO decomposeParDict(param, value) VALUES ('%s','%s')" % ('distributed', ''))

        if 'decomposeParDict' in self.con.tables():
            query = QtSql.QSqlQuery()

            query.prepare("UPDATE decomposeParDict SET value=? WHERE param='numberOfSubdomains'")
            query.bindValue(0, numberOfSubdomains_txt)
            query.exec_()
			
            query.prepare("UPDATE decomposeParDict SET value=? WHERE param='method'")
            query.bindValue(0, method_txt)
            query.exec_()
			
            query.prepare("UPDATE decomposeParDict SET value=? WHERE param='simpleCoeffs_xyz'")
            query.bindValue(0, xyz_1_str)
            query.exec_()
			
            query.prepare("UPDATE decomposeParDict SET value=? WHERE param='simpleCoeffs_delta'")
            query.bindValue(0, simpleCoeffs_delta_txt)
            query.exec_()
			
            query.prepare("UPDATE decomposeParDict SET value=? WHERE param='hierarchicalCoeffs_xyz'")
            query.bindValue(0, xyz_2_str)
            query.exec_()
			
            query.prepare("UPDATE decomposeParDict SET value=? WHERE param='hierarchicalCoeffs_delta'")
            query.bindValue(0, hierarchicalCoeffs_delta_txt)
            query.exec_()
			
            query.prepare("UPDATE decomposeParDict SET value=? WHERE param='manualCoeffs_dataFile'")
            query.bindValue(0, manualCoeffs_dataFile_txt)
            query.exec_()
			
            query.prepare("UPDATE decomposeParDict SET value=? WHERE param='distributed'")
            query.bindValue(0, distributed_txt)
            query.exec_()
			
        if '' not in corr_list:
			
			# записываем файл decomposeParDict
            if os.path.exists(self.full_dir + '/system/decomposeParDict'):
                os.remove(self.full_dir + '/system/decomposeParDict')

            shutil.copyfile("./matches/Shablon/system/decomposeParDict", self.full_dir + '/system/decomposeParDict')

            dPD = open(self.full_dir + '/system/decomposeParDict', 'a')
			###numberOfSubdomains###
            nOS_bl = '\n' + 'numberOfSubdomains ' + str(numberOfSubdomains_txt) + ';' + '\n'

			###method###
            m_bl = '\n' + 'method          ' + method_txt + ';' + '\n'

			###simpleCoeffs###
            sC_bl = '\n' + 'simpleCoeffs' + '\n' + '{' + '\n' + '    ' + 'n' + '               ' + '(' + x_1_txt + ' ' + y_1_txt + ' ' + z_1_txt + ')' + ';' + '\n' + \
            '    ' + 'delta' + '           ' + simpleCoeffs_delta_txt + ';' + '\n' + '}' + '\n' 

			###hierarchicalCoeffs###
            hC_bl = '\n' + 'hierarchicalCoeffs' + '\n' + '{' + '\n' + '    ' + 'n' + '               ' + '(' + x_2_txt + ' ' + y_2_txt + ' ' + z_2_txt + ')' + ';' + '\n' + \
            '    ' + 'delta' + '           ' + hierarchicalCoeffs_delta_txt + ';' + '\n' + '    ' + 'order' + '           ' + 'xyz' + ';' + '\n' + \
            '}' + '\n' 

			###manualCoeffs###
            mC_bl = '\n' + 'manualCoeffs' + '\n' + '{' + '\n' + '    ' + 'dataFile' + '        ' + '"' + manualCoeffs_dataFile_txt + '"' + ';' + '\n' + '}' + '\n' 

			###distributed###
            d_bl = '\n' + 'distributed' + '     ' + distributed_txt + ';' + '\n\n' 

            dPD.write(nOS_bl + m_bl + sC_bl + hC_bl + mC_bl + d_bl)
            close_str = '// ************************************************************************* //'
            dPD.write(close_str)

            dPD.close()

            self.par.cdw.setWidget(self.par.outf_scroll)
            outf = open(self.full_dir + '/system/decomposeParDict')

            if self.interface_lng_val == 'Russian':
                msg_lbl = QLabel(
                    '<span style="color:green">Файл decomposeParDict сохранен</span>')
            elif self.interface_lng_val == 'English':
                msg_lbl = QLabel(
                    '<span style="color:green">The decomposeParDict file saved</span>')
				
            data = outf.read()

            if self.interface_lng_val == 'Russian':
                self.par.outf_lbl.setText("Файл " + "<font color='peru'>" + 'decomposeParDict' + "</font>")
            elif self.interface_lng_val == 'English':
                self.par.outf_lbl.setText("<font color='peru'>" + 'decomposeParDict' + "</font>" + " file")
            self.par.outf_edit.setText(data)
			
            self.par.outf_edit.setText(data)

            self.par.cdw.setTitleBarWidget(self.par.cdw_frame)
            outf.close()
			
        else:
            if self.interface_lng_val == 'Russian':
                msg_lbl = QLabel(
                    '<span style="color:red">Проверьте заполнение всех параметров</span>')
            elif self.interface_lng_val == 'English':
                msg_lbl = QLabel(
                    '<span style="color:red">Check the completion of all parameters</span>')


        self.par.listWidget.clear()
        self.par.item = QListWidgetItem()
        self.par.listWidget.addItem(self.par.item)
        self.par.listWidget.setItemWidget(self.par.item, msg_lbl)

        
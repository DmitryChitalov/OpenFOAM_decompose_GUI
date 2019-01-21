# -*- coding: utf-8 -*-
# -----------------------------Импорт модулей-----------------------------------

from PyQt5 import QtSql
import os
import os.path
import shutil
from PyQt5 import QtCore

from PyQt5 import QtGui

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QFormLayout, QTableWidget, QComboBox, \
    QSpinBox, QPushButton, QListWidgetItem, QCheckBox, QHBoxLayout, QDoubleSpinBox

# -----------------------------------Форма--------------------------------------

class thermophysicalProperties_form_class(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.interface_lng_val = parent.interface_lng_val
        self.con = parent.con
        self.full_dir = parent.full_dir
        self.par = parent

        if self.con.open():
			
            self.table = QTableWidget(3, 2)
            self.table.setColumnWidth(0, 150)
            self.table.setColumnWidth(1, 230)
            self.table.setFixedSize(674, 480)
            if self.interface_lng_val == 'Russian':
                self.table.setHorizontalHeaderLabels(["Параметр", "Значение"])
            elif self.interface_lng_val == 'English':
                self.table.setHorizontalHeaderLabels(["Parameter", "Value"])
			
			# checks
            checks_lbl = QLabel('Фазы')
            self.water_chkb = QCheckBox(":water")
            self.air_chkb = QCheckBox(":air")
            self.checks_hbox = QHBoxLayout()
            self.checks_hbox.addWidget(self.water_chkb)
            self.checks_hbox.addWidget(self.air_chkb)

            self.checks_w = QWidget()
            self.checks_w.setLayout(self.checks_hbox)
            self.table.setCellWidget(0, 1, self.checks_w)
            self.table.setCellWidget(0, 0, checks_lbl)
            self.table.setRowHeight(0, 40)
			
			# pMin
            pMin_lbl = QLabel('pMin')
            self.pMin = QSpinBox()
            self.pMin.setRange(0, 100000)
            self.pMin.setFixedSize(80, 25)
            self.table.setCellWidget(1, 0, pMin_lbl)
            self.table.setCellWidget(1, 1, self.pMin)
					
			# sigma
            sigma_lbl = QLabel('sigma')
            self.sigma = QDoubleSpinBox()
            self.sigma.setRange(0, 100000)
            self.sigma.setFixedSize(80, 25)
            self.table.setCellWidget(2, 0, sigma_lbl)
            self.table.setCellWidget(2, 1, self.sigma)
            
            # вывод значений параметров
            if 'thermophysicalProperties' in self.con.tables():						
                query = QtSql.QSqlQuery()
                query.exec("SELECT * FROM thermophysicalProperties")
                if query.isActive():
                    query.first()
                    value_list = []
                    while query.isValid():
                        value_res = query.value('value')
                        value_list.append(value_res)
                        query.next()
						
                    if value_list[0].split(' ')[0]:
                        self.water_chkb.setChecked(True)
					
                    if value_list[0].split(' ')[1]:
                        self.air_chkb.setChecked(True)
					
                    # pMin
                    self.pMin.setValue(int(value_list[1]))
					
					# sigma 
                    self.sigma.setValue(float(value_list[2]))
            					
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

        spec_list = []
        if self.water_chkb.isChecked() == True:
            spec_list.append('water')
			
            if os.path.exists(self.full_dir + '/constant/thermophysicalProperties.water'):
                os.remove(self.full_dir + '/constant/thermophysicalProperties.water')
		
            shutil.copyfile("./matches/Shablon/constant/thermophysicalProperties.water", self.full_dir + '/constant/thermophysicalProperties.water')
		
        if self.air_chkb.isChecked() == True:
            spec_list.append('air')
            if os.path.exists(self.full_dir + '/constant/thermophysicalProperties.air'):
                os.remove(self.full_dir + '/constant/thermophysicalProperties.air')
		
            shutil.copyfile("./matches/Shablon/constant/thermophysicalProperties.air", self.full_dir + '/constant/thermophysicalProperties.air')
		
        phases_str = 'phases ' + '(' + ' '.join(spec_list) + ')'
        pMin_str = str(self.pMin.value())
        sigma_str = str(self.sigma.value())
		
        if 'thermophysicalProperties' not in self.con.tables():
            query = QtSql.QSqlQuery()
            query.exec("CREATE TABLE thermophysicalProperties(param, value)")
			
            query.exec("INSERT INTO thermophysicalProperties(param, value) VALUES ('%s','%s')" % ('phases', phases_str))
            query.exec("INSERT INTO thermophysicalProperties(param, value) VALUES ('%s','%s')" % ('pMin', pMin_str))
            query.exec("INSERT INTO thermophysicalProperties(param, value) VALUES ('%s','%s')" % ('sigma', sigma_str))
			
        if 'thermophysicalProperties' in self.con.tables():
            query = QtSql.QSqlQuery()

            query.prepare("UPDATE thermophysicalProperties SET value=? WHERE param='phases'")
            query.bindValue(0, phases_str)
            query.exec_()
			
            query.prepare("UPDATE thermophysicalProperties SET value=? WHERE param='pMin'")
            query.bindValue(0, pMin_str)
            query.exec_()
			
            query.prepare("UPDATE thermophysicalProperties SET value=? WHERE param='sigma'")
            query.bindValue(0, sigma_str)
            query.exec_()
			
        # записываем файл thermophysicalProperties
        if os.path.exists(self.full_dir + '/constant/thermophysicalProperties'):
            os.remove(self.full_dir + '/constant/thermophysicalProperties')
		
        shutil.copyfile("./matches/Shablon/constant/thermophysicalProperties", self.full_dir + '/constant/thermophysicalProperties')
		
        thermophysicalProperties = open(self.full_dir + '/constant/thermophysicalProperties', 'a')
		
		###phases###
        phases_bl = '\n' + phases_str + ';' + '\n\n'
		###pMin###
        pMin_bl = 'pMin' + '        ' + pMin_str + ';' + '\n\n'
		###sigma###
        sigma_bl = 'sigma' + '       ' + sigma_str + ';' + '\n\n'

        thermophysicalProperties.write(phases_bl + pMin_bl + sigma_bl)
		
        close_str = '// ************************************************************************* //'
        thermophysicalProperties.write(close_str)

        thermophysicalProperties.close()
		
        self.par.cdw.setWidget(self.par.outf_scroll)
        outf = open(self.full_dir + '/constant/thermophysicalProperties')

        if self.interface_lng_val == 'Russian':
            msg_lbl = QLabel(
                '<span style="color:green">Файл thermophysicalProperties сохранен</span>')
        elif self.interface_lng_val == 'English':
            msg_lbl = QLabel(
                '<span style="color:green">The thermophysicalProperties file saved</span>')

        self.par.listWidget.clear()
        self.par.item = QListWidgetItem()
        self.par.listWidget.addItem(self.par.item)
        self.par.listWidget.setItemWidget(self.par.item, msg_lbl)

        data = outf.read()

        if self.interface_lng_val == 'Russian':
            self.par.outf_lbl.setText("Файл " + "<font color='peru'>" + 'thermophysicalProperties' + "</font>")
        elif self.interface_lng_val == 'English':
            self.par.outf_lbl.setText("<font color='peru'>" + 'thermophysicalProperties' + "</font>" + " file")
        self.par.outf_edit.setText(data)

        self.par.cdw.setTitleBarWidget(self.par.cdw_frame)
        outf.close()
		
        el_system_air = 'thermophysicalProperties.air'
        item_system = self.par.treeview.model.item(1, 0)
        child_item_system = QtGui.QStandardItem(el_system_air)
        child_item_system.setForeground(QtGui.QColor('navy'))
        item_system.setChild(3, 0, child_item_system)
		
        el_system_water = 'thermophysicalProperties.water'
        item_system = self.par.treeview.model.item(1, 0)
        child_item_system = QtGui.QStandardItem(el_system_water)
        child_item_system.setForeground(QtGui.QColor('navy'))
        item_system.setChild(4, 0, child_item_system)
		
		
		
		
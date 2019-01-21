# -*- coding: utf-8 -*-
# -----------------------------Импорт модулей-----------------------------------

from PyQt5 import QtSql
import os
import os.path
import shutil

from PyQt5 import QtCore

from PyQt5 import QtGui

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QFormLayout, QTableWidget, QComboBox, \
    QSpinBox, QPushButton, QListWidgetItem, QLineEdit

# -----------------------------------Форма--------------------------------------

class thermophysicalProperties_air_form_class(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.interface_lng_val = parent.interface_lng_val
        self.con = parent.con
        self.full_dir = parent.full_dir
        self.par = parent

        if self.con.open():

            self.table = QTableWidget(14, 2)
            self.table.setColumnWidth(0, 150)
            self.table.setColumnWidth(1, 230)
            self.table.setFixedSize(674, 480)
           
            if self.interface_lng_val == 'Russian':
                self.table.setHorizontalHeaderLabels(["Параметр", "Значение"])
            elif self.interface_lng_val == 'English':
                self.table.setHorizontalHeaderLabels(["Parameter", "Value"])
			
			# thermoType
            thermoType_lbl = QLabel('thermoType')
            self.table.setCellWidget(0, 0, thermoType_lbl)
			
			# type
            type_lbl = QLabel('type')
            self.type = QComboBox()
            self.type.setFixedSize(160, 25)
            type_list = ["heRhoThermo"]
            self.type.addItems(type_list)
            self.table.setCellWidget(1, 0, type_lbl)
            self.table.setCellWidget(1, 1, self.type)
			
			# mixture
            mixture_lbl = QLabel('mixture')
            self.mixture = QComboBox()
            self.mixture.setFixedSize(160, 25)
            mixture_list = ["pureMixture"]
            self.mixture.addItems(mixture_list)
            self.table.setCellWidget(2, 0, mixture_lbl)
            self.table.setCellWidget(2, 1, self.mixture)
			
			# transport
            transport_lbl = QLabel('transport')
            self.transport = QComboBox()
            self.transport.setFixedSize(160, 25)
            transport_list = ["const"]
            self.transport.addItems(transport_list)
            self.table.setCellWidget(3, 0, transport_lbl)
            self.table.setCellWidget(3, 1, self.transport)
			
			# thermo
            thermo_lbl = QLabel('thermo')
            self.thermo = QComboBox()
            self.thermo.setFixedSize(160, 25)
            thermo_list = ["hConst"]
            self.thermo.addItems(thermo_list)
            self.table.setCellWidget(4, 0, thermo_lbl)
            self.table.setCellWidget(4, 1, self.thermo)
			
			# equationOfState
            equationOfState_lbl = QLabel('thermo')
            self.equationOfState = QComboBox()
            self.equationOfState.setFixedSize(160, 25)
            equationOfState_list = ["perfectGas"]
            self.equationOfState.addItems(equationOfState_list)
            self.table.setCellWidget(5, 0, equationOfState_lbl)
            self.table.setCellWidget(5, 1, self.equationOfState)
			
			# specie
            specie_lbl = QLabel('specie')
            self.specie = QComboBox()
            self.specie.setFixedSize(160, 25)
            specie_list = ["specie"]
            self.specie.addItems(specie_list)
            self.table.setCellWidget(6, 0, specie_lbl)
            self.table.setCellWidget(6, 1, self.specie)
			
			# energy
            energy_lbl = QLabel('energy')
            self.energy = QComboBox()
            self.energy.setFixedSize(160, 25)
            energy_list = ["sensibleInternalEnergy"]
            self.energy.addItems(energy_list)
            self.table.setCellWidget(7, 0, energy_lbl)
            self.table.setCellWidget(7, 1, self.energy)
			
            # mixture
            mixture_lbl = QLabel('mixture')
            self.table.setCellWidget(8, 0, mixture_lbl)
			
			# specie.molWeight
            specie_molWeight_lbl = QLabel('specie.molWeight')
            self.specie_molWeight = QLineEdit()
            self.specie_molWeight.setFixedSize(160, 25)
            self.table.setCellWidget(9, 0, specie_molWeight_lbl)
            self.table.setCellWidget(9, 1, self.specie_molWeight)
			
            # thermodynamics.Cp
            thermodynamics_Cp_lbl = QLabel('thermodynamics.Cp')
            self.thermodynamics_Cp = QLineEdit()
            self.thermodynamics_Cp.setFixedSize(160, 25)
            self.table.setCellWidget(10, 0, thermodynamics_Cp_lbl)
            self.table.setCellWidget(10, 1, self.thermodynamics_Cp)
			
			# thermodynamics.Hf
            thermodynamics_Hf_lbl = QLabel('thermodynamics.Hf')
            self.thermodynamics_Hf = QLineEdit()
            self.thermodynamics_Hf.setFixedSize(160, 25)
            self.table.setCellWidget(11, 0, thermodynamics_Hf_lbl)
            self.table.setCellWidget(11, 1, self.thermodynamics_Hf)
			
			# transport.mu
            transport_mu_lbl = QLabel('transport.mu')
            self.transport_mu = QLineEdit()
            self.transport_mu.setFixedSize(160, 25)
            self.table.setCellWidget(12, 0, transport_mu_lbl)
            self.table.setCellWidget(12, 1, self.transport_mu)
			
			# transport.Pr
            transport_Pr_lbl = QLabel('transport.Pr')
            self.transport_Pr = QLineEdit()
            self.transport_Pr.setFixedSize(160, 25)
            self.table.setCellWidget(13, 0, transport_Pr_lbl)
            self.table.setCellWidget(13, 1, self.transport_Pr)

            # вывод значений параметров
            if 'thermophysicalProperties_air' in self.con.tables():						
                query = QtSql.QSqlQuery()
                query.exec("SELECT * FROM thermophysicalProperties_air")
                if query.isActive():
                    query.first()
                    value_list = []
                    while query.isValid():
                        value_res = query.value('value')
                        value_list.append(value_res)
                        query.next()
					
                    # type
                    type_mas = self.type.count()   
                    for i in range(type_mas):
                        if self.type.itemText(i) == value_list[0]:
                            self.type.setCurrentIndex(i)
							
					# mixture
                    mixture_mas = self.mixture.count()   
                    for i in range(mixture_mas):
                        if self.mixture.itemText(i) == value_list[1]:
                            self.mixture.setCurrentIndex(i)
							
					# transport
                    transport_mas = self.transport.count()   
                    for i in range(transport_mas):
                        if self.transport.itemText(i) == value_list[2]:
                            self.transport.setCurrentIndex(i)
							
					# thermo
                    thermo_mas = self.thermo.count()   
                    for i in range(thermo_mas):
                        if self.thermo.itemText(i) == value_list[3]:
                            self.thermo.setCurrentIndex(i)
							
					# equationOfState
                    equationOfState_mas = self.equationOfState.count()   
                    for i in range(equationOfState_mas):
                        if self.equationOfState.itemText(i) == value_list[4]:
                            self.equationOfState.setCurrentIndex(i)
							
					# specie
                    specie_mas = self.specie.count()   
                    for i in range(specie_mas):
                        if self.specie.itemText(i) == value_list[5]:
                            self.specie.setCurrentIndex(i)
							
					# energy
                    energy_mas = self.energy.count()   
                    for i in range(energy_mas):
                        if self.energy.itemText(i) == value_list[6]:
                            self.energy.setCurrentIndex(i)
							
					# specie.molWeight
                    self.specie_molWeight.setText(value_list[7])
					
					# sthermodynamics.Cp
                    self.thermodynamics_Cp.setText(value_list[8])
					
					# thermodynamics.Hf
                    self.thermodynamics_Hf.setText(value_list[9])
					
					# transport.mu
                    self.transport_mu.setText(value_list[10])
					
					# transport.Pr
                    self.transport_Pr.setText(value_list[11])
							
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
        type_txt = self.type.currentText()
        mixture_txt = self.mixture.currentText()
        transport_txt = self.transport.currentText()
        thermo_txt = self.thermo.currentText()
        equationOfState_txt = self.equationOfState.currentText()
        specie_txt = self.specie.currentText()
        energy_txt = self.energy.currentText()
		
        specie_molWeight_txt = self.specie_molWeight.text()
        thermodynamics_Cp_txt = self.thermodynamics_Cp.text()
        thermodynamics_Hf_txt = self.thermodynamics_Hf.text()
        transport_mu_txt = self.transport_mu.text()
        transport_Pr_txt = self.transport_Pr.text()
        
        mixture_list = [self.specie_molWeight.text(), self.thermodynamics_Cp.text(), self.thermodynamics_Hf.text(), self.transport_mu.text(), self.transport_Pr.text()]
		
        if '' not in mixture_list:
            
            if 'thermophysicalProperties_air' not in self.con.tables():
                query = QtSql.QSqlQuery()
                query.exec("CREATE TABLE thermophysicalProperties_air(param, value)")

                query.exec("INSERT INTO thermophysicalProperties_air(param, value) VALUES ('%s','%s')" % ('type', ''))
                query.exec("INSERT INTO thermophysicalProperties_air(param, value) VALUES ('%s','%s')" % ('mixture', ''))
                query.exec("INSERT INTO thermophysicalProperties_air(param, value) VALUES ('%s','%s')" % ('transport', ''))
                query.exec("INSERT INTO thermophysicalProperties_air(param, value) VALUES ('%s','%s')" % ('thermo', ''))
                query.exec("INSERT INTO thermophysicalProperties_air(param, value) VALUES ('%s','%s')" % ('equationOfState', ''))
                query.exec("INSERT INTO thermophysicalProperties_air(param, value) VALUES ('%s','%s')" % ('specie', ''))
                query.exec("INSERT INTO thermophysicalProperties_air(param, value) VALUES ('%s','%s')" % ('energy', ''))
				
                query.exec("INSERT INTO thermophysicalProperties_air(param, value) VALUES ('%s','%s')" % ('specie.molWeight', ''))
                query.exec("INSERT INTO thermophysicalProperties_air(param, value) VALUES ('%s','%s')" % ('thermodynamics.Cp', ''))
                query.exec("INSERT INTO thermophysicalProperties_air(param, value) VALUES ('%s','%s')" % ('thermodynamics.Hf', ''))
                query.exec("INSERT INTO thermophysicalProperties_air(param, value) VALUES ('%s','%s')" % ('transport.mu', ''))
                query.exec("INSERT INTO thermophysicalProperties_air(param, value) VALUES ('%s','%s')" % ('transport.Pr', ''))

            if 'thermophysicalProperties_air' in self.con.tables():
                query = QtSql.QSqlQuery()

                query.prepare("UPDATE thermophysicalProperties_air SET value=? WHERE param='type'")
                query.bindValue(0, type_txt)
                query.exec_()
				
                query.prepare("UPDATE thermophysicalProperties_air SET value=? WHERE param='mixture'")
                query.bindValue(0, mixture_txt)
                query.exec_()
				
                query.prepare("UPDATE thermophysicalProperties_air SET value=? WHERE param='transport'")
                query.bindValue(0, transport_txt)
                query.exec_()
				
                query.prepare("UPDATE thermophysicalProperties_air SET value=? WHERE param='thermo'")
                query.bindValue(0, thermo_txt)
                query.exec_()
				
                query.prepare("UPDATE thermophysicalProperties_air SET value=? WHERE param='equationOfState'")
                query.bindValue(0, equationOfState_txt)
                query.exec_()
				
                query.prepare("UPDATE thermophysicalProperties_air SET value=? WHERE param='specie'")
                query.bindValue(0, specie_txt)
                query.exec_()
				
                query.prepare("UPDATE thermophysicalProperties_air SET value=? WHERE param='energy'")
                query.bindValue(0, energy_txt)
                query.exec_()
				
                query.prepare("UPDATE thermophysicalProperties_air SET value=? WHERE param='specie.molWeight'")
                query.bindValue(0, specie_molWeight_txt)
                query.exec_()
				
                query.prepare("UPDATE thermophysicalProperties_air SET value=? WHERE param='thermodynamics.Cp'")
                query.bindValue(0, thermodynamics_Cp_txt)
                query.exec_()
				
                query.prepare("UPDATE thermophysicalProperties_air SET value=? WHERE param='thermodynamics.Hf'")
                query.bindValue(0, thermodynamics_Hf_txt)
                query.exec_()
				
                query.prepare("UPDATE thermophysicalProperties_air SET value=? WHERE param='transport.mu'")
                query.bindValue(0, transport_mu_txt)
                query.exec_()
				
                query.prepare("UPDATE thermophysicalProperties_air SET value=? WHERE param='transport.Pr'")
                query.bindValue(0, transport_Pr_txt)
                query.exec_()

            # записываем файл thermophysicalProperties
            if os.path.exists(self.full_dir + '/constant/thermophysicalProperties.air'):
                os.remove(self.full_dir + '/constant/thermophysicalProperties.air')
		
            shutil.copyfile("./matches/Shablon/constant/thermophysicalProperties.air", self.full_dir + '/constant/thermophysicalProperties.air')
		
            tP = open(self.full_dir + '/constant/thermophysicalProperties.air', 'a')
			
			###thermoType_start###
            tT_bl_start = '\n' + 'thermoType' + '\n' + '{' + '\n'
        
		    ###type###
            t_bl = '    ' + 'type            ' + type_txt + ';' + '\n'
			
			###mixture###
            m_bl = '    ' + 'mixture         ' + mixture_txt + ';' + '\n'
			
			###transport###
            tr_bl = '    ' + 'transport       ' + transport_txt + ';' + '\n'
			
			###thermo###
            th_bl = '    ' + 'thermo          ' + thermo_txt + ';' + '\n'
			
			###equationOfState###
            eOS_bl = '    ' + 'equationOfState ' + equationOfState_txt + ';' + '\n'
			
			###specie###
            s_bl = '    ' + 'specie          ' + specie_txt + ';' + '\n'
			
			###energy###
            e_bl = '    ' + 'energy          ' + energy_txt + ';' + '\n'
			
			###thermoType_end###
            tT_bl_end = '}' + '\n\n'
			
			###mixture_start###
            m_bl_start = 'mixture' + '\n' + '{' + '\n'
			
			###specie###
            sp_bl = '    ' + 'specie' + '\n' + '    ' + '{' + '\n' + '        ' + 'molWeight' + '   ' + specie_molWeight_txt + ';' + '\n' + '    ' + '}' + '\n'
			
			###thermodynamics###
            td_bl = '    ' + 'thermodynamics' + '\n' + '    ' + '{' + '\n' + '        ' + 'Cp' + '   ' + thermodynamics_Cp_txt + ';' + '\n' + '        ' + 'Hf' + '   ' + thermodynamics_Hf_txt + ';' + '\n'+ '    ' + '}' + '\n'
		
		    ###transport###
            tra_bl = '    ' + 'transport' + '\n' + '    ' + '{' + '\n' + '        ' + 'mu' + '   ' + transport_mu_txt + ';' + '\n' + '        ' + 'Pr' + '   ' + transport_Pr_txt + ';' + '\n'+ '    ' + '}'
		
            ###mixture_end###
            m_bl_end = '\n' + '}' + '\n\n'
		
            tP.write(tT_bl_start + t_bl + m_bl + tr_bl + th_bl + eOS_bl + s_bl + e_bl + tT_bl_end + m_bl_start + sp_bl + td_bl + tra_bl + m_bl_end)
            close_str = '// ************************************************************************* //'
            tP.write(close_str)

            tP.close()

            self.par.cdw.setWidget(self.par.outf_scroll)
            outf = open(self.full_dir + '/constant/thermophysicalProperties.air')

            if self.interface_lng_val == 'Russian':
                msg_lbl = QLabel(
                    '<span style="color:green">Файл thermophysicalProperties.air сохранен</span>')
            elif self.interface_lng_val == 'English':
                msg_lbl = QLabel(
                    '<span style="color:green">The thermophysicalProperties.air file saved</span>')

            data = outf.read()

            if self.interface_lng_val == 'Russian':
                self.par.outf_lbl.setText("Файл " + "<font color='peru'>" + 'thermophysicalProperties.air' + "</font>")
            elif self.interface_lng_val == 'English':
                self.par.outf_lbl.setText("<font color='peru'>" + 'thermophysicalProperties.air' + "</font>" + " file")
            self.par.outf_edit.setText(data)

            self.par.cdw.setTitleBarWidget(self.par.cdw_frame)
            outf.close()

        else:
			
            if self.interface_lng_val == 'Russian':
                msg_lbl = QLabel(
                    '<span style="color:red">Проверьте корректность заполнения всех параметров</span>')
            elif self.interface_lng_val == 'English':
                msg_lbl = QLabel(
                    '<span style="color:red">Check the correctness of filling all the parameters</span>')
		
        self.par.listWidget.clear()
        self.par.item = QListWidgetItem()
        self.par.listWidget.addItem(self.par.item)
        self.par.listWidget.setItemWidget(self.par.item, msg_lbl)


# -*- coding: utf-8 -*-
# -----------------------------Импорт модулей-----------------------------------

from PyQt5 import QtSql
import os
import os.path
import shutil

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QFormLayout, QTableWidget, QComboBox, \
    QSpinBox, QPushButton, QListWidgetItem

# -----------------------------------Форма--------------------------------------

class fvSchemes_form_class(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.interface_lng_val = parent.interface_lng_val
        self.con = parent.con
        self.full_dir = parent.full_dir
        self.par = parent

        if self.con.open():

            self.table = QTableWidget(13, 2)
            self.table.setColumnWidth(0, 320)
            self.table.setColumnWidth(1, 230)
            self.table.setFixedSize(674, 480)
            if self.interface_lng_val == 'Russian':
                self.table.setHorizontalHeaderLabels(["Параметр", "Значение"])
            elif self.interface_lng_val == 'English':
                self.table.setHorizontalHeaderLabels(["Parameter", "Value"])

            # ddtSchemes.default
            ddtSchemes_default_lbl = QLabel('ddtSchemes.default')
            self.ddtSchemes_default = QComboBox()
            ddtSchemes_default_list = ["Euler", "demo"]
            self.ddtSchemes_default.addItems(ddtSchemes_default_list)
            self.table.setCellWidget(0, 1, self.ddtSchemes_default)
            self.table.setCellWidget(0, 0, ddtSchemes_default_lbl)

            # gradSchemes.default
            gradSchemes_default_lbl = QLabel('gradSchemes.default')
            self.gradSchemes_default = QComboBox()
            gradSchemes_default_list = ["Gauss linear", "leastSquares", "demo"]
            self.gradSchemes_default.addItems(gradSchemes_default_list)
            self.table.setCellWidget(1, 1, self.gradSchemes_default)
            self.table.setCellWidget(1, 0, gradSchemes_default_lbl)

            # divSchemes.div(phi,alpha)
            divSchemes_div_1_lbl = QLabel('divSchemes.div(phi,alpha)')
            self.divSchemes_div_1 = QComboBox()
            divSchemes_div_1_list = ["Gauss vanLeer", "demo"]
            self.divSchemes_div_1.addItems(divSchemes_div_1_list)
            self.table.setCellWidget(2, 1, self.divSchemes_div_1)
            self.table.setCellWidget(2, 0, divSchemes_div_1_lbl)
			
			# divSchemes.div(phirb,alpha)
            divSchemes_div_2_lbl = QLabel('divSchemes.div(phirb,alpha)')
            self.divSchemes_div_2 = QComboBox()
            divSchemes_div_2_list = ["Gauss linear", "demo"]
            self.divSchemes_div_2.addItems(divSchemes_div_2_list)
            self.table.setCellWidget(3, 1, self.divSchemes_div_2)
            self.table.setCellWidget(3, 0, divSchemes_div_2_lbl)
			
			# divSchemes.div(rhoPhi,U)
            divSchemes_div_3_lbl = QLabel('divSchemes.div(rhoPhi,U)')
            self.divSchemes_div_3 = QComboBox()
            divSchemes_div_3_list = ["Gauss upwind", "demo"]
            self.divSchemes_div_3.addItems(divSchemes_div_3_list)
            self.table.setCellWidget(4, 1, self.divSchemes_div_3)
            self.table.setCellWidget(4, 0, divSchemes_div_3_lbl)
			
			# divSchemes.div(rhoPhi,T)
            divSchemes_div_4_lbl = QLabel('divSchemes.div(rhoPhi,T)')
            self.divSchemes_div_4 = QComboBox()
            divSchemes_div_4_list = ["Gauss upwind", "demo"]
            self.divSchemes_div_4.addItems(divSchemes_div_4_list)
            self.table.setCellWidget(5, 1, self.divSchemes_div_4)
            self.table.setCellWidget(5, 0, divSchemes_div_4_lbl)
			
			# divSchemes.div(rhoPhi,K)
            divSchemes_div_5_lbl = QLabel('divSchemes.div(rhoPhi,K)')
            self.divSchemes_div_5 = QComboBox()
            divSchemes_div_5_list = ["Gauss upwind", "demo"]
            self.divSchemes_div_5.addItems(divSchemes_div_5_list)
            self.table.setCellWidget(6, 1, self.divSchemes_div_5)
            self.table.setCellWidget(6, 0, divSchemes_div_5_lbl)
			
			# divSchemes.div(phi,p)
            divSchemes_div_6_lbl = QLabel('divSchemes.div(phi,p)')
            self.divSchemes_div_6 = QComboBox()
            divSchemes_div_6_list = ["Gauss upwind", "demo"]
            self.divSchemes_div_6.addItems(divSchemes_div_6_list)
            self.table.setCellWidget(7, 1, self.divSchemes_div_6)
            self.table.setCellWidget(7, 0, divSchemes_div_6_lbl)
			
			# divSchemes.div(phi,k)
            divSchemes_div_7_lbl = QLabel('divSchemes.div(phi,k)')
            self.divSchemes_div_7 = QComboBox()
            divSchemes_div_7_list = ["Gauss upwind", "demo"]
            self.divSchemes_div_7.addItems(divSchemes_div_7_list)
            self.table.setCellWidget(8, 1, self.divSchemes_div_7)
            self.table.setCellWidget(8, 0, divSchemes_div_7_lbl)
			
			# divSchemes.div(((rho*nuEff)*dev2(T(grad(U)))))
            divSchemes_div_8_lbl = QLabel('divSchemes.div(((rho*nuEff)*dev2(T(grad(U)))))')
            self.divSchemes_div_8 = QComboBox()
            divSchemes_div_8_list = ["Gauss linear", "demo"]
            self.divSchemes_div_8.addItems(divSchemes_div_8_list)
            self.table.setCellWidget(9, 1, self.divSchemes_div_8)
            self.table.setCellWidget(9, 0, divSchemes_div_8_lbl)
			
			# laplacianSchemes.default
            laplacianSchemes_default_lbl = QLabel('laplacianSchemes.default')
            self.laplacianSchemes_default = QComboBox()
            laplacianSchemes_default_list = ["Gauss linear uncorrected", "demo"]
            self.laplacianSchemes_default.addItems(laplacianSchemes_default_list)
            self.table.setCellWidget(10, 1, self.laplacianSchemes_default)
            self.table.setCellWidget(10, 0, laplacianSchemes_default_lbl)
			
			# interpolationSchemes.default
            interpolationSchemes_default_lbl = QLabel('interpolationSchemes.default')
            self.interpolationSchemes_default = QComboBox()
            interpolationSchemes_default_list = ["linear", "demo"]
            self.interpolationSchemes_default.addItems(interpolationSchemes_default_list)
            self.table.setCellWidget(11, 1, self.interpolationSchemes_default)
            self.table.setCellWidget(11, 0, interpolationSchemes_default_lbl)
			
			# snGradSchemes.default
            snGradSchemes_default_lbl = QLabel('snGradSchemes.default')
            self.snGradSchemes_default = QComboBox()
            snGradSchemes_default_list = ["uncorrected", "demo"]
            self.snGradSchemes_default.addItems(snGradSchemes_default_list)
            self.table.setCellWidget(12, 1, self.snGradSchemes_default)
            self.table.setCellWidget(12, 0, snGradSchemes_default_lbl)
			
            # вывод значений параметров
            if 'fvSchemes' in self.con.tables():
						
                query = QtSql.QSqlQuery()
                query.exec("SELECT * FROM fvSchemes")
                if query.isActive():
                    query.first()
                    value_list = []
                    while query.isValid():
                        value_res = query.value('value')
                        value_list.append(value_res)
                        query.next()
					
                    # ddtSchemes.default
                    ddtSchemes_default_mas = self.ddtSchemes_default.count()   
                    for i in range(ddtSchemes_default_mas):
                        if self.ddtSchemes_default.itemText(i) == value_list[0]:
                            self.ddtSchemes_default.setCurrentIndex(i)
							
					# gradSchemes.default
                    gradSchemes_default_mas = self.gradSchemes_default.count()   
                    for i in range(gradSchemes_default_mas):
                        if self.gradSchemes_default.itemText(i) == value_list[1]:
                            self.gradSchemes_default.setCurrentIndex(i)
					
					# divSchemes.div(phi,alpha)
                    divSchemes_div_1_mas = self.divSchemes_div_1.count()   
                    for i in range(divSchemes_div_1_mas):
                        if self.divSchemes_div_1.itemText(i) == value_list[2]:
                            self.divSchemes_div_1.setCurrentIndex(i)
					
					# divSchemes.div(phirb,alpha)
                    divSchemes_div_2_mas = self.divSchemes_div_2.count()   
                    for i in range(divSchemes_div_2_mas):
                        if self.divSchemes_div_2.itemText(i) == value_list[3]:
                            self.divSchemes_div_2.setCurrentIndex(i)
					
					# divSchemes.div(rhoPhi,U)
                    divSchemes_div_3_mas = self.divSchemes_div_3.count()   
                    for i in range(divSchemes_div_3_mas):
                        if self.divSchemes_div_3.itemText(i) == value_list[4]:
                            self.divSchemes_div_3.setCurrentIndex(i)
					
					# divSchemes.div(rhoPhi,T)
                    divSchemes_div_4_mas = self.divSchemes_div_4.count()   
                    for i in range(divSchemes_div_4_mas):
                        if self.divSchemes_div_4.itemText(i) == value_list[5]:
                            self.divSchemes_div_4.setCurrentIndex(i)
					
					# divSchemes.div(rhoPhi,K)
                    divSchemes_div_5_mas = self.divSchemes_div_5.count()   
                    for i in range(divSchemes_div_5_mas):
                        if self.divSchemes_div_5.itemText(i) == value_list[6]:
                            self.divSchemes_div_5.setCurrentIndex(i)
					
					# divSchemes.div(phi,p)
                    divSchemes_div_6_mas = self.divSchemes_div_6.count()   
                    for i in range(divSchemes_div_6_mas):
                        if self.divSchemes_div_6.itemText(i) == value_list[7]:
                            self.divSchemes_div_6.setCurrentIndex(i)
					
					# divSchemes.div(phi,k)
                    divSchemes_div_7_mas = self.divSchemes_div_7.count()   
                    for i in range(divSchemes_div_7_mas):
                        if self.divSchemes_div_7.itemText(i) == value_list[8]:
                            self.divSchemes_div_7.setCurrentIndex(i)
					
					# divSchemes.div(((rho*nuEff)*dev2(T(grad(U)))))
                    divSchemes_div_8_mas = self.divSchemes_div_8.count()   
                    for i in range(divSchemes_div_8_mas):
                        if self.divSchemes_div_8.itemText(i) == value_list[9]:
                            self.divSchemes_div_8.setCurrentIndex(i)
					
					# laplacianSchemes.default
                    laplacianSchemes_default_mas = self.laplacianSchemes_default.count()   
                    for i in range(laplacianSchemes_default_mas):
                        if self.laplacianSchemes_default.itemText(i) == value_list[10]:
                            self.laplacianSchemes_default.setCurrentIndex(i)
					
					# interpolationSchemes.default
                    interpolationSchemes_default_mas = self.interpolationSchemes_default.count()   
                    for i in range(interpolationSchemes_default_mas):
                        if self.interpolationSchemes_default.itemText(i) == value_list[11]:
                            self.interpolationSchemes_default.setCurrentIndex(i)
					
					# snGradSchemes.default
                    snGradSchemes_default_mas = self.snGradSchemes_default.count()   
                    for i in range(snGradSchemes_default_mas):
                        if self.snGradSchemes_default.itemText(i) == value_list[12]:
                            self.snGradSchemes_default.setCurrentIndex(i)
							
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
        ddtSchemes_default_txt = self.ddtSchemes_default.currentText()
        gradSchemes_default_txt = self.gradSchemes_default.currentText()
        divSchemes_div_1_txt = self.divSchemes_div_1.currentText()
        divSchemes_div_2_txt = self.divSchemes_div_2.currentText()
        divSchemes_div_3_txt = self.divSchemes_div_3.currentText()
        divSchemes_div_4_txt = self.divSchemes_div_4.currentText()
        divSchemes_div_5_txt = self.divSchemes_div_5.currentText()
        divSchemes_div_6_txt = self.divSchemes_div_6.currentText()
        divSchemes_div_7_txt = self.divSchemes_div_7.currentText()
        divSchemes_div_8_txt = self.divSchemes_div_8.currentText()
        laplacianSchemes_default_txt = self.laplacianSchemes_default.currentText()
        interpolationSchemes_default_txt = self.interpolationSchemes_default.currentText()
        snGradSchemes_default_txt = self.snGradSchemes_default.currentText()
		
        if 'fvSchemes' not in self.con.tables():
            query = QtSql.QSqlQuery()
            query.exec("CREATE TABLE fvSchemes(param, value)")

            query.exec("INSERT INTO fvSchemes(param, value) VALUES ('%s','%s')" % ('ddtSchemes_default', ''))
            query.exec("INSERT INTO fvSchemes(param, value) VALUES ('%s','%s')" % ('gradSchemes_default', ''))
            query.exec("INSERT INTO fvSchemes(param, value) VALUES ('%s','%s')" % ('divSchemes_div_1', ''))
            query.exec("INSERT INTO fvSchemes(param, value) VALUES ('%s','%s')" % ('divSchemes_div_2', ''))
            query.exec("INSERT INTO fvSchemes(param, value) VALUES ('%s','%s')" % ('divSchemes_div_3', ''))
            query.exec("INSERT INTO fvSchemes(param, value) VALUES ('%s','%s')" % ('divSchemes_div_4', ''))
            query.exec("INSERT INTO fvSchemes(param, value) VALUES ('%s','%s')" % ('divSchemes_div_5', ''))
            query.exec("INSERT INTO fvSchemes(param, value) VALUES ('%s','%s')" % ('divSchemes_div_6', ''))
            query.exec("INSERT INTO fvSchemes(param, value) VALUES ('%s','%s')" % ('divSchemes_div_7', ''))
            query.exec("INSERT INTO fvSchemes(param, value) VALUES ('%s','%s')" % ('divSchemes_div_8', ''))
            query.exec("INSERT INTO fvSchemes(param, value) VALUES ('%s','%s')" % ('laplacianSchemes_default', ''))
            query.exec("INSERT INTO fvSchemes(param, value) VALUES ('%s','%s')" % ('interpolationSchemes_default', ''))
            query.exec("INSERT INTO fvSchemes(param, value) VALUES ('%s','%s')" % ('snGradSchemes_default', ''))
            
			
        if 'fvSchemes' in self.con.tables():
            query = QtSql.QSqlQuery()

            query.prepare("UPDATE fvSchemes SET value=? WHERE param='ddtSchemes_default'")
            query.bindValue(0, ddtSchemes_default_txt)
            query.exec_()
			
            query.prepare("UPDATE fvSchemes SET value=? WHERE param='gradSchemes_default'")
            query.bindValue(0, gradSchemes_default_txt)
            query.exec_()
			
            query.prepare("UPDATE fvSchemes SET value=? WHERE param='divSchemes_div_1'")
            query.bindValue(0, divSchemes_div_1_txt)
            query.exec_()
			
            query.prepare("UPDATE fvSchemes SET value=? WHERE param='divSchemes_div_2'")
            query.bindValue(0, divSchemes_div_2_txt)
            query.exec_()
			
            query.prepare("UPDATE fvSchemes SET value=? WHERE param='divSchemes_div_3'")
            query.bindValue(0, divSchemes_div_3_txt)
            query.exec_()
			
            query.prepare("UPDATE fvSchemes SET value=? WHERE param='divSchemes_div_4'")
            query.bindValue(0, divSchemes_div_4_txt)
            query.exec_()
			
            query.prepare("UPDATE fvSchemes SET value=? WHERE param='divSchemes_div_5'")
            query.bindValue(0, divSchemes_div_5_txt)
            query.exec_()
			
            query.prepare("UPDATE fvSchemes SET value=? WHERE param='divSchemes_div_6'")
            query.bindValue(0, divSchemes_div_6_txt)
            query.exec_()
			
            query.prepare("UPDATE fvSchemes SET value=? WHERE param='divSchemes_div_7'")
            query.bindValue(0, divSchemes_div_7_txt)
            query.exec_()
			
            query.prepare("UPDATE fvSchemes SET value=? WHERE param='divSchemes_div_8'")
            query.bindValue(0, divSchemes_div_8_txt)
            query.exec_()
			
            query.prepare("UPDATE fvSchemes SET value=? WHERE param='laplacianSchemes_default'")
            query.bindValue(0, laplacianSchemes_default_txt)
            query.exec_()
			
            query.prepare("UPDATE fvSchemes SET value=? WHERE param='interpolationSchemes_default'")
            query.bindValue(0, interpolationSchemes_default_txt)
            query.exec_()
			
            query.prepare("UPDATE fvSchemes SET value=? WHERE param='snGradSchemes_default_txt'")
            query.bindValue(0, snGradSchemes_default_txt)
            query.exec_()

        # записываем файл fvSchemes
        if os.path.exists(self.full_dir + '/system/fvSchemes'):
            os.remove(self.full_dir + '/system/fvSchemes')
		
        shutil.copyfile("./matches/Shablon/system/fvSchemes", self.full_dir + '/system/fvSchemes')

        fvS = open(self.full_dir + '/system/fvSchemes', 'a')
        ###ddtSchemes###
        ddtSchemes_bl = '\n' + 'ddtSchemes' + '\n' + '{' + '\n' + '    ' + 'default'  + '         ' + ddtSchemes_default_txt + ';' + '\n' + '}' + '\n'
		
		###gradSchemes###
        gradSchemes_bl = '\n' + 'gradSchemes' + '\n' + '{' + '\n' + '    ' + 'default'  + '         ' + gradSchemes_default_txt + ';' + '\n' + '}' + '\n'
		
        ###divSchemes###
        divSchemes_bl = '\n' + 'divSchemes' + '\n' + '{' + '\n' + \
        '    ' + 'div(phi,alpha)' + '  ' + divSchemes_div_1_txt + ';' + '\n' + \
        '    ' + 'div(phirb,alpha)' + ' ' + divSchemes_div_2_txt + ';' + '\n\n' + \
        '    ' + 'div(rhoPhi,U)' + '  ' + divSchemes_div_3_txt + ';' + '\n' + \
        '    ' + 'div(rhoPhi,T)' + '  ' + divSchemes_div_4_txt + ';' + '\n' + \
        '    ' + 'div(rhoPhi,K)' + '  ' + divSchemes_div_5_txt + ';' + '\n' + \
        '    ' + 'div(phi,p)' + '      ' + divSchemes_div_6_txt + ';' + '\n' + \
        '    ' + 'div(phi,k)' + '      ' + divSchemes_div_7_txt + ';' + '\n\n' + \
        '    ' + 'div(((rho*nuEff)*dev2(T(grad(U)))))' + ' ' + divSchemes_div_8_txt + ';' + '\n' + \
        '}' + '\n'
		
		###laplacianSchemes###
        laplacianSchemes_bl = '\n' + 'laplacianSchemes' + '\n' + '{' + '\n' + '    ' + 'default'  + '         ' + laplacianSchemes_default_txt + ';' + '\n' + '}' + '\n'
		
		###interpolationSchemes###
        interpolationSchemes_bl = '\n' + 'interpolationSchemes' + '\n' + '{' + '\n' + '    ' + 'default'  + '         ' + interpolationSchemes_default_txt + ';' + '\n' + '}' + '\n'
		
		###snGradSchemes###
        snGradSchemes_bl = '\n' + 'snGradSchemes' + '\n' + '{' + '\n' + '    ' + 'default'  + '         ' + snGradSchemes_default_txt + ';' + '\n' + '}' + '\n\n'

        fvS.write(ddtSchemes_bl + gradSchemes_bl + divSchemes_bl + laplacianSchemes_bl + interpolationSchemes_bl + snGradSchemes_bl)
        close_str = '// ************************************************************************* //'
        fvS.write(close_str)

        fvS.close()

        self.par.cdw.setWidget(self.par.outf_scroll)
        outf = open(self.full_dir + '/system/fvSchemes')

        if self.interface_lng_val == 'Russian':
            msg_lbl = QLabel(
                '<span style="color:green">Файл fvSchemes сохранен</span>')
        elif self.interface_lng_val == 'English':
            msg_lbl = QLabel(
                '<span style="color:green">The fvSchemes file saved</span>')

        self.par.listWidget.clear()
        self.par.item = QListWidgetItem()
        self.par.listWidget.addItem(self.par.item)
        self.par.listWidget.setItemWidget(self.par.item, msg_lbl)

        data = outf.read()

        if self.interface_lng_val == 'Russian':
            self.par.outf_lbl.setText("Файл " + "<font color='peru'>" + 'fvSchemes' + "</font>")
        elif self.interface_lng_val == 'English':
            self.par.outf_lbl.setText("<font color='peru'>" + 'fvSchemes' + "</font>" + " file")
        self.par.outf_edit.setText(data)

        self.par.cdw.setTitleBarWidget(self.par.cdw_frame)
        outf.close()


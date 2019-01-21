# -*- coding: utf-8 -*-
# -----------------------------Импорт модулей-----------------------------------

from PyQt5 import QtSql
import os
import os.path
import shutil

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QFormLayout, QTableWidget, QComboBox, \
    QSpinBox, QPushButton, QListWidgetItem

# -----------------------------------Форма--------------------------------------

class turbulenceProperties_form_class(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.interface_lng_val = parent.interface_lng_val
        self.con = parent.con
        self.full_dir = parent.full_dir
        self.par = parent

        if self.con.open():

            self.table = QTableWidget(1, 2)
            self.table.setColumnWidth(0, 150)
            self.table.setColumnWidth(1, 230)
            self.table.setFixedSize(674, 480)
            if self.interface_lng_val == 'Russian':
                self.table.setHorizontalHeaderLabels(["Параметр", "Значение"])
            elif self.interface_lng_val == 'English':
                self.table.setHorizontalHeaderLabels(["Parameter", "Value"])
            # simulationType
            simulationType_lbl = QLabel('simulationType')
            self.simulationType = QComboBox()
            simulationType_list = ["laminar", "RAS"]
            self.simulationType.addItems(simulationType_list)
            self.table.setCellWidget(0, 1, self.simulationType)
            self.table.setCellWidget(0, 0, simulationType_lbl)

            # вывод значений параметров
            if 'turbulenceProperties' in self.con.tables():						
                query = QtSql.QSqlQuery()
                query.exec("SELECT * FROM turbulenceProperties")
                if query.isActive():
                    query.first()
                    value_list = []
                    while query.isValid():
                        value_res = query.value('value')
                        value_list.append(value_res)
                        query.next()
					
                    # simulationType
                    simulationType_mas = self.simulationType.count()   
                    for i in range(simulationType_mas):
                        if self.simulationType.itemText(i) == value_list[0]:
                            self.simulationType.setCurrentIndex(i)
							
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
        simulationType_txt = self.simulationType.currentText()
        
        if 'turbulenceProperties' not in self.con.tables():
            query = QtSql.QSqlQuery()
            query.exec("CREATE TABLE turbulenceProperties(param, value)")

            query.exec("INSERT INTO turbulenceProperties(param, value) VALUES ('%s','%s')" % ('simulationType', ''))

        if 'turbulenceProperties' in self.con.tables():
            query = QtSql.QSqlQuery()

            query.prepare("UPDATE turbulenceProperties SET value=? WHERE param='simulationType'")
            query.bindValue(0, simulationType_txt)
            query.exec_()

        # записываем файл turbulenceProperties
        if os.path.exists(self.full_dir + '/constant/turbulenceProperties'):
            os.remove(self.full_dir + '/constant/turbulenceProperties')
		
        shutil.copyfile("./matches/Shablon/constant/turbulenceProperties", self.full_dir + '/constant/turbulenceProperties')
		
        tP = open(self.full_dir + '/constant/turbulenceProperties', 'a')
		
        ###simulationType###
        sT_bl = '\n' + 'simulationType     ' + simulationType_txt + ';' + '\n\n'

        tP.write(sT_bl)
        close_str = '// ************************************************************************* //'
        tP.write(close_str)

        tP.close()

        self.par.cdw.setWidget(self.par.outf_scroll)
        outf = open(self.full_dir + '/constant/turbulenceProperties')

        if self.interface_lng_val == 'Russian':
            msg_lbl = QLabel(
                '<span style="color:green">Файл turbulenceProperties сохранен</span>')
        elif self.interface_lng_val == 'English':
            msg_lbl = QLabel(
                '<span style="color:green">The turbulenceProperties file saved</span>')

        self.par.listWidget.clear()
        self.par.item = QListWidgetItem()
        self.par.listWidget.addItem(self.par.item)
        self.par.listWidget.setItemWidget(self.par.item, msg_lbl)

        data = outf.read()

        if self.interface_lng_val == 'Russian':
            self.par.outf_lbl.setText("Файл " + "<font color='peru'>" + 'turbulenceProperties' + "</font>")
        elif self.interface_lng_val == 'English':
            self.par.outf_lbl.setText("<font color='peru'>" + 'turbulenceProperties' + "</font>" + " file")
        self.par.outf_edit.setText(data)

        self.par.cdw.setTitleBarWidget(self.par.cdw_frame)
        outf.close()


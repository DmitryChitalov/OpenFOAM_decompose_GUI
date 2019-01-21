# -*- coding: utf-8 -*-
# -----------------------------Импорт модулей-----------------------------------

from PyQt5 import QtSql
import os
import os.path
import shutil

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QFormLayout, QTableWidget, QComboBox, \
    QSpinBox, QPushButton, QListWidgetItem, QLineEdit, QHBoxLayout

# -----------------------------------Форма--------------------------------------

class g_form_class(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.interface_lng_val = parent.interface_lng_val
        self.con = parent.con
        self.full_dir = parent.full_dir
        self.par = parent

        if self.con.open():

            self.table = QTableWidget(2, 2)
            self.table.setColumnWidth(0, 150)
            self.table.setColumnWidth(1, 330)
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

			# value
            value_lbl = QLabel('value')
            self.x = QLineEdit()
            self.x.setFixedSize(40, 25)
            self.y = QLineEdit()
            self.y.setFixedSize(40, 25)
            self.z = QLineEdit()
            self.z.setFixedSize(40, 25)
            self.value_hbox = QHBoxLayout()
            self.value_hbox.addWidget(self.x)
            self.value_hbox.addWidget(self.y)
            self.value_hbox.addWidget(self.z)
            self.value_w = QWidget()
            self.value_w.setLayout(self.value_hbox)
            self.table.setCellWidget(1, 1, self.value_w)
            self.table.setCellWidget(1, 0, value_lbl)
            self.table.setRowHeight(1, 40)

            # вывод значений параметров
            if 'g' in self.con.tables():						
                query = QtSql.QSqlQuery()
                query.exec("SELECT * FROM g")
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

                    # value
                    self.x.setText(value_list[1].split(' ')[0])
                    self.y.setText(value_list[1].split(' ')[1])
                    self.z.setText(value_list[1].split(' ')[2])
					
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
        self.d_list = [self.d_1.text(), self.d_2.text(), self.d_3.text(), self.d_4.text(), self.d_5.text(), self.d_6.text(), self.d_7.text()]
        self.value_list = [self.x.text(), self.y.text(), self.z.text()]
		
        if '' not in self.d_list and '' not in self.value_list:
		
            dimensions_perem = [self.d_1.text(), self.d_2.text(), self.d_3.text(), self.d_4.text(), self.d_5.text(), self.d_6.text(), self.d_7.text()]
            dimensions_str = ' '.join(dimensions_perem)

            value_perem = [self.x.text(), self.y.text(), self.z.text()]
            value_str = ' '.join(value_perem)

            if 'g' not in self.con.tables():
                query = QtSql.QSqlQuery()
                query.exec("CREATE TABLE g(param, value)")

                query.exec("INSERT INTO g(param, value) VALUES ('%s','%s')" % ('dimensions', dimensions_str))
                query.exec("INSERT INTO g(param, value) VALUES ('%s','%s')" % ('value', value_str))

            if 'g' in self.con.tables():
                query = QtSql.QSqlQuery()

                query.prepare("UPDATE controlDict SET value=? WHERE param='dimensions'")
                query.bindValue(0, dimensions_str)
                query.exec_()
				
                query.prepare("UPDATE controlDict SET value=? WHERE param='value'")
                query.bindValue(0, value_str)
                query.exec_()

			# записываем файл g
            if os.path.exists(self.full_dir + '/constant/g'):
                os.remove(self.full_dir + '/constant/g')

            shutil.copyfile("./matches/Shablon/constant/g", self.full_dir + '/constant/g')

            g = open(self.full_dir + '/constant/g', 'a')

			###dimensions###
            dimensions_bl = '\n' + 'dimensions      ' + '[' + dimensions_str + ']' + ';' + '\n'
			###value###
            value_bl = '\n' + 'value           ' + '(' + self.x.text() + ' ' + self.y.text() + ' ' + self.z.text() + ')' + ';' + '\n\n'

            g.write(dimensions_bl + value_bl)

            close_str = '// ************************************************************************* //'
            g.write(close_str)

            g.close()

            self.par.cdw.setWidget(self.par.outf_scroll)
            outf = open(self.full_dir + '/constant/g')

            if self.interface_lng_val == 'Russian':
                msg_lbl = QLabel(
                    '<span style="color:green">Файл g сохранен</span>')
            elif self.interface_lng_val == 'English':
                msg_lbl = QLabel(
                    '<span style="color:green">g file saved</span>')
				
            data = outf.read()

            if self.interface_lng_val == 'Russian':
                self.par.outf_lbl.setText("Файл " + "<font color='peru'>" + 'g' + "</font>")
            elif self.interface_lng_val == 'English':
                self.par.outf_lbl.setText("<font color='peru'>" + 'g' + "</font>" + " file")
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
			
		
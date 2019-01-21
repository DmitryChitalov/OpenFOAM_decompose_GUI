# -*- coding: utf-8 -*-
# -----------------------------Импорт модулей-----------------------------------

from PyQt5 import QtSql
import os
import os.path
import shutil

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QFormLayout, QTableWidget, QComboBox, \
    QSpinBox, QPushButton, QListWidgetItem, QDoubleSpinBox, QLineEdit

# -----------------------------------Форма--------------------------------------

class controlDict_form_class(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.interface_lng_val = parent.interface_lng_val
        self.con = parent.con
        self.full_dir = parent.full_dir
        self.par = parent

        if self.con.open():

            self.table = QTableWidget(19, 2)
            self.table.setColumnWidth(0, 150)
            self.table.setColumnWidth(1, 230)
            self.table.setFixedSize(674, 480)
            if self.interface_lng_val == 'Russian':
                self.table.setHorizontalHeaderLabels(["Параметр", "Значение"])
            elif self.interface_lng_val == 'English':
                self.table.setHorizontalHeaderLabels(["Parameter", "Value"])
				
            # application
            application_lbl = QLabel('application')
            self.application = QComboBox()
            application_list = ["compressibleInterFoam", "rhoCentralFoam", "sonicFoam", "icoFoam", "pisoFoam"]
            self.application.addItems(application_list)
            self.table.setCellWidget(0, 1, self.application)
            self.table.setCellWidget(0, 0, application_lbl)

            # startFrom
            startFrom_lbl = QLabel('startFrom')
            self.startFrom = QComboBox()
            startFrom_list = ["startTime", "latestTime"]
            self.startFrom.addItems(startFrom_list)
            self.table.setCellWidget(1, 1, self.startFrom)
            self.table.setCellWidget(1, 0, startFrom_lbl)

            # startTime
            startTime_lbl = QLabel('startTime')
            self.startTime = QSpinBox()
            self.table.setCellWidget(2, 1, self.startTime)
            self.table.setCellWidget(2, 0, startTime_lbl)

            # stopAt
            stopAt_lbl = QLabel('stopAt')
            self.stopAt = QComboBox()
            stopAt_list = ["endTime"]
            self.stopAt.addItems(stopAt_list)
            self.table.setCellWidget(3, 1, self.stopAt)
            self.table.setCellWidget(3, 0, stopAt_lbl)

            # endTime
            endTime_lbl = QLabel('endTime')
            self.endTime = QDoubleSpinBox()
            self.endTime.setRange(0, 10000)
            self.table.setCellWidget(4, 1, self.endTime)
            self.table.setCellWidget(4, 0, endTime_lbl)

            # deltaT
            deltaT_lbl = QLabel('deltaT')
            self.deltaT = QLineEdit()
            self.deltaT.setFixedSize(100, 25)
            #self.deltaT.setRange(0, 10000)
            self.table.setCellWidget(5, 1, self.deltaT)
            self.table.setCellWidget(5, 0, deltaT_lbl)

            # writeControl
            writeControl_lbl = QLabel('writeControl')
            self.writeControl = QComboBox()
            writeControl_list = ["timeStep", "adjustableRunTime"]
            self.writeControl.addItems(writeControl_list)
            self.table.setCellWidget(6, 1, self.writeControl)
            self.table.setCellWidget(6, 0, writeControl_lbl)

            # writeInterval
            writeInterval_lbl = QLabel('writeInterval')
            self.writeInterval = QDoubleSpinBox()
            self.writeInterval.setRange(0, 10000)
            self.table.setCellWidget(7, 1, self.writeInterval)
            self.table.setCellWidget(7, 0, writeInterval_lbl)

            # purgeWrite
            purgeWrite_lbl = QLabel('purgeWrite')
            self.purgeWrite = QSpinBox()
            self.purgeWrite.setRange(0, 10000)
            self.table.setCellWidget(8, 1, self.purgeWrite)
            self.table.setCellWidget(8, 0, purgeWrite_lbl)

            # writeFormat
            writeFormat_lbl = QLabel('writeFormat')
            self.writeFormat = QComboBox()
            writeFormat_list = ["ascii", "binary"]
            self.writeFormat.addItems(writeFormat_list)
            self.table.setCellWidget(9, 1, self.writeFormat)
            self.table.setCellWidget(9, 0, writeFormat_lbl)

            # writePrecision
            writePrecision_lbl = QLabel('writePrecision')
            self.writePrecision = QSpinBox()
            self.writePrecision.setRange(0, 10000)
            self.table.setCellWidget(10, 1, self.writePrecision)
            self.table.setCellWidget(10, 0, writePrecision_lbl)

            # writeCompression
            writeCompression_lbl = QLabel('writeCompression')
            self.writeCompression = QComboBox()
            writeCompression_list = ["off"]
            self.writeCompression.addItems(writeCompression_list)
            self.table.setCellWidget(11, 1, self.writeCompression)
            self.table.setCellWidget(11, 0, writeCompression_lbl)

            # timeFormat
            timeFormat_lbl = QLabel('timeFormat')
            self.timeFormat = QComboBox()
            timeFormat_list = ["general"]
            self.timeFormat.addItems(timeFormat_list)
            self.table.setCellWidget(12, 1, self.timeFormat)
            self.table.setCellWidget(12, 0, timeFormat_lbl)

            # timePrecision
            timePrecision_lbl = QLabel('timePrecision')
            self.timePrecision = QSpinBox()
            self.timePrecision.setRange(0, 10000)
            self.table.setCellWidget(13, 1, self.timePrecision)
            self.table.setCellWidget(13, 0, timePrecision_lbl)
			
			# runTimeModifiable
            runTimeModifiable_lbl = QLabel('runTimeModifiable')
            self.runTimeModifiable = QComboBox()
            runTimeModifiable_list = ["yes", "no"]
            self.runTimeModifiable.addItems(runTimeModifiable_list)
            self.table.setCellWidget(14, 1, self.runTimeModifiable)
            self.table.setCellWidget(14, 0, runTimeModifiable_lbl)
			
			# adjustTimeStep
            adjustTimeStep_lbl = QLabel('adjustTimeStep')
            self.adjustTimeStep = QComboBox()
            adjustTimeStep_list = ["yes", "no"]
            self.adjustTimeStep.addItems(adjustTimeStep_list)
            self.table.setCellWidget(15, 1, self.adjustTimeStep)
            self.table.setCellWidget(15, 0, adjustTimeStep_lbl)
			
			# maxCo
            maxCo_lbl = QLabel('maxCo')
            self.maxCo = QDoubleSpinBox()
            self.maxCo.setRange(0, 10000)
            self.table.setCellWidget(16, 1, self.maxCo)
            self.table.setCellWidget(16, 0, maxCo_lbl)
			
			# maxAlphaCo
            maxAlphaCo_lbl = QLabel('maxAlphaCo')
            self.maxAlphaCo = QDoubleSpinBox()
            self.maxAlphaCo.setRange(0, 10000)
            self.table.setCellWidget(17, 1, self.maxAlphaCo)
            self.table.setCellWidget(17, 0, maxAlphaCo_lbl)
			
			# maxDeltaT
            maxDeltaT_lbl = QLabel('maxDeltaT')
            self.maxDeltaT = QSpinBox()
            self.maxDeltaT.setRange(0, 10000)
            self.table.setCellWidget(18, 1, self.maxDeltaT)
            self.table.setCellWidget(18, 0, maxDeltaT_lbl)
			
            # вывод значений параметров
            if 'controlDict' in self.con.tables():						
                query = QtSql.QSqlQuery()
                query.exec("SELECT * FROM controlDict")
                if query.isActive():
                    query.first()
                    value_list = []
                    while query.isValid():
                        value_res = query.value('value')
                        value_list.append(value_res)
                        query.next()
					
                    # application
                    application_mas = self.application.count()   
                    for i in range(application_mas):
                        if self.application.itemText(i) == value_list[0]:
                            self.application.setCurrentIndex(i)
							
                    # startFrom
                    startFrom_mas = self.startFrom.count()   
                    for i in range(startFrom_mas):
                        if self.startFrom.itemText(i) == value_list[1]:
                            self.startFrom.setCurrentIndex(i)
							
                    # startTime
                    self.startTime.setValue(value_list[2])
					
                    # stopAt
                    stopAt_mas = self.stopAt.count()   
                    for i in range(stopAt_mas):
                        if self.stopAt.itemText(i) == value_list[3]:
                            self.stopAt.setCurrentIndex(i)
							
                    # endTime
                    self.endTime.setValue(value_list[4])
					
                    # deltaT
                    self.deltaT.setText(str(value_list[5]))
					
                    # writeControl
                    writeControl_mas = self.writeControl.count()   
                    for i in range(writeControl_mas):
                        if self.writeControl.itemText(i) == value_list[6]:
                            self.writeControl.setCurrentIndex(i)
							
                    # writeInterval
                    self.writeInterval.setValue(value_list[7])
					
                    # purgeWrite
                    self.purgeWrite.setValue(value_list[8])
					
                    # writeFormat
                    writeFormat_mas = self.writeFormat.count()   
                    for i in range(writeFormat_mas):
                        if self.writeFormat.itemText(i) == value_list[9]:
                            self.writeFormat.setCurrentIndex(i)
							
                    # writePrecision
                    self.writePrecision.setValue(value_list[10])
					
                    # writeCompression
                    writeCompression_mas = self.writeCompression.count()   
                    for i in range(writeCompression_mas):
                        if self.writeCompression.itemText(i) == value_list[11]:
                            self.writeCompression.setCurrentIndex(i)
							
                    # timeFormat
                    timeFormat_mas = self.timeFormat.count()   
                    for i in range(timeFormat_mas):
                        if self.timeFormat.itemText(i) == value_list[12]:
                            self.timeFormat.setCurrentIndex(i)
							
                    # timePrecision
                    self.timePrecision.setValue(value_list[13])
					
					# runTimeModifiable
                    runTimeModifiable_mas = self.runTimeModifiable.count()   
                    for i in range(runTimeModifiable_mas):
                        if self.runTimeModifiable.itemText(i) == value_list[14]:
                            self.runTimeModifiable.setCurrentIndex(i)

					# adjustTimeStep
                    adjustTimeStep_mas = self.adjustTimeStep.count()   
                    for i in range(adjustTimeStep_mas):
                        if self.adjustTimeStep.itemText(i) == value_list[15]:
                            self.adjustTimeStep.setCurrentIndex(i)

					# maxCo
                    self.maxCo.setValue(value_list[16])

					# maxAlphaCo
                    self.maxAlphaCo.setValue(value_list[17])

					# maxDeltaT
                    self.maxDeltaT.setValue(value_list[18])
					
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
        application_txt = self.application.currentText()
        startFrom_txt = self.startFrom.currentText()
        startTime_txt = self.startTime.value()
        stopAt_txt = self.stopAt.currentText()
        endTime_txt = self.endTime.value()
        deltaT_txt = self.deltaT.text()
        writeControl_txt = self.writeControl.currentText()
        writeInterval_txt = self.writeInterval.value()
        purgeWrite_txt = self.purgeWrite.value()
        writeFormat_txt = self.writeFormat.currentText()
        writePrecision_txt = self.writePrecision.value()
        writeCompression_txt = self.writeCompression.currentText()
        timeFormat_txt = self.timeFormat.currentText()
        timePrecision_txt = self.timePrecision.value()
        runTimeModifiable_txt = self.runTimeModifiable.currentText() 
        adjustTimeStep_txt = self.adjustTimeStep.currentText()
        maxCo_txt = self.maxCo.value()
        maxAlphaCo_txt = self.maxAlphaCo.value()
        maxDeltaT_txt = self.maxDeltaT.value()
		
        self.par.application = application_txt	
        
        if 'controlDict' not in self.con.tables():
            query = QtSql.QSqlQuery()
            query.exec("CREATE TABLE controlDict(param, value)")

            query.exec("INSERT INTO controlDict(param, value) VALUES ('%s','%s')" % ('application', ''))
            query.exec("INSERT INTO controlDict(param, value) VALUES ('%s','%s')" % ('startFrom', ''))
            query.exec("INSERT INTO controlDict(param, value) VALUES ('%s','%s')" % ('startTime', ''))
            query.exec("INSERT INTO controlDict(param, value) VALUES ('%s','%s')" % ('stopAt', ''))
            query.exec("INSERT INTO controlDict(param, value) VALUES ('%s','%s')" % ('endTime', ''))
            query.exec("INSERT INTO controlDict(param, value) VALUES ('%s','%s')" % ('deltaT', ''))
            query.exec("INSERT INTO controlDict(param, value) VALUES ('%s','%s')" % ('writeControl', ''))
            query.exec("INSERT INTO controlDict(param, value) VALUES ('%s','%s')" % ('writeInterval', ''))
            query.exec("INSERT INTO controlDict(param, value) VALUES ('%s','%s')" % ('purgeWrite', ''))
            query.exec("INSERT INTO controlDict(param, value) VALUES ('%s','%s')" % ('writeFormat', ''))
            query.exec("INSERT INTO controlDict(param, value) VALUES ('%s','%s')" % ('writePrecision', ''))
            query.exec("INSERT INTO controlDict(param, value) VALUES ('%s','%s')" % ('writeCompression', ''))
            query.exec("INSERT INTO controlDict(param, value) VALUES ('%s','%s')" % ('timeFormat', ''))
            query.exec("INSERT INTO controlDict(param, value) VALUES ('%s','%s')" % ('timePrecision', ''))
            query.exec("INSERT INTO controlDict(param, value) VALUES ('%s','%s')" % ('runTimeModifiable', ''))
            query.exec("INSERT INTO controlDict(param, value) VALUES ('%s','%s')" % ('adjustTimeStep', ''))
            query.exec("INSERT INTO controlDict(param, value) VALUES ('%s','%s')" % ('maxCo', ''))
            query.exec("INSERT INTO controlDict(param, value) VALUES ('%s','%s')" % ('maxAlphaCo', ''))
            query.exec("INSERT INTO controlDict(param, value) VALUES ('%s','%s')" % ('maxDeltaT', ''))


        if 'controlDict' in self.con.tables():
            query = QtSql.QSqlQuery()

            query.prepare("UPDATE controlDict SET value=? WHERE param='application'")
            query.bindValue(0, application_txt)
            query.exec_()

            query.prepare("UPDATE controlDict SET value=? WHERE param='startFrom'")
            query.bindValue(0, startFrom_txt)
            query.exec_()

            query.prepare("UPDATE controlDict SET value=? WHERE param='startTime'")
            query.bindValue(0, startTime_txt)
            query.exec_()

            query.prepare("UPDATE controlDict SET value=? WHERE param='stopAt'")
            query.bindValue(0, stopAt_txt)
            query.exec_()

            query.prepare("UPDATE controlDict SET value=? WHERE param='endTime'")
            query.bindValue(0, endTime_txt)
            query.exec_()

            query.prepare("UPDATE controlDict SET value=? WHERE param='deltaT'")
            query.bindValue(0, deltaT_txt)
            query.exec_()

            query.prepare("UPDATE controlDict SET value=? WHERE param='writeControl'")
            query.bindValue(0, writeControl_txt)
            query.exec_()

            query.prepare("UPDATE controlDict SET value=? WHERE param='writeInterval'")
            query.bindValue(0, writeInterval_txt)
            query.exec_()

            query.prepare("UPDATE controlDict SET value=? WHERE param='purgeWrite'")
            query.bindValue(0, purgeWrite_txt)
            query.exec_()

            query.prepare("UPDATE controlDict SET value=? WHERE param='purgeWrite'")
            query.bindValue(0, purgeWrite_txt)
            query.exec_()

            query.prepare("UPDATE controlDict SET value=? WHERE param='writeFormat'")
            query.bindValue(0, writeFormat_txt)
            query.exec_()

            query.prepare("UPDATE controlDict SET value=? WHERE param='writePrecision'")
            query.bindValue(0, writePrecision_txt)
            query.exec_()

            query.prepare("UPDATE controlDict SET value=? WHERE param='writeCompression'")
            query.bindValue(0, writeCompression_txt)
            query.exec_()

            query.prepare("UPDATE controlDict SET value=? WHERE param='timeFormat'")
            query.bindValue(0, timeFormat_txt)
            query.exec_()

            query.prepare("UPDATE controlDict SET value=? WHERE param='timePrecision'")
            query.bindValue(0, timePrecision_txt)
            query.exec_()
			
            query.prepare("UPDATE controlDict SET value=? WHERE param='runTimeModifiable'")
            query.bindValue(0, runTimeModifiable_txt)
            query.exec_()
			
            query.prepare("UPDATE controlDict SET value=? WHERE param='adjustTimeStep'")
            query.bindValue(0, adjustTimeStep_txt)
            query.exec_()
			
            query.prepare("UPDATE controlDict SET value=? WHERE param='maxCo'")
            query.bindValue(0, maxCo_txt)
            query.exec_()
			
            query.prepare("UPDATE controlDict SET value=? WHERE param='maxAlphaCo'")
            query.bindValue(0, maxAlphaCo_txt)
            query.exec_()
			
            query.prepare("UPDATE controlDict SET value=? WHERE param='maxDeltaT'")
            query.bindValue(0, maxDeltaT_txt)
            query.exec_()

        # записываем файл controlDict
        if os.path.exists(self.full_dir + '/system/controlDict'):
            os.remove(self.full_dir + '/system/controlDict')
		
        shutil.copyfile("./matches/Shablon/system/controlDict", self.full_dir + '/system/controlDict')
		
        cD = open(self.full_dir + '/system/controlDict', 'a')
        ###application###
        a_bl = '\n' + 'application     ' + application_txt + ';' + '\n\n'

        ###startFrom###
        sF_bl = 'startFrom       ' + startFrom_txt + ';' + '\n\n'

        ###startTime###
        sT_bl = 'startTime       ' + str(startTime_txt) + ';' + '\n\n'

        ###stopAt###
        sA_bl = 'stopAt          ' + stopAt_txt + ';' + '\n\n'

        ###endTime###
        sTi_bl = 'endTime         ' + str(endTime_txt) + ';' + '\n\n'

        ###deltaT###
        dT_bl = 'deltaT          ' + str(deltaT_txt) + ';' + '\n\n'

        ###writeControl###
        wC_bl = 'writeControl    ' + writeControl_txt + ';' + '\n\n'

        ###writeInterval###
        wI_bl = 'writeInterval   ' + str(writeInterval_txt) + ';' + '\n\n'

        ###purgeWrite###
        pW_bl = 'purgeWrite      ' + str(purgeWrite_txt) + ';' + '\n\n'

        ###writeFormat###
        wF_bl = 'writeFormat     ' + writeFormat_txt + ';' + '\n\n'

        ###writePrecision###
        wP_bl = 'writePrecision  ' + str(writePrecision_txt) + ';' + '\n\n'

        ###writeCompression###
        wCo_bl = 'writeCompression ' + writeCompression_txt + ';' + '\n\n'

        ###timeFormat###
        tF_bl = 'timeFormat      ' + timeFormat_txt + ';' + '\n\n'

        ###timePrecision###
        tP_bl = 'timePrecision   ' + str(timePrecision_txt) + ';' + '\n\n'
		
		###runTimeModifiable###
        rTM_bl = 'runTimeModifiable ' + runTimeModifiable_txt + ';' + '\n\n'
		
		###adjustTimeStep###
        aTS_bl = 'adjustTimeStep  ' + adjustTimeStep_txt + ';' + '\n\n'
		
		###maxCo###
        mC_bl = 'maxCo           ' + str(maxCo_txt) + ';' + '\n\n'
		
		###maxAlphaCo###
        mAC_bl = 'maxAlphaCo      ' + str(maxAlphaCo_txt) + ';' + '\n\n'
		
		###maxDeltaT###
        mDT_bl = 'maxDeltaT       ' + str(maxDeltaT_txt) + ';' + '\n\n'
		
        if deltaT_txt != '':

            cD.write(a_bl + sF_bl + sT_bl + sA_bl + sTi_bl + dT_bl + wC_bl + wI_bl + pW_bl + wF_bl + wP_bl + wCo_bl + tF_bl + tP_bl + rTM_bl + aTS_bl + mC_bl + mAC_bl + mDT_bl)
            close_str = '// ************************************************************************* //'
            cD.write(close_str)

            cD.close()

            self.par.cdw.setWidget(self.par.outf_scroll)
            outf = open(self.full_dir + '/system/controlDict')

            if self.interface_lng_val == 'Russian':
                msg_lbl = QLabel(
                    '<span style="color:green">Файл controlDict сохранен</span>')
            elif self.interface_lng_val == 'English':
                msg_lbl = QLabel(
                    '<span style="color:green">The controlDict file saved</span>')

            data = outf.read()

            if self.interface_lng_val == 'Russian':
                self.par.outf_lbl.setText("Файл " + "<font color='peru'>" + 'controlDict' + "</font>")
            elif self.interface_lng_val == 'English':
                self.par.outf_lbl.setText("<font color='peru'>" + 'controlDict' + "</font>" + " file")
            self.par.outf_edit.setText(data)

            self.par.cdw.setTitleBarWidget(self.par.cdw_frame)
            outf.close()
        else:
            if self.interface_lng_val == 'Russian':
                msg_lbl = QLabel(
                    '<span style="color:green">Укажите значение параметра deltaT</span>')
            elif self.interface_lng_val == 'English':
                msg_lbl = QLabel(
                    '<span style="color:green">Specify deltaT value</span>')
            
        self.par.listWidget.clear()
        self.par.item = QListWidgetItem()
        self.par.listWidget.addItem(self.par.item)
        self.par.listWidget.setItemWidget(self.par.item, msg_lbl)

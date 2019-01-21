# -*- coding: utf-8 -*-
# -------------------------------Импорт модулей----------------------------------

import shutil
import sys
import re
import os
import os.path
import traceback

from PyQt5 import QtCore
from PyQt5 import QtSql
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QFileDialog, QLineEdit, QLabel, \
    QHBoxLayout, QLineEdit, QPushButton, QGridLayout, \
    QFrame, QVBoxLayout, QFormLayout, QFileDialog, QRadioButton, QStyle, \
    QComboBox, QFrame

# ---------------------------Главная форма проекта-------------------------------

class prj_window_class(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowSystemMenuHint)
        self.setWindowModality(QtCore.Qt.WindowModal)

        global par
        par = parent

        global int_lng
        int_lng = par.interface_lng_val

        # ------------------------Функции связанные с формой-----------------------------

        # .....Функция, запускаемая при нажатии радио-кнопки "создать новый проект"......

        def on_np_clicked():
            if np_radio.isChecked():
                title_label.setEnabled(True)
                project_frame.setEnabled(True)
                project_frame.setStyleSheet("border-color: dimgray;")

                project_name.setEnabled(True)
                project_name.setText("")
                project_path_name.setText("")
                path_button.setEnabled(True)

        # .....Функция, запускаемая при нажатии радио-кнопки "открыть имеющийся проект"......

        def on_cp_clicked():
            if cp_radio.isChecked():
                choice_button.setEnabled(True)
                title_label.setEnabled(False)
                project_frame.setEnabled(False)
                project_frame.setStyleSheet("border-color: darkgray;")
            else:
                choice_button.setEnabled(False)

        # .....Функция, запускаемая при нажатии кнопки "выбрать имеющийся проект"......

        def on_chbtn_clicked():

            folder_dir = QFileDialog.getExistingDirectory(self, directory=QtCore.QDir.currentPath())
            
            self.new_dir, project_name_dir = os.path.split(folder_dir)

            path_button.setEnabled(False)
            title_label.setEnabled(True)
            project_frame.setEnabled(True)
            project_frame.setStyleSheet("border-color: dimgray;")
            project_name.setEnabled(True)
            project_name.setStyleSheet("border-color: silver;")
            project_name.setText(project_name_dir)
            project_path_name.setText(self.new_dir)
            project_path_name.setEnabled(True)
            project_path_name.setStyleSheet("border-color: silver;")

            # --------------------------Функции связанные c выводом-----------------------------

        # .....Функция, запускаемая при нажатии кнопки выбора директории сохранения нового проекта"......

        def on_path_choose():

            self.new_dir = QFileDialog.getExistingDirectory(self, directory=QtCore.QDir.currentPath())
            dir_reg = re.compile(r"\S*(?<=[\/])run(?![\/])")
            dir_mas = dir_reg.findall(self.new_dir)

            project_path_name.setText(self.new_dir)

        # .....Функция, запускаемая при завершении редактирования названия проекта и его директории"......

        def handleEditingFinished():
            if project_name.text() and project_path_name.text():
                save_button.setEnabled(True)

        # ....................Функция, запускаемая при нажатии кнопки "сохранить"....................

        def on_save_clicked():
            par.treeview.model.clear()			
			
            par.fsw.setWidget(par.treeview)
            par.fsw.setTitleBarWidget(par.fsw_frame)
			
            par.serv_mes.setWidget(par.listWidget)
            
            if int_lng == 'Russian':
                par.fsw_grid.itemAtPosition(0, 0).widget().setText("<font color='SeaGreen'>" + "Файловая Cтруктура Проекта" + "</font>")
                serv_mes_default = QLabel("Служебные сообщения")
            elif int_lng == 'English':
                par.fsw_grid.itemAtPosition(0, 0).widget().setText("<font color='SeaGreen'>" + "File Structure of the Project" + "</font>")
                serv_mes_default = QLabel("Service messages")
            par.serv_mes.setTitleBarWidget(serv_mes_default)
			
            par.addDockWidget(QtCore.Qt.LeftDockWidgetArea, par.fsw)
            par.addDockWidget(QtCore.Qt.BottomDockWidgetArea, par.serv_mes)

            prj_name = project_name.text()

            full_dir = self.new_dir + "/" + prj_name

            par.full_dir = full_dir
            par.prj_name = prj_name
			
            if np_radio.isChecked():
                os.mkdir(full_dir)
                os.mkdir(full_dir + "/system")
                os.mkdir(full_dir + "/constant")
                os.mkdir(full_dir + "/0")
                shutil.copy("./matches/Shablon/system/fvSchemes", full_dir + '/system')
                shutil.copy("./matches/Shablon/system/setFieldsDict", full_dir + '/system')
                shutil.copy("./matches/Shablon/system/controlDict", full_dir + '/system')
                shutil.copy("./matches/Shablon/system/fvSolution", full_dir + '/system')
                shutil.copy("./matches/Shablon/system/decomposeParDict", full_dir + '/system')
				
            # ---constant---
            dir_constant_path = full_dir + '/constant'
            if dir_constant_path:
                dir_constant_name = os.path.basename(full_dir + '/constant')
                files_constant = [f for f in os.listdir(full_dir + '/constant/') if os.path.isfile(os.path.join(full_dir + '/constant/', f))]

                item_constant = QtGui.QStandardItem(dir_constant_name)
                par.treeview.model.insertRow(0, item_constant)
                j = 0
                index_constant = par.treeview.model.index(0, 0)
                par.treeview.expand(index_constant)
                for el_constant in files_constant:
                    child_item_constant = QtGui.QStandardItem(el_constant)
                    child_item_constant.setForeground(QtGui.QColor('navy'))
                    item_constant.setChild(j, 0, child_item_constant)
                    j = j + 1

            dir_system_path = full_dir + '/system'
            # ---system---
            dir_system_name = os.path.basename(full_dir + '/system')
            if dir_system_name:
                files_system = ['controlDict', 'decomposeParDict', 'fvSchemes']

                item_system = QtGui.QStandardItem(dir_system_name)
                par.treeview.model.insertRow(0, item_system)
                j = 0
                index_system = par.treeview.model.index(0, 0)
                par.treeview.expand(index_system)
                for el_system in files_system:
                    child_item_system = QtGui.QStandardItem(el_system)
                    child_item_system.setForeground(QtGui.QColor('navy'))
                    item_system.setChild(j, 0, child_item_system)
                    j = j + 1
					
                bMD_name = os.path.exists(full_dir + '/system/blockMeshDict')
                if bMD_name:
                    bMD_system = par.treeview.model.item(0, 0)
                    bMD_system = 'blockMeshDict'
                    child_item_system = QtGui.QStandardItem(bMD_system)
                    child_item_system.setForeground(QtGui.QColor('navy'))
                    item_system.setChild(3, 0, child_item_system)
                    par.file_open.setEnabled(True)
					
                sHMD_name = os.path.exists(full_dir + '/system/snappyHexMeshDict')
                if sHMD_name:
                    sHMD_system = par.treeview.model.item(0, 0)
                    sHMD_system = 'snappyHexMeshDict'
                    child_item_system = QtGui.QStandardItem(sHMD_system)
                    child_item_system.setForeground(QtGui.QColor('navy'))
                    item_system.setChild(3, 0, child_item_system)
                    par.file_open.setEnabled(True)
			
			# ---0---
            dir_0_name = os.path.basename(full_dir + '/0')
            if dir_system_name:
                item_0 = QtGui.QStandardItem(dir_0_name)
                par.treeview.model.insertRow(2, item_0)
                if cp_radio.isChecked():
                    if os.path.exists(full_dir + '/0') and os.listdir(full_dir + '/0'):
                        files_0 = [f for f in os.listdir(full_dir + '/0/') if os.path.isfile(os.path.join(full_dir + '/0/', f))]
                        j = 0
                        index = par.treeview.model.index(2, 0)
                        par.treeview.expand(index)
                        for el_0 in files_0:
                            child_item_0 = QtGui.QStandardItem(el_0)
                            child_item_0.setForeground(QtGui.QColor('navy'))
                            item_0.setChild(j, 0, child_item_0)
                            j = j + 1

            prj_lbl = QLabel()
            if int_lng == 'Russian':
                prj_lbl.setText('Путь до директории проекта:')
            elif int_lng == 'English':
                prj_lbl.setText('Path to mesh file:')

            prj_lbl.setStyleSheet("border-style: none;" "font-size: 10pt;")
            prj_path_lbl = QLineEdit()
            prj_path_lbl.setStyleSheet("background-color: white;" "font-size: 10pt;" "color: green;")
            prj_path_lbl.setFixedSize(500, 25)
            prj_path_lbl.setText(full_dir)
            prj_path_lbl.setEnabled(False)
            par.tdw_grid.addWidget(prj_lbl, 0, 0, alignment=QtCore.Qt.AlignCenter)
            par.tdw_grid.addWidget(prj_path_lbl, 0, 1, alignment=QtCore.Qt.AlignCenter)

            # Создаем все таблицы, которые нужны
            if not os.path.exists(full_dir + '/db_data'):
                os.mkdir(full_dir + '/db_data')
            db_path = full_dir + '/db_data/db.sqlite'
			
            if par.con == '':
                con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
                con.setDatabaseName(db_path)
                con.open()
                par.con = con

            parent.msh_open.setEnabled(True)

            self.close()
			
            contDict_file = os.path.exists(par.full_dir + '/system/controlDict')
            if os.path.exists(contDict_file) == True:		
                query = QtSql.QSqlQuery()
                query.exec("SELECT * FROM controlDict")
                if query.isActive():
                    query.first()
                    value_list = []
                    while query.isValid():
                        value_res = query.value('value')
                        value_list.append(value_res)
                        query.next()
                parent.application = value_list[0]
				
            for el in os.listdir(par.full_dir):
                if 'processor' in el:
                    shutil.rmtree(par.full_dir + '/' + el)

        # .....................Функция, запускаемая при нажатии кнопки "отмена"......................

        def on_cancel_clicked():
            self.close()
            self.clear_label = QLabel()
            parent.ffw.setTitleBarWidget(self.clear_label)

        # ------------------------------------Первый блок формы--------------------------------------
		
        if int_lng == 'Russian':
            choice_label = QLabel("Создайте новый проект или откройте имеющийся")
            np_radio = QRadioButton("Создать новый проект")
            cp_radio = QRadioButton("Открыть имеющийся проект")
        elif int_lng == 'English':
            choice_label = QLabel("Create a new project or open an existing one")
            np_radio = QRadioButton("Create a new project")
            cp_radio = QRadioButton("Open existing project")

        cl_hbox = QHBoxLayout()
        cl_hbox.addWidget(choice_label)
        
        np_radio.toggled.connect(on_np_clicked)
        
        cp_radio.toggled.connect(on_cp_clicked)
        icon = self.style().standardIcon(QStyle.SP_DirOpenIcon)
        choice_button = QPushButton()
        choice_button.setFixedSize(30, 30)
        choice_button.setIcon(icon)
        choice_button.setEnabled(False)
        choice_button.clicked.connect(on_chbtn_clicked)
        ch_grid = QGridLayout()
        ch_grid.addWidget(np_radio, 0, 0)
        ch_grid.addWidget(cp_radio, 0, 1)
        ch_grid.addWidget(choice_button, 0, 2)
        ch_frame = QFrame()

        ch_frame.setFrameShape(QFrame.Panel)
        ch_frame.setFrameShadow(QFrame.Sunken)
        ch_frame.setLayout(ch_grid)
        ch_hbox = QHBoxLayout()
        ch_hbox.addWidget(ch_frame)

        # -------------------------------------Второй блок формы------------------------------------
		
        if int_lng == 'Russian':
            title_label = QLabel("Введите название задачи")
            project_label = QLabel("Название проекта:")
        elif int_lng == 'English':
            title_label = QLabel("Enter project name")
            project_label = QLabel("Project name:")

        title_label.setEnabled(False)
        tl_hbox = QHBoxLayout()
        tl_hbox.addWidget(title_label)
        
        project_name = QLineEdit()
        project_name.textChanged.connect(handleEditingFinished)
        project_name.setFixedSize(180, 25)
        valid = QtGui.QRegExpValidator(QtCore.QRegExp("\S*"), self)
        project_name.setValidator(valid)

        if int_lng == 'Russian':
            project_path_label = QLabel("Путь:")
        elif int_lng == 'English':
            project_path_label = QLabel("Path:")
        project_path_name = QLineEdit()
        project_path_name.setEnabled(False)
        project_path_name.textChanged.connect(handleEditingFinished)
        project_path_name.setFixedSize(180, 25)
        path_button = QPushButton("...")
        path_button.clicked.connect(on_path_choose)
        path_button.setFixedSize(25, 25)
        project_grid = QGridLayout()
        project_grid.addWidget(project_label, 0, 0)
        project_grid.addWidget(project_name, 0, 1, alignment=QtCore.Qt.AlignRight)
        project_grid.addWidget(project_path_label, 1, 0)
        project_grid.addWidget(project_path_name, 1, 1)
        project_grid.addWidget(path_button, 1, 2)
        project_frame = QFrame()

        project_frame.setEnabled(False)
        project_frame.setStyleSheet("border-color: darkgray;")
        project_frame.setFrameShape(QFrame.Panel)
        project_frame.setFrameShadow(QFrame.Sunken)
        project_frame.setLayout(project_grid)
        project_grid_vbox = QVBoxLayout()
        project_grid_vbox.addWidget(project_frame)

        # ---------------------Кнопки сохранения и отмены и их блок-------------------------
		
        if int_lng == 'Russian':
            save_button = QPushButton("Сохранить")
            cancel_button = QPushButton("Отмена")
        elif int_lng == 'English':
            save_button = QPushButton("Save")
            cancel_button = QPushButton("Cancel")

        save_button.setFixedSize(80, 25)
        save_button.clicked.connect(on_save_clicked)
        save_button.setEnabled(False)
        
        cancel_button.setFixedSize(80, 25)
        cancel_button.clicked.connect(on_cancel_clicked)
        buttons_hbox = QHBoxLayout()
        buttons_hbox.addWidget(save_button)
        buttons_hbox.addWidget(cancel_button)

        # -------------------------Фрейм формы---------------------------

        bound_grid = QGridLayout()
        bound_grid.addLayout(cl_hbox, 0, 0, alignment=QtCore.Qt.AlignCenter)
        bound_grid.addLayout(ch_hbox, 1, 0, alignment=QtCore.Qt.AlignCenter)
        bound_grid.addLayout(tl_hbox, 2, 0, alignment=QtCore.Qt.AlignCenter)
        bound_grid.addLayout(project_grid_vbox, 3, 0, alignment=QtCore.Qt.AlignCenter)
        bound_grid.addLayout(buttons_hbox, 4, 0, alignment=QtCore.Qt.AlignCenter)
        bound_frame = QFrame()
        bound_frame.setStyleSheet(open("./styles/properties_form_style.qss", "r").read())
        bound_frame.setLayout(bound_grid)
        bound_vbox = QVBoxLayout()
        bound_vbox.addWidget(bound_frame)

        # --------------------Размещение на форме всех компонентов---------

        form_1 = QFormLayout()
        form_1.addRow(bound_vbox)
        self.setLayout(form_1)


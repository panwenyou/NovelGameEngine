#-*- coding:utf-8 -*-


import sys
import os
import time

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from MyFrame import MyFrame
from ToolFrame import ToolFrame
from TreeFrame import TreeFrame
from PropertyFrame import PropertyFrame
from CategoryFrame import CategoryFrame
from InputDlg import InputDlg

from utils import file_util, common_util


class CentralWidget(QWidget):
    def __init__(self):
        super(CentralWidget, self).__init__()
        self.initLayout()
        self.initWidgets()

    def initLayout(self):
        self.layout = QHBoxLayout()
        self.h_splliter = QSplitter(Qt.Horizontal)
        self.left_frame = ToolFrame(self, u'工具栏')
        self.left_frame.setFrameShape(QFrame.StyledPanel)
        height = self.left_frame.frameGeometry().height()
        self.left_frame.resize(150, height)
        self.middle_frame = TreeFrame(self, u'情节树')
        self.middle_frame.setFrameShape(QFrame.StyledPanel)

        self.right_splliter = QSplitter(Qt.Vertical)
        self.right_top_frame = PropertyFrame(self, u'属性窗口')
        self.right_top_frame.setFrameShape(QFrame.StyledPanel)
        common_util.property_frame = self.right_top_frame

        self.right_bottom_frame = CategoryFrame(self, u'章节')
        self.right_bottom_frame.setFrameShape(QFrame.StyledPanel)
        self.right_splliter.addWidget(self.right_top_frame)
        self.right_splliter.addWidget(self.right_bottom_frame)
        self.right_splliter.setStretchFactor(1, 1)
        height = self.right_splliter.frameGeometry().height()
        self.right_splliter.resize(200, height)

        self.h_splliter.addWidget(self.left_frame)
        self.h_splliter.addWidget(self.middle_frame)
        self.h_splliter.addWidget(self.right_splliter)

        self.h_splliter.setStretchFactor(1,1)

        self.layout.addWidget(self.h_splliter)
        self.setLayout(self.layout)

    def initWidgets(self):
        pass


class CentralWindow(QMainWindow):
    def __init__(self):
        super(CentralWindow, self).__init__()
        
        self.initMenu()
        
        self.widget = CentralWidget()
        self.setCentralWidget(self.widget)

        self.setGeometry(300, 100, 1200, 800)
        self.setWindowTitle('NovelEditor')    
        self.show()
        
    
    def initMenu(self):
        new_story_act = QAction("新建故事", self)
        new_story_act.setShortcut('Ctrl+N')
        new_story_act.triggered.connect(self.onNewStory)

        img_path = file_util.getImageFilePath('exit.png')
        exit_act = QAction(QIcon(img_path), '退出', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.setStatusTip('退出')
        exit_act.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('文件')
        file_menu.addAction(new_story_act)
        file_menu.addAction(exit_act)

        self.toolbar = self.addToolBar('退出')
        self.toolbar.addAction(exit_act)

    def onNewStory(self):
        print 'on new story'
        self.input_dlg = InputDlg()
        self.input_dlg.setGeometry(300, 100, 200, 100)
        self.input_dlg.buildInput(('name',), self.onStroyBuild)
        self.input_dlg.show()

    def onStroyBuild(self, data_dict):
        self.input_dlg = None
        name = data_dict['name']['widget'].text()
        print name
    
    
    
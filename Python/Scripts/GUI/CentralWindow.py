#-*- coding:utf-8 -*-


import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from MyFrame import MyFrame
from ToolFrame import ToolFrame
from TreeFrame import TreeFrame

from utils import file_utils


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
        self.right_top_frame = MyFrame(self, u'属性窗口')
        self.right_top_frame.setFrameShape(QFrame.StyledPanel)
        self.right_bottom_frame = MyFrame(self, u'章节')
        self.right_bottom_frame.setFrameShape(QFrame.StyledPanel)
        self.right_splliter.addWidget(self.right_top_frame)
        self.right_splliter.addWidget(self.right_bottom_frame)
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

        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('NovelEditor')    
        self.show()
        
    
    def initMenu(self):
        img_path = file_utils.getImageFilePath('exit.png')
        exitAct = QAction(QIcon(img_path), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAct)
    
    
    
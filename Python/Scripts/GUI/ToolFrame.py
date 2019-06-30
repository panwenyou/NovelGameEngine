#-*- coding:utf-8 -*-


import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from utils import file_utils
from MyFrame import MyFrame


class ListView(QWidget):
    def __init__(self):
        super(ListView, self).__init__()
        self.v_layout = QVBoxLayout()
        for filename in range(20):
            MapButton = QPushButton('click', self)
            self.v_layout.addWidget(MapButton)
        self.v_layout.addStretch(1)
        self.setLayout(self.v_layout)


class ToolFrame(MyFrame):
    def __init__(self, widget=None, title=''):
        super(ToolFrame, self).__init__(widget, title)

    def initUI(self):
        self.scroll_area = QScrollArea()
        self.list_view = ListView()
        self.scroll_area.resize(100, 1000)
        self.scroll_area.setWidget(self.list_view)
        self.root_panel.addWidget(self.scroll_area)


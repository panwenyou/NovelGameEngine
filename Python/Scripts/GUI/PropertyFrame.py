#-*- coding:utf-8 -*-


import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QDrag, QPainter, QColor, QBrush
from PyQt5.QtCore import Qt, QMimeData, QRect


from utils import file_utils
from MyFrame import MyFrame

from data.tools_data import tools
from data.property_data import properties
from data import consts


class EditWindowWidget(QWidget):
    def __init__(self, title, widget=None):
        super(EditWindowWidget, self).__init__(widget)

        self.h_layout = QHBoxLayout()
        self.label = QLabel(title)
        self.text_edit = QLineEdit('')
        self.btn = QPushButton("edit")
        self.h_layout.addWidget(self.label)
        self.h_layout.addWidget(self.text_edit)
        self.h_layout.addWidget(self.btn)
        self.h_layout.setStretchFactor(self.text_edit, 1)
        self.setLayout(self.h_layout)

    def setContent(self, data):
        self.text_edit.text = QString(data)


class TextWidget(QWidget):
    def __init__(self, title, widget=None):
        super(TextWidget, self).__init__(widget)

        self.h_layout = QHBoxLayout()
        self.label = QLabel(title)
        self.text_edit = QLineEdit('')
        self.h_layout.addWidget(self.label)
        self.h_layout.addWidget(self.text_edit)
        self.h_layout.setStretchFactor(self.text_edit, 1)
        self.setLayout(self.h_layout)

    def setContent(self, data):
        self.text_edit.text = QString(data)


class LabelWidget(QWidget):
    def __init__(self, title, widget=None):
        super(LabelWidget, self).__init__(widget)

        self.h_layout = QHBoxLayout()
        self.label = QLabel(title)
        self.label2 = QLineEdit('')
        self.h_layout.addWidget(self.label)
        self.h_layout.addWidget(self.label2)
        self.h_layout.setStretchFactor(self.label2, 1)
        self.setLayout(self.h_layout)

    def setContent(self, data):
        self.text_edit.text = QString(data)


class PropertyFrame(MyFrame):
    def __init__(self, widget=None, title=''):
        super(PropertyFrame, self).__init__(widget, title)

    def refreshWidgets(self):
        print self.v_layout.count()
        for i in reversed(range(self.v_layout.count())): 
            self.v_layout.itemAt(i).widget().setParent(None)

    def onSetProperty(self, tool_id, data):
        self.refreshWidgets()
        for prop in properties[tool_id]:
            widget = None
            if prop[1] == consts.PROPERTY_LABEL:
                widget = LabelWidget(prop[0])
            elif prop[1] == consts.PROPERTY_TEXT:
                widget = TextWidget(prop[0])
            elif prop[1] == consts.PROPERTY_EDIT_WINDOW:
                widget = EditWindowWidget(prop[0])
            self.v_layout.addWidget(widget)
        self.update()

    def initUI(self):
        self.v_layout = QVBoxLayout()
        self.root_panel.addLayout(self.v_layout)
        self.root_panel.addStretch(1)

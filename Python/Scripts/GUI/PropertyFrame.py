#-*- coding:utf-8 -*-


import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QDrag, QPainter, QColor, QBrush
from PyQt5.QtCore import Qt, QMimeData, QRect


from utils import storyline_util
from MyFrame import MyFrame

from data.tools_data import tools
from data import consts


class EditWindowWidget(QWidget):
    def __init__(self, node_id, title, widget=None):
        super(EditWindowWidget, self).__init__(widget)
        self.node_id = node_id
        self.h_layout = QHBoxLayout()
        self.label = QLabel(title)
        self.btn = QPushButton("edit")
        self.btn.clicked.connect(self.OnEdit)
        self.h_layout.addWidget(self.label)
        self.h_layout.addWidget(self.btn)
        self.h_layout.setStretchFactor(self.btn, 1)
        self.setLayout(self.h_layout)
    
    def OnEdit(self):
        node = storyline_util.GetStoryNode(self.node_id)
        os.system("notepad %s" % node.GetScrptPath())


class TextWidget(QWidget):
    def __init__(self, node_id, title, default, widget=None):
        super(TextWidget, self).__init__(widget)
        self.node_id = node_id
        self.h_layout = QHBoxLayout()
        self.label = QLabel(title)
        self.text_edit = QLineEdit(default)
        self.save_btn = QPushButton("save")
        self.h_layout.addWidget(self.label)
        self.h_layout.addWidget(self.text_edit)
        self.h_layout.addWidget(self.save_btn)
        self.save_btn.clicked.connect(self.OnSave)
        self.h_layout.setStretchFactor(self.text_edit, 1)
        self.setLayout(self.h_layout)
    
    def OnSave(self):
        new_name = self.text_edit.text()
        storyline_util.OnChangeStoryNodeName(self.node_id, new_name)
        cur_wnd.widget.middle_frame.update()

class LabelWidget(QWidget):
    def __init__(self, node_id, title, default, widget=None):
        super(LabelWidget, self).__init__(widget)
        self.node_id = node_id
        self.h_layout = QHBoxLayout()
        self.label = QLabel(title)
        self.label2 = QLabel(default)
        self.h_layout.addWidget(self.label)
        self.h_layout.addWidget(self.label2)
        self.h_layout.setStretchFactor(self.label2, 1)
        self.setLayout(self.h_layout)


class PropertyFrame(MyFrame):
    def __init__(self, widget=None, title=''):
        super(PropertyFrame, self).__init__(widget, title)

    def refreshWidgets(self, node_id):
        for i in reversed(range(self.v_layout.count())): 
            self.v_layout.itemAt(i).widget().setParent(None)
        
        type_widget = LabelWidget(node_id, '类型', storyline_util.GetStoryNodeTypeName(node_id))
        name_widget = TextWidget(node_id, '名称', storyline_util.GetStoryNodeName(node_id))
        script_widget = EditWindowWidget(node_id, '脚本')
        self.v_layout.addWidget(type_widget)
        self.v_layout.addWidget(name_widget)
        self.v_layout.addWidget(script_widget)

        self.update()

    def initUI(self):
        self.v_layout = QVBoxLayout()
        self.root_panel.addLayout(self.v_layout)
        self.root_panel.addStretch(1)

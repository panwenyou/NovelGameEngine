#-*- coding:utf-8 -*-


import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QDrag
from PyQt5.QtCore import Qt, QMimeData


from utils import file_utils
from MyFrame import MyFrame

from data.tools_data import tools


class ToolButton(QPushButton):
    def __init__(self, tool_id, parent):
        super(ToolButton, self).__init__(tools[tool_id]['name'], parent)
        self.tool_id = tool_id

    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.LeftButton:
            return
        mimeData = QMimeData()
        # int转字符串作为text传入mimedata
        mimeData.setText(str(self.tool_id))

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.exec_(Qt.MoveAction)


class ListView(QWidget):
    def __init__(self):
        super(ListView, self).__init__()
        self.v_layout = QVBoxLayout()
        self.setLayout(self.v_layout)

    def initTools(self):
        for tool_id in tools.iterkeys():
            MapButton = ToolButton(tool_id, self)
            self.v_layout.addWidget(MapButton)
        self.v_layout.addStretch(1)
        self.update()


class ToolFrame(MyFrame):
    def __init__(self, widget=None, title=''):
        super(ToolFrame, self).__init__(widget, title)

    def initUI(self):
        self.scroll_area = QScrollArea()
        self.list_view = ListView()
        self.list_view.initTools()
        self.scroll_area.resize(100, 1000)
        self.scroll_area.setWidget(self.list_view)
        self.root_panel.addWidget(self.scroll_area)



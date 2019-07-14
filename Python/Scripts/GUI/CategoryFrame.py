#-*- coding:utf-8 -*-


import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QDrag, QPainter, QColor, QBrush
from PyQt5.QtCore import Qt, QMimeData, QRect, pyqtSlot


from utils import file_utils
from MyFrame import MyFrame

from data.tools_data import tools
from data.property_data import properties
from data import consts


class MyTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent=None):
        super(MyTreeWidgetItem, self).__init__(parent)

        self.str_id = '1'


class MyTreeWidget(QTreeWidget):
    def __init__(self, parent=None):
        super(MyTreeWidget, self).__init__(parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openMenu)

    def openMenu(self, pos):
        menu = QMenu(self)
        quitAction = menu.addAction("Delete")
        action = menu.exec_(self.mapToGlobal(pos))
        if action == quitAction:
            print 'delete'

class CategoryFrame(MyFrame):
    def __init__(self, widget=None, title=''):
        super(CategoryFrame, self).__init__(widget, title)

    def initUI(self):
        self.v_layout = QVBoxLayout()
        self.treeWidget = MyTreeWidget()
        self.treeWidget.setHeaderLabels(["目录"])
        self.treeWidget.currentItemChanged.connect(self.itemSelected)
        self.v_layout.addWidget(self.treeWidget)
        self.v_layout.setStretchFactor(self.treeWidget, 1)
        self.root_panel.addLayout(self.v_layout)
        self.onNewCategory('123')

    def onLoad(self, data):
        pass

    def onNewCategory(self, name):
        root1 = MyTreeWidgetItem(self.treeWidget)
        root1.setText(0, '序章')
        c1 = MyTreeWidgetItem(root1)
        c1.setText(0, '皇子等等')

    @pyqtSlot(MyTreeWidgetItem, MyTreeWidgetItem)
    def itemSelected(self, current, previous):
        print current.str_id

    
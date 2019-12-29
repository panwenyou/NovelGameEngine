#-*- coding:utf-8 -*-


import sys
import os
import time
import functools

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QDrag, QPainter, QColor, QBrush
from PyQt5.QtCore import Qt, QMimeData, QRect, pyqtSlot, QTimer


from utils import file_util, data_util, section_util, common_util
from MyFrame import MyFrame

from data.tools_data import tools
from data.property_data import properties
from data import consts

import InputDlg


class MyTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, key = None, name = None, parent=None):
        super(MyTreeWidgetItem, self).__init__(parent)
        if not key:
            self.section_id = common_util.genId('section')
        else:
            self.section_id = key
        if not name:
            self.name = '章节名'
        else:
            self.name = name

        self.setText(0, self.name)


class MyTreeWidget(QTreeWidget):
    def __init__(self, parent=None):
        super(MyTreeWidget, self).__init__(parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openMenu)

        self.currentItemChanged.connect(self.itemSelected)

        self.cur_item = None

    def clear(self):
        super(MyTreeWidget, self).clear()

    def openMenu(self, pos):
        menu = QMenu(self)
        add_action = menu.addAction("添加章节")
        del_action = menu.addAction("删除章节")
        rename_action = menu.addAction("重命名")
        action = menu.exec_(self.mapToGlobal(pos))
        if action == del_action:
            self.onDeleteAction()
        elif action == add_action:
            self.onAddAction()
        elif action == rename_action:
            self.onRenameAction()

    @pyqtSlot(MyTreeWidgetItem, MyTreeWidgetItem)
    def itemSelected(self, current, previous):
        if current:
            print current.section_id
            self.cur_item = current
            section_util.OnSectionChanged(current.section_id)
            old_id = getattr(previous, 'section_id', None)
            new_id = current.section_id
            cur_wnd.widget.middle_frame.onSectionChanged(old_id, new_id)

    def onAddAction(self):
        self.input_dlg = InputDlg.InputDlg()
        self.input_dlg.buildInput((('name','章节名'),), self.onSectionAdded)
        self.input_dlg.show()

    def onDeleteAction(self):
        if not self.cur_item:
            return
        if self.cur_item is self.root_item:
            return
        # 从章节信息中删除
        section_util.DeleteSection(self.cur_item.section_id)
        # UI删除
        self.cur_item.parent().removeChild(self.cur_item)
        self.cur_item = None
        self.update()

    def onRenameAction(self):
        if self.cur_item is self.root_item:
            return
        self.input_dlg = InputDlg.InputDlg()
        self.input_dlg.buildInput((('name','章节名'),), self.onSectionRenamed)
        self.input_dlg.show()

    def onSectionAdded(self, data_dict):
        self.input_dlg = None
        name = data_dict['name']['widget'].text()
        if not name:
            return
        if self.cur_item:
            section_key = section_util.AddSection(self.cur_item.section_id, name)
            cate_item = MyTreeWidgetItem(section_key, name, self.cur_item)
        else:
            section_key = section_util.AddSection(None, name)
            cate_item = MyTreeWidgetItem(section_key, name, self.root_item)

    def onSectionRenamed(self, data_dict):
        self.input_dlg = None
        name = data_dict['name']['widget'].text()
        if not name:
            return
        if self.cur_item:
            section_util.RenameSection(self.cur_item.section_id, name)
            self.cur_item.setText(0, name)

    def buildTreeItems(self, section, parent=None):
        # 递归创建目录树
        name = section.name
        key = section.id
        if parent:
            cate_item = MyTreeWidgetItem(key, name, parent)
        else:
            cate_item = MyTreeWidgetItem(key, name, self)
        sub_sections = section.sub_sections.values()
        sorted_sub_sections = sorted(sub_sections, key=lambda sub: sub.idx)
        for sub in sorted_sub_sections:
            self.buildTreeItems(sub, cate_item)

class CategoryFrame(MyFrame):
    def __init__(self, widget=None, title=''):
        super(CategoryFrame, self).__init__(widget, title)

    def initUI(self):
        self.v_layout = QVBoxLayout()
        self.treeWidget = MyTreeWidget()
        self.treeWidget.setHeaderLabels(["目录"])
        self.v_layout.addWidget(self.treeWidget)
        self.v_layout.setStretchFactor(self.treeWidget, 1)
        self.root_panel.addLayout(self.v_layout)

    def onLoad(self, data):
        pass

    def buildCategory(self):
        # 要先清空原来的树目录
        self.treeWidget.clear()
        self.treeWidget.buildTreeItems(section_util.GetRootSection())
        self.treeWidget.update()

    def onNewCategory(self):
        # 根据category去初始化目录视图
        self.buildCategory()

    def onRefreshUI(self):
        self.onNewCategory()




    
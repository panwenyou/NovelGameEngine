#-*- coding:utf-8 -*-


import sys
import os
import time
import functools

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QDrag, QPainter, QColor, QBrush
from PyQt5.QtCore import Qt, QMimeData, QRect, pyqtSlot, QTimer


from utils import file_util, data_util
from MyFrame import MyFrame

from data.tools_data import tools
from data.property_data import properties
from data import consts




class MyTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, key = None, name = None, parent=None):
        super(MyTreeWidgetItem, self).__init__(parent)
        if not key:
            self.story_id = ''.join(data_util.cur_story , '_', str(time.time()))
        else:
            self.story_id = key
        if not name:
            self.cate_name = '章节名'
        else:
            self.name = name

        self.setText(0, self.name)


class MyTreeWidget(QTreeWidget):
    def __init__(self, parent=None):
        super(MyTreeWidget, self).__init__(parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openMenu)

    def openMenu(self, pos):
        menu = QMenu(self)
        quitAction = menu.addAction("添加章节")
        quitAction = menu.addAction("删除章节")
        quitAction = menu.addAction("重命名")
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

    def onLoad(self, data):
        pass

    def buildCategory(self, cate_dict, parent):
        # 递归创建目录树
        for key, name in cate_dict.iteritems():
            cate_item = MyTreeWidgetItem(key, name, parent)
            sub_cate = cate_dict.get(cate)
            if sub_cate:
                self.buildCategory(sub_cate, cate_item)

    def onNewCategory(self, story_name):
        # 尝试去读目录结构，如果没有，则新建一个目录结构json file
        root_path = file_util.getStoryFileRoot()
        cat_file_path = ''.join((root_path, '\\', story_name, '\\catetory.json'))
        print 'cat_file_path:', cat_file_path
        if os.path.exists(cat_file_path):
            try:
                f = open(cat_file_path, 'r')
                catetory = json.loads(f.read().strip('\n'))
                data_util.catetory = catetory
            except IOError:
                # 重试
                print ''.join(('read file error:', cat_file_path))
                self.timer = QTimer()
                self.timer.timeout.connect(functools.partial(self.onNewCategory, story_name))
                self.timer.start(100)
                return
        else:
            try:
                f = open(cat_file_path, 'w+')
                f.write('{}')
                catetory = {}
                data_util.catetory = catetory
            except IOError:
                # 重试
                print ''.join(('read file error:', cat_file_path))
                self.timer = QTimer()
                self.timer.timeout.connect(functools.partial(self.onNewCategory, story_name))
                self.timer.start(100)
                return
        f.close()

        # 根据category去初始化目录视图
        self.buildCategory(catetory, self.treeWidget)


    @pyqtSlot(MyTreeWidgetItem, MyTreeWidgetItem)
    def itemSelected(self, current, previous):
        print current.str_id

    def onRefreshUI(self):
        self.onNewCategory(data_util.cur_story)



    
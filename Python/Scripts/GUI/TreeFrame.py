#-*- coding:utf-8 -*-


import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QDrag, QPainter, QColor, QBrush
from PyQt5.QtCore import Qt, QMimeData, QRect


from utils import file_util, common_util, data_util
from MyFrame import MyFrame

from data.tools_data import tools


class Node(object):
    def __init__(self, node_id, tool_id, x, y):
        super(Node, self).__init__()

        self.node_id = node_id
        self.tool_id = tool_id
        self.x = x
        self.y = y
        self.width = 90
        self.height = 60

        self.next_nodes = {}

    def addNext(self, next_node):
        self.next_nodes[next_node.node_id] = next_node

    def cancelNext(self, node_id):
        if node_id in self.next_nodes:
            self.next_nodes.pop(node_id)

    def checkClicked(self, x, y):
        r = self.x + self.width
        b = self.y + self.height
        if x < self.x or y < self.y or x > r or y > b:
            return False
        return True

    def onClicked(self):
        print 'node clicked'
        common_util.property_frame.onSetProperty(self.tool_id, {})

    def drawNode(self, qp):
        color = tools[self.tool_id]['color']
        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')
        qp.setPen(col)
        qp.setBrush(QColor(color[0], color[1], color[2], color[3]))
        qp.drawRect(self.x, self.y, self.width, self.height)
        qp.drawText(QRect(self.x, self.y, self.width, self.height), Qt.AlignCenter, tools[self.tool_id]['name'])


class TreeFrame(MyFrame):
    def __init__(self, widget=None, title=''):
        super(TreeFrame, self).__init__(widget, title)

        self.setAcceptDrops(True)

        self.mousePressEvent = self.onMousePress
        self.mouseMoveEvent = self.onMouseMove
        self.mouseReleaseEvent=self.onMouseRelease

        self.nodes_dict = {}
        self.max_node_id = 0
        self.press_begin_pos = ()
        self.press_begin_node = None
        self.mouse_move_flag = False

    def contextMenuEvent(self, e):
        menu = QMenu(self)
        quitAction = menu.addAction("Quit")
        action = menu.exec_(self.mapToGlobal(e.pos()))
        if action == quitAction:
            qApp.quit()

    def onMousePress(self, e):
        x = e.pos().x()
        y = e.pos().y()
        self.press_begin_pos = (x, y)
        for node in self.nodes_dict.itervalues():
            if node.checkClicked(x, y):
                self.press_begin_node = node
                return

    def onMouseMove(self, e):
        x = e.pos().x()
        y = e.pos().y()
        diff_x = x - self.press_begin_pos[0]
        diff_y = y - self.press_begin_pos[1]
        if self.press_begin_node:
            self.press_begin_node.x += diff_x
            self.press_begin_node.y += diff_y
        else:
            for node in self.nodes_dict.itervalues():
                node.x += diff_x
                node.y += diff_y
        self.press_begin_pos = (x, y)
        self.mouse_move_flag = True
        self.update()

    def onMouseRelease(self, e):
        if not self.mouse_move_flag and self.press_begin_node:
            self.press_begin_node.onClicked()
        self.press_begin_pos = ()
        self.mouse_move_flag = False
        self.press_begin_node = None

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore() 

    def dropEvent(self, e):
        print e.mimeData().text()
        if not data_util.cur_story:
            return
        tool_id = int(e.mimeData().text())
        drop_pos = (e.pos().x(), e.pos().y())
        if tool_id in tools:
            self.nodes_dict[self.max_node_id] = Node(self.max_node_id, tool_id, drop_pos[0], drop_pos[1])
            self.max_node_id += 1
        self.update()

    def paintEvent(self, e):
        super(TreeFrame, self).paintEvent(e)
        qp = QPainter()
        qp.begin(self)
        for node in self.nodes_dict.itervalues():
            node.drawNode(qp)
        qp.end()


#-*- coding:utf-8 -*-


import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QDrag, QPainter, QColor, QBrush
from PyQt5.QtCore import Qt, QMimeData


from utils import file_utils
from MyFrame import MyFrame

from data.tools_data import tools


class Node(object):
    def __init__(self, parent, node_id, title='node', pos=(500, 200)):
        super(Node, self).__init__()

        self.node_id = node_id
        self.title = title
        self.pos = pos
        self.widget = QPushButton(title)
        self.widget.setParent(parent)
        # self.widget.move(self.pos[0], self.pos[1])
        self.widget.clicked.connect(self.onClicked)

        self.next_nodes = {}

    def addNext(self, next_node):
        self.next_nodes[next_node.node_id] = next_node

    def cancelNext(self, node_id):
        if node_id in self.next_nodes:
            self.next_nodes.pop(node_id)

    def onClicked(self):
        print 'node clicked'


class SequenceNode(Node):
    def __init__(self, parent, node_id, title='情节', pos=(10, 10)):
        super(SequenceNode, self).__init__(parent, node_id, title, pos)

    def onClicked(self):
        print 'SequenceNode clicked'


class BranchNode(Node):
    def __init__(self, parent, node_id, title='分枝', pos=(10, 10)):
        super(BranchNode, self).__init__(parent, node_id, title, pos)

    def onClicked(self):
        print 'BranchNode clicked'


class EventNode(Node):
    def __init__(self, parent, node_id, title='事件', pos=(10, 10)):
        super(EventNode, self).__init__(parent, node_id, title, pos)

    def onClicked(self):
        print 'EventNode clicked'


class DialogNode(Node):
    def __init__(self, parent, node_id, title='对话', pos=(10, 10)):
        super(DialogNode, self).__init__(parent, node_id, title, pos)

    def onClicked(self):
        print 'DialogNode clicked'


class JumpNode(Node):
    def __init__(self, parent, node_id, title='跳转', pos=(10, 10)):
        super(JumpNode, self).__init__(parent, node_id, title, pos)

    def onClicked(self):
        print 'JumpNode clicked'


class TreeFrame(MyFrame):
    def __init__(self, widget=None, title=''):
        super(TreeFrame, self).__init__(widget, title)

        self.setAcceptDrops(True)

        self.nodes_dict = {}



    def dragEnterEvent(self, e):

        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore() 

    def dropEvent(self, e):
        # print e.mimeData().text()
        # print e.pos().x()
        tool_id = int(e.mimeData().text())
        drop_pos = (e.pos().x(), e.pos().y())
        print drop_pos
        if tool_id in tools:
            self.draw_rect()

    def draw_rect(self):
        qp = QPainter()
        qp.begin(self)

        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')
        qp.setPen(col)

        qp.setBrush(QColor(200, 0, 0))
        qp.drawRect(10, 15, 90, 60)

        qp.end()


    def initUI(self):
        pass


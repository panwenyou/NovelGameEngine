#-*- coding:utf-8 -*-


import sys
import os
import json
import math
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QDrag, QPainter, QColor, QBrush, QPen
from PyQt5.QtCore import Qt, QMimeData, QRect


from utils import file_util, common_util, data_util, storyline_util
from MyFrame import MyFrame

from data.tools_data import tools


class Node(object):
    def __init__(self, tool_id, x, y, node_id=None, width=90, height=60):
        super(Node, self).__init__()
        if not node_id:
            node_id = storyline_util.OnAddNode(tool_id)
        self.node_id = node_id
        self.tool_id = tool_id
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.relative_lines = []

    def addNext(self, next_node):
        storyline_util.OnAddNext(self.node_id, next_node.node_id)

    def cancelNext(self, next_node):
        storyline_util.OnCancelNext(self.node_id, next_node.node_id)

    def checkClicked(self, x, y):
        r = self.x + self.width
        b = self.y + self.height
        if x < self.x or y < self.y or x > r or y > b:
            return False
        return True

    def onClicked(self):
        print 'node clicked'
        cur_wnd.widget.right_top_frame.refreshWidgets(self.node_id)

    def drawNode(self, qp):
        color = tools[self.tool_id]['color']
        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')
        qp.setPen(col)
        qp.setBrush(QColor(color[0], color[1], color[2], color[3]))
        qp.drawRect(self.x, self.y, self.width, self.height)
        text = "%s(%s)" % (storyline_util.GetStoryNodeName(self.node_id), tools[self.tool_id]['name'])
        qp.drawText(QRect(self.x, self.y, self.width, self.height), Qt.AlignCenter, text)

    def Pack(self):
        return {"node_id": self.node_id, "tool_id": self.tool_id, "x": self.x, "y": self.y, "width": self.width, "height": self.height}

    def AddRelativeLine(self, line):
        self.relative_lines.append(line)
    
    def destroy(self):
        storyline_util.OnDeleteNode(self.node_id)

class Line(object):
    def __init__(self, start_node, end_node):
        self.id = common_util.genId("Line")
        self.start_node = start_node
        self.end_node = end_node

        self.start_pos = None
        self.end_pos = None
        self.k = 1
        self.b = 0
        self.tri_first = None
        self.tri_second = None
        self.resetPos()
    
    def getDistancePointFromPoint(self, org_pos, k, dist):
        x, y = org_pos
        if k is None:
            return ((x, y - dist), (x, y + dist))
        elif k == 0:
            return ((x - dist, y), (x + dist, y))
        else:
            alpha = dist / math.sqrt(k ** 2 + 1)
            return ((x - alpha, y - k * alpha), (x + alpha, y + k *alpha))

    def resetPos(self):
        start_node = self.start_node
        end_node = self.end_node

        vertical = abs(start_node.y - end_node.y) - (start_node.height + end_node.height) / 2
        horizontal = abs(start_node.x - end_node.x) - (start_node.width + end_node.width) / 2

        if vertical > horizontal:
            if start_node.y > end_node.y:
                start_y = start_node.y
                end_y = end_node.y + end_node.height
                start_x = start_node.x + start_node.width / 2
                end_x = end_node.x + end_node.width / 2
            else:
                start_y = start_node.y + start_node.height
                end_y = end_node.y
                start_x = start_node.x + start_node.width / 2
                end_x = end_node.x + end_node.width / 2
        else:
            if start_node.x > end_node.x:
                start_y = start_node.y + start_node.height / 2
                end_y = end_node.y + end_node.height / 2
                start_x = start_node.x
                end_x = end_node.x + end_node.width
            else:
                start_y = start_node.y + start_node.height / 2
                end_y = end_node.y + end_node.height / 2
                start_x = start_node.x + start_node.width
                end_x = end_node.x
                
        self.start_pos = (start_x, start_y)
        self.end_pos = (end_x, end_y)
        if end_x - start_x > 0.01:
            self.k = (end_y - start_y) / (end_x - start_x)
            self.b = (start_y * end_x - end_y * start_x) / (end_x - start_x)
        else:
            self.k = None
            self.b = None

        sqrt_3 = math.sqrt(3)
        if self.k is None:
            y_dis = 5 if end_y < start_y else -5
            self.tri_first = (end_x - 5 / sqrt_3, end_y + y_dis)
            self.tri_second = (end_x + 5 / sqrt_3, end_y + y_dis)
        elif self.k == 0:
            x_dis = 5 if end_x < start_y else -5
            self.tri_first = (end_x + x_dis, end_y - 5 / sqrt_3)
            self.tri_second = (end_x + x_dis, end_y + 5 / sqrt_3)
        else:
            temp_points = self.getDistancePointFromPoint(self.end_pos, self.k, 5.0)
            trans_point = temp_points[0] if self.k > 0 else temp_points[1]
            self.tri_first, self.tri_second = self.getDistancePointFromPoint(trans_point, -1 / self.k, 5.0 / sqrt_3)

    def checkClicked(self, x, y):
        expect_y = x * self.k + self.b
        if abs(y - expect_y) < 5:
            return True
    
    def drawLine(self, qp):
        self.resetPos()
        pen = QPen(Qt.black, 2, Qt.SolidLine)

        qp.setPen(pen)
        qp.drawLine(self.start_pos[0], self.start_pos[1],
                    self.end_pos[0], self.end_pos[1])
        qp.drawLine(self.end_pos[0], self.end_pos[1],
                    self.tri_first[0], self.tri_first[1])
        qp.drawLine(self.end_pos[0], self.end_pos[1],
                    self.tri_second[0], self.tri_second[1])

class TreeFrame(MyFrame):
    def __init__(self, widget=None, title=''):
        super(TreeFrame, self).__init__(widget, title)

        self.setAcceptDrops(True)

        self.mousePressEvent = self.onMousePress
        self.mouseMoveEvent = self.onMouseMove
        self.mouseReleaseEvent=self.onMouseRelease

        self.nodes_dict = {}
        self.line_dict = {}
        self.max_node_id = 0
        self.press_begin_pos = ()
        self.press_begin_node = None
        self.mouse_move_flag = False
        self.add_link_node = None

    def loadUINode(self):
        path = file_util.getUINodePath()
        try:
            f = open(path, 'r')
            content = f.read().strip('\n')
            f.close()
        except IOError:
            print "Read UI failed"
            return
        
        info = json.loads(content)
        for key, value in info.iteritems():
            node = Node(**value)
            self.nodes_dict[node.node_id] = node
        for node in self.nodes_dict.itervalues():
            nexts_ids = storyline_util.GetNextStoryNodeIds(node.node_id)
            for n_id in nexts_ids:
                node.next_node
                n_node = self.nodes_dict[n_id]
                line = Line(node, n_node)
                self.line_dict[line.id] = line
                node.relative_lines.append(line)
                n_node.relative_lines.append(line)
        self.update()

    def saveUINode(self):
        result = {}
        for node in self.nodes_dict.itervalues():
            result[node.node_id] = node.Pack()
        path = file_util.getUINodePath()
        try:
            f = open(path, 'w')
            f.write(json.dumps(result))
            f.close()
        except IOError:
            print "Save UI failed"
            print path
        return
    
    def clearUINode(self):
        self.nodes_dict = {}
        self.line_dict = {}
        self.max_node_id = 0
        self.press_begin_pos = ()
        self.press_begin_node = None
        self.mouse_move_flag = False
        self.add_link_node = None

    def onSectionChanged(self, old_id, new_id):
        if old_id and old_id != new_id:
            self.saveUINode()
        self.clearUINode()
        self.loadUINode()
    
    def onAddNode(self, tool_id, drop_pos):
        new_node = Node(tool_id, drop_pos[0], drop_pos[1])
        self.nodes_dict[new_node.node_id] = new_node
        self.max_node_id += 1
        self.saveUINode()

    def onDeleteNode(self, node):
        for line in self.relative_lines:
            self.onDeleteLine(line, from_node=node)
        self.nodes_dict.pop(node.node_id)
        node.destroy()
        self.saveUINode()

    def onAddLine(self, begin_node, end_node):
        begin_node.addNext(end_node)
        line = line = Line(begin_node, end_node)
        self.line_dict[line.id] = line
        begin_node.relative_lines.append(line)
        end_node.relative_lines.append(line)
        self.update()
    
    def onDeleteLine(self, line, from_node=None):
        if line.begin_node is not from_node:
            line.begin_node.cancelNext(line.end_node)
            line.begin_node.relative_lines.remove(line)
        if line.end_node is not from_node:
            line.end_node.relative_lines.remove(line)
        self.line_dict.pop(line.id)
        self.update()

    def eventForNode(self, node, e):
        menu = QMenu(self)
        next_action = menu.addAction("Add Next")
        delete_action = menu.addAction("Delete")
        action = menu.exec_(self.mapToGlobal(e.pos()))
        if action == next_action:
            self.add_link_node = node
        elif action == delete_action:
            self.onDeleteNode(node)
    
    def eventForLine(self, line):
        menu = QMenu(self)
        delete_action = menu.addAction("Delete")
        action = menu.exec_(self.mapToGlobal(e.pos()))
        if action == delete_action:
            self.onDeleteLine(line)

    def contextMenuEvent(self, e):
        x = e.pos().x()
        y = e.pos().y()
        for node in self.nodes_dict.itervalues():
            if node.checkClicked(x, y):
                self.eventForNode(node, e)
                return
        for line in self.line_dict.itervalues():
            if line.checkClicked(x, y):
                self.eventForLine(line, e)
                return

    def onMousePress(self, e):
        x = e.pos().x()
        y = e.pos().y()
        self.press_begin_pos = (x, y)
        for node in self.nodes_dict.itervalues():
            if node.checkClicked(x, y):
                if self.add_link_node:
                    self.onAddLine(self.add_link_node, node)
                    self.add_link_node = None
                    return
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
        cur_section = cur_story.category.cur_section
        if not cur_story.id or not cur_section or cur_section.id == 'root':
            print "IN??"
            return
        tool_id = int(e.mimeData().text())
        drop_pos = (e.pos().x(), e.pos().y())
        if tool_id in tools:
            print "Node??"
            self.onAddNode(tool_id, drop_pos)
        self.update()

    def paintEvent(self, e):
        super(TreeFrame, self).paintEvent(e)
        qp = QPainter()
        qp.begin(self)
        for node in self.nodes_dict.itervalues():
            node.drawNode(qp)
        for line in self.line_dict.itervalues():
            line.drawLine(qp)
        qp.end()


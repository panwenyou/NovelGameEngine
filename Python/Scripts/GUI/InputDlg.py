#-*- coding:utf-8 -*-


import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from utils import common_util


class InputDlg(QWidget):
	def __init__(self,  parent=None):
		super(InputDlg, self).__init__(parent)
		self.data_dict = {}
		self.call_back = None

		self.v_layout = QVBoxLayout()
		self.setLayout(self.v_layout)

	def buildInput(self, data_list, call_back):
		self.data_dict = {}
		for key in data_list:
			l = QHBoxLayout()
			label = QLabel(key)
			text_edit = QLineEdit('')
			l.addWidget(label)
			l.addWidget(text_edit)
			self.v_layout.addLayout(l)
			self.data_dict[key] = {'widget': text_edit}
		l = QHBoxLayout()
		yes_btn = QPushButton("确定")
		yes_btn.clicked.connect(self.Confirm)
		cancel_btn = QPushButton("取消")
		cancel_btn.clicked.connect(self.Cancel)
		l.addStretch(1)
		l.addWidget(yes_btn)
		l.addWidget(cancel_btn)
		l.addStretch(1)
		self.v_layout.addLayout(l)
		self.call_back = call_back

	def Confirm(self):
		self.call_back(self.data_dict)

	def Cancel(self):
		return

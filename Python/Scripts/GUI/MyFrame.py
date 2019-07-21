#-*- coding:utf-8 -*-


import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from utils import file_utils


class MyFrame(QFrame):
	def __init__(self, widget=None, title=''):
		super(MyFrame, self).__init__(widget)

		self.root_panel = QVBoxLayout()
		# 标题
		self.title = QLabel(title)

		self.root_panel.addWidget(self.title)
		self.initUI()
		self.setLayout(self.root_panel)

	def initUI(self):
		self.root_panel.addStretch(1)

	def onRefreshUI(self):
		pass

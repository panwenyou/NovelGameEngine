#-*- coding:utf-8 -*-

import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget

print sys.path

from GUI.CentralWindow import CentralWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CentralWindow()
    sys.exit(app.exec_())
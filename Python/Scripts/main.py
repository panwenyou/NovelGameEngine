#-*- coding:utf-8 -*-

import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget

print sys.path

from GUI.CentralWindow import CentralWindow

from utils.model import Story


__builtins__.cur_story = Story()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CentralWindow()
    __builtins__.cur_wnd = ex
    sys.exit(app.exec_())
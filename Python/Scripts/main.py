#-*- coding:utf-8 -*-

import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget

print sys.path

from GUI.CentralWindow import CentralWindow
from GUI.InputDlg import InputDlg

from utils.model import Story


__builtins__.cur_story = Story()

debug_dict = {}

def cb(data_dict):
    global debug_dict
    code = data_dict['code']['widget'].text()
    print "input:", code
    exec(code)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CentralWindow()
    __builtins__.cur_wnd = ex

    debug_dlg = InputDlg()
    debug_dlg.setGeometry(500, 100, 400, 100)
    debug_dlg.buildInput((("code", u'代码'),), cb)
    debug_dlg.show()

    sys.exit(app.exec_())
#-*- coding:utf-8 -*-

import os

root_dir_name = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def getImageFilePath(file_name):
    return ''.join((root_dir_name, '\\res\\' ,file_name))

def getStoryFileRoot():
	return ''.join((root_dir_name, '\\stories'))

def getTemplatePath(file_name):
    return ''.join((root_dir_name, '\\res\\template\\', file_name))

print getImageFilePath('exit.jpg')
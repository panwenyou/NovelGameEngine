#-*- coding:utf-8 -*-

import os

root_dir_name = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def getImageFilePath(file_name):
    return ''.join((root_dir_name, '\\res\\' ,file_name))

def getStoryFileRoot():
	return ''.join((root_dir_name, '\\stories'))

def getTemplatePath(file_name):
    return ''.join((root_dir_name, '\\res\\template\\', file_name))

def getUINodePath():
    story_id = cur_story.id
    section_id = cur_story.category.cur_section.id
    root_path = getStoryFileRoot()
    return ''.join((root_path, '\\', story_id, '\\', section_id, '\\ui.json'))

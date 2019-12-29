#-*- coding:utf-8 -*-

import file_util
import os
import json
import common_util


def AddSection(parent_key, name):
    return cur_story.category.AddSection(parent_key, name)


def DeleteSection(section_key):
    cur_story.category.deleteSection(section_key)


def RenameSection(section_key, name):
    cur_story.category.renameSection(section_key, name)


def OnSectionChanged(section_key):
    cur_story.category.ChangeCurSection(section_key)


def SaveCategory():
    cur_story.category.SaveCategory()


def GetRootSection():
    return cur_story.category.section_dict['root']
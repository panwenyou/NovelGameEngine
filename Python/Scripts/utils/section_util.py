#-*- coding:utf-8 -*-

import file_util
import os
import json
import common_util


from PyQt5.QtCore import Qt, QMimeData, QRect, pyqtSlot, QTimer


cur_category = {}
cur_section = ''


class Category(object):
    def __init__(self, story_name):
        self.category_dict = {}
        self.category_quick_dict = {}
        self.story_name = story_name
        self.save_timer = None

    def addSection(self, parent_key, name):
        key = common_util.genId('section')
        # 是根目录下的章节
        if not parent_key or parent_key not in self.category_quick_dict:
            section = {'name': name, 'parent_key': None}
            self.category_dict[key] = section
            self.category_quick_dict[key] = section
        # 是已有章节中的子章节
        else:
            parent_section = self.category_quick_dict[parent_key]
            section = {'name': name, 'parent_key': parent_key}
            # 作为子章节加入
            if 'sub' not in parent_section:
                parent_section['sub'] = {}
            parent_section['sub'][key] = section
            # 添加到快速索引中
            self.category_quick_dict[key] = section
        return key

    def deleteSection(self, key):
        # 通过快速字典找到对象
        section = self.category_quick_dict.get(key)
        if not section:
            return
        # 从父节点删除
        parent_key = section.get('parent_key')
        if parent_key:
            print self.category_quick_dict
            parent = self.category_quick_dict[parent_key]
            parent['sub'].pop(key)
        # 从快速字典删除
        self.category_quick_dict.pop(key)

    def renameSection(self, key, name):
        # 通过快速字典找到对象
        section = self.category_quick_dict.get(key)
        if not section:
            return
        section['name'] = name

    def load(self):
        self.loadCategory()
        self.loadQuickDict()

    def buildQuickDict(self, cate_dict):
        for key, value in cate_dict.iteritems():
            self.category_quick_dict[key] = value
            sub = value.get('sub')
            sub and self.buildQuickDict(sub)

    def loadQuickDict(self):
        # QuickDict的设计思路是用于快速检索到需要的对象，从而避免在catedict里面去递归寻找
        # 用一次递归节省后面的多次递归
        self.category_quick_dict = {}
        self.buildQuickDict(self.category_dict)

    def loadCategory(self):
        # 尝试去读目录结构，如果没有，则新建一个目录结构json file
        root_path = file_util.getStoryFileRoot()
        cat_file_path = ''.join((root_path, '\\', self.story_name, '\\category.json'))
        print 'cat_file_path:', cat_file_path
        if os.path.exists(cat_file_path):
            try:
                f = open(cat_file_path, 'r')
                catetory = json.loads(f.read().strip('\n'))
                self.category_dict = catetory
            except IOError:
                # 重试
                print ''.join(('read file error:', cat_file_path))
                return
        else:
            try:
                f = open(cat_file_path, 'w+')
                f.write('{}')
                catetory = {}
                self.category_dict = catetory
            except IOError:
                # 重试
                print ''.join(('read file error:', cat_file_path))
                return
        f.close()

    def save(self):
        self.saveCategory()

    def saveCategory(self):
        root_path = file_util.getStoryFileRoot()
        cat_file_path = ''.join((root_path, '\\', self.story_name, '\\category.json'))
        try:
            f = open(cat_file_path, 'w')
            catetory_string = json.dumps(self.category_dict)
            f.write(catetory_string)
            f.close()
        except IOError:
            # 重试
            print ''.join(('read file error:', cat_file_path))
            save_timer = QTimer()
            save_timer.timeout.connect(saveCategory)
        return


def loadCategory(story_name):
    global cur_category
    cur_category = Category(story_name)
    cur_category.load()


def addSection(parent_key, name):
    global cur_category
    if cur_category:
        cur_category.addSection(parent_key, name)
        cur_category.save()


def deleteSection(section_key):
    global cur_category
    if cur_category:
        cur_category.deleteSection(section_key)
        cur_category.save()


def renameSection(section_key, name):
    global cur_category
    if cur_category:
        cur_category.renameSection(section_key, name)
        cur_category.save()


def saveCategory():
    global cur_category
    cur_category and cur_category.save()
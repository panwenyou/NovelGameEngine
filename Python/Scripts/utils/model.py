#-*- coding:utf-8 -*-

from utils import file_util, common_util, data_util, section_util
from data import consts, tools_data
import os
import json
import shutil


class StoryNode(object):
    def __init__(self, story_id, section_id):
        self.story_id = story_id
        self.section_id = section_id
        self.id = 0
        self.name = ''
        self.n_type = ''
        self.nexts = []
    
    def LoadFromDict(self, dic):
        self.id = dic.get("id", 0)
        self.name = dic.get("name", '')
        self.n_type = dic.get("n_type", '')
    
    def Pack(self):
        ret_dict = {"id": self.id, 'name':self.name, 'n_type': self.n_type, 'nexts':list()}
        for sn in self.nexts:
            ret_dict['nexts'].append(sn.id)
        return ret_dict
    
    def Link(self, node_list):
        self.nexts = node_list
    
    def NewLink(self, node):
        if node not in self.nexts:
            self.nexts.append(node)
    
    def DropLink(self, node):
        if node in self.nexts:
            self.nexts.remove(node)
    
    def GenScript(self):
        root_path = file_util.getStoryFileRoot()
        script_path = ''.join((root_path, '\\', self.story_id, '\\', self.section_id, '\\', self.id, '.stln'))
        template_path = file_util.getTemplatePath(consts.TEMPLATES[self.n_type])
        template_file = open(template_path, 'r')
        script_file = open(script_path, 'w')
        script_file.write(template_file.read())
        script_file.close()
        template_file.close()


class StoryLine(object):
    def __init__(self, story_id, section_id):
        self.story_line_dict = {}
        self.story_id = story_id
        self.section_id = section_id
    
    def LoadStoryLine(self):
        root_path = file_util.getStoryFileRoot()
        sl_file_path = ''.join((root_path, '\\', self.story_id, '\\', self.section_id, '\\', 'storyline.json'))
        if os.path.exists(sl_file_path):
            # {id:{id, name, []}, id:{id, name, []}}
            f = open(sl_file_path, 'r')
            story_content_dict = json.loads(f.read().strip('\n'))
            self.GenNodes(story_content_dict)
            f.close()
        else:
            f = open(sl_file_path, 'w')
            f.write(json.dumps(self.story_line_dict))
            f.close()
            story_content_dict = {}
    
    def GenNodes(self, node_dict):
        for key, value in node_dict.iteritems():
            sn = StoryNode(self.story_id, self.section_id)
            sn.LoadFromDict(value)
            self.story_line_dict[key] = sn
        for sn in self.story_line_dict.itervalues():
            link_node_list = []
            nexts_list = node_dict[sn.id]['nexts']
            for n_id in nexts_list:
                link_node_list.append(self.story_line_dict[n_id])
            sn.Link(link_node_list)

    def SaveStoryLine(self):
        pack_dict = {}
        for key, value in self.story_line_dict.iteritems():
            pack_dict[key] = value.Pack()
        root_path = file_util.getStoryFileRoot()
        sl_file_path = ''.join((root_path, '\\', self.story_id, '\\', self.section_id, '\\', 'storyline.json'))
        f = open(sl_file_path, 'w')
        f.write(json.dumps(pack_dict))
        f.close()
    
    def AddNode(self, name, n_type):
        new_id = common_util.genId("StoryNode")
        new_node = StoryNode(self.story_id, self.section_id)
        new_node.LoadFromDict({'id': new_id, "name": name, "n_type": n_type})
        new_node.GenScript()
        self.story_line_dict[new_id] = new_node
        self.SaveStoryLine()
        return new_id
    
    def DeleteNode(self, node_id):
        if node_id in self.story_line_dict:
            old = self.story_line_dict.pop(node_id)
            for node in self.story_line_dict.itervalues():
                if old in node.nexts:
                    node.nexts.remove(old)

    def BuildLink(self, node_id1, node_id2):
        node1 = self.story_line_dict[node_id1]
        node2 = self.story_line_dict[node_id2]
        node1.NewLink(node2)
    
    def BreakLink(self, node_id1, node_id2):
        node1 = self.story_line_dict[node_id1]
        node2 = self.story_line_dict[node_id2]
        node1.DropLink(node2)


class Section(object):
    def __init__(self, story_id, idx):
        self.story_id = story_id
        self.idx = idx
        self.id = 0
        self.name = ''
        self.parent = None
        self.story_line = None
        self.sub_sections = {}
    
    def LoadSection(self, dic):
        self.id = dic.get("id", 0)
        self.name = dic.get("name", '')
        
        root_path = file_util.getStoryFileRoot()
        dir_path = ''.join((root_path, '\\', self.story_id, '\\', self.id))
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        self.story_line = StoryLine(self.story_id, self.id)
        self.story_line.LoadStoryLine()
    
    def Link(self, sub_sections):
        self.sub_sections = sub_sections
    
    def AddSubSection(self, section):
        self.sub_sections[section.id] = section
    
    def LinkParent(self, parent):
        self.parent = parent
    
    def Pack(self):
        pack_dict = {
            "id": self.id,
            "name": self.name,
            "parent_id": self.parent.id if self.parent else None,
            "sub_sections": list()
            }
        for sub in self.sub_sections.itervalues():
            pack_dict['sub_sections'].append(sub.id)
        return pack_dict
    
    def SaveStoryLine(self):
        if self.id != 'root':
            self.story_line.SaveStoryLine()


class Category(object):
    def __init__(self, story_id):
        self.section_dict = {}
        self.story_id = story_id
        self.save_timer = None
        self.max_idx = 0
        self.cur_section = None

    def AddSection(self, parent_key, name):
        self.max_idx += 1
        section = Section(self.story_id, self.max_idx)
        new_id = common_util.genId("Section")
        section.LoadSection({"id": new_id, "name": name})
        self.section_dict[new_id] = section
        # 是已有章节中的子章节
        if parent_key and parent_key in self.section_dict:
            parent_section = self.section_dict[parent_key]
        else:
            parent_section = self.section_dict["root"]
        parent_section.AddSubSection(section)
        section.LinkParent(parent_section)
        self.SaveCategory()
        return new_id

    def DeleteSection(self, key):
        section = self.section_dict.get(key)
        if not section:
            return
        # 从父节点删除
        parent = section.parent
        if parent:
            parent = parent.sub_sections.pop(section.id)
        # 删除所有子节点
        for sub_id in section.sub_sections.iterkeys():
            self.deleteSection(sub_id)
        
        self.section_dict.pop(key)

    def RenameSection(self, key, name):
        section = self.section_dict.get(key)
        if not section:
            return
        section.name = name

    def GenSections(self, content):
        if not content:
            section = Section(self.story_id, self.max_idx)
            section.name = cur_story.name
            section.id = "root"
            self.section_dict["root"] = section
            self.SaveCategory()
            return
        
        for key, value in content.iteritems():
            section = Section(self.story_id, self.max_idx)
            section.LoadSection(value)
            self.section_dict[key] = section
        
        for section in self.section_dict.itervalues():
            subs_ids = content[section.id]['sub_sections']
            sub_dict = {}
            for sub_id in subs_ids:
                sub_section = self.section_dict[sub_id]
                sub_dict[sub_id] = sub_section
            section.Link(sub_dict)
            parent_id = content[section.id]['parent_id']
            if parent_id:
                section.LinkParent(self.section_dict[parent_id])

    def LoadCategory(self):
        # {id: {id, name, parent_id, sub_sections}}
        # 尝试去读目录结构，如果没有，则新建一个目录结构json file
        root_path = file_util.getStoryFileRoot()
        cat_file_path = ''.join((root_path, '\\', self.story_id, '\\category.json'))
        print 'category_file_path:', cat_file_path
        if os.path.exists(cat_file_path):
            try:
                f = open(cat_file_path, 'r')
                content = json.loads(f.read().strip('\n'))
            except IOError:
                # 重试
                print ''.join(('read file error:', cat_file_path))
                return
        else:
            try:
                f = open(cat_file_path, 'w+')
                content = {"max_idx": 0, "sections": dict()}
                f.write(json.dumps(content))
            except IOError:
                # 重试
                print ''.join(('read file error:', cat_file_path))
                return
        f.close()
        self.max_idx = content.get('max_idx', 0)
        self.GenSections(content['sections'])

    def Pack(self):
        ret = {"max_idx": self.max_idx, "sections": dict()}
        for section in self.section_dict.itervalues():
            print section
            print self.section_dict
            ret['sections'][section.id] = section.Pack()
        return ret

    def SaveCategory(self):
        root_path = file_util.getStoryFileRoot()
        cat_file_path = ''.join((root_path, '\\', self.story_id, '\\category.json'))
        try:
            f = open(cat_file_path, 'w')
            catetory_string = json.dumps(self.Pack())
            f.write(catetory_string)
            f.close()
        except IOError:
            # 重试
            print ''.join(('read file error:', cat_file_path))
        for section in self.section_dict.itervalues():
            section.SaveStoryLine()
        return
    
    def ChangeCurSection(self, section_key):
        print "!!!!!!!!!!"
        print section_key
        print self.section_dict
        self.cur_section = self.section_dict.get(section_key)


class Story(object):
    def __init__(self):
        self.category = None
        self.id = 0
        self.name = ''
        self.stories_dict = {}
        self.Init()

    def Init(self):
        stories_root = file_util.getStoryFileRoot()

        # 读故事列表json
        try:
            meta = open(''.join((stories_root, "\\stories.json")), "r")
        except:
            print 'read failed: ', ''.join((stories_root, "\\stories.json"))
            return False

        content = meta.read().strip('\n')
        if content:
            self.stories_dict = json.loads(content)
        else:
            self.stories_dict = {}
        meta.close()
    
    def HasStory(self, story_id):
        return story_id in self.stories_dict

    def SaveStory(self):
        if self.category:
            self.category.SaveCategory()
    
    def NewStory(self, name):
        self.SaveStory()
        story_id = common_util.genId("Story")
        self.id = story_id
        self.name = name
        self.stories_dict[story_id] = name
        result = json.dumps(self.stories_dict)
        stories_root = file_util.getStoryFileRoot()
        cur_path = ''.join((stories_root, "\\", story_id))
        os.mkdir(cur_path)

        # 创建新的目录数据
        self.category = Category(self.id)
        self.category.LoadCategory()

        try:
            meta = open(''.join((stories_root, "\\stories.json")), "w")
            meta.write(result)
            meta.close()
        except:
            print 'write failed: ', ''.join((stories_root, "\\stories.json"))
            return False

        return True
    
    def LoadStory(self, story_id):
        if story_id not in self.stories_dict:
            return False
        self.SaveStory()
        self.id = story_id
        self.name = self.stories_dict[story_id]

        # 创建新的目录数据
        self.category = Category(self.id)
        self.category.LoadCategory()

        return True
    
    def DeleteStory(self, story_id):
        if story_id in self.stories_dict:
            self.stories_dict.pop(story_id)
            stories_root = file_util.getStoryFileRoot()
            shutil.rmtree(''.join((stories_root, "\\", story_id)))

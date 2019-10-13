#-*- coding:utf-8 -*-

from utils import file_util, common_util, data_util, section_util
from data import consts, tools_data
import os
import json


cur_story_data = {}

templates = {
		'SequenceNode': 'sequence.txt',
		'BranchNode': 'branck.txt',
		'EventNode': 'event.txt',
		'DialogNode': 'dialog.txt',
		'JumpNode': 'jump.txt',
	}


def OnSectionChanged(section_id):
	# 根据section_id去找到对应的故事线
	global cur_story_data
	story_root = file_util.getStoryFileRoot()
	story_file = ''.join((story_root, '\\', section_id))
	f = open(story_file, 'r')
	cur_story_data = json.loads(f.read().strip('\n'))
	f.close()


def OnAddNode(node_id):
	global cur_story_data, templates
	tool = tools_data.tools.get(node_id)
	node_name = tool['node_name']
	sid = common_util.genId(node_name)
	
	cur_story_data[sid] = {
		'name': tool['name'],
		'type': node_name,
		'para': {'file': ''}, 
		'next_node_ids': list(),
	}
	
	# 创建模板
	section_id = section_util.cur_section
	template = templates.get(node_name)
	f = open(file_util.getTemplatePath(template), 'r')
	story_root = file_util.getStoryFileRoot()
	story_file = ''.join((story_root, '\\', section_id, '\\', node_id, '.story'))
	f2 = open(story_file, 'w')
	f2.write(f.read())
	f.close()
	f2.close()
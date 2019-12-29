#-*- coding:utf-8 -*-

from utils import file_util, common_util, data_util, section_util
from data import consts, tools_data
import os
import json


def OnAddNode(type_id):
	default_name = "未命名"
	return cur_story.category.cur_section.story_line.AddNode(default_name, type_id)


def OnDeleteNode(node_id):
	cur_story.category.cur_section.story_line.DeleteNode(node_id)


def OnAddNext(node_id, next_node_id):
	cur_story.category.cur_section.story_line.BuildLink(node_id, next_node_id)


def OnCancelNext(node_id, next_node_id):
	cur_story.category.cur_section.story_line.BreakLink(node_id, next_node_id)


def OnChangeStoryNodeName(node_id, name):
	cur_story.category.cur_section.story_line.story_line_dict[node_id].name = name
	cur_story.SaveStory()


def GetStoryLine():
	return cur_story.category.cur_section.story_line


def GetNextStoryNodeIds(node_id):
	ret = []
	cur_node = cur_story.category.cur_section.story_line.story_line_dict[node_id]
	for node in cur_node.nexts:
		ret.append(node.id)
	return ret


def GetStoryNode(node_id):
	return cur_story.category.cur_section.story_line.story_line_dict[node_id]


def GetStoryNodeName(node_id):
	print "####"
	print type(cur_story.category.cur_section.story_line.story_line_dict[node_id].name)
	return cur_story.category.cur_section.story_line.story_line_dict[node_id].name


def GetStoryNodeTypeName(node_id):
	n_type = cur_story.category.cur_section.story_line.story_line_dict[node_id].n_type
	return tools_data.tools[n_type]['name']

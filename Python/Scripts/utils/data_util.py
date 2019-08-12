#-*- coding:utf-8 -*-

import file_util
import os
import json
import section_util

cur_story = ''
story_path = ''

# {name1:0, name2:0}
stories_dict = {}



def getAllStroies():
	global stories_dict
	stories_root = file_util.getStoryFileRoot()
	try:
		f = open(''.join((stories_root, '\\stories.json')))
		stories_dict = json.loads(f.read().strip('\n'))
	except IOError:
		return False
	return True

def hasStory(name):
	return name in stories_dict

def openStory(path):
	global cur_story, cur_path

	# 先保存一记
	cur_story and section_util.saveCategory()

	cur_path = path
	cur_story = path.split('/')[-1]
	print cur_story
	print cur_path
	section_util.loadCategory(cur_story)

def newStory(name):
	global cur_story, cur_path
	# 先保存一记
	cur_story and ection_util.saveCategory()

	result = ''
	stories_root = file_util.getStoryFileRoot()

	# 读故事列表json
	try:
		meta = open(''.join((stories_root, "\\stories.json")), "r")
	except:
		print 'read failed: ', ''.join((stories_root, "\\stories.json"))
		return False

	content = meta.read().strip('\n')
	if content:
		stories_dict = json.loads(content)
		if name in stories_dict:
			return False
	else:
		stories_dict = {}
	# 目前来说，只要name就好了，0没有什么特别意义
	stories_dict[name] = 0
	result = json.dumps(stories_dict)
	meta.close()

	#  写Json
	if result:
		try:
			meta = open(''.join((stories_root, "\\stories.json")), "w")
			meta.write(result)
			meta.close()
		except:
			print 'write failed: ', ''.join((stories_root, "\\stories.json"))
			return False

		# 给故事创建一个跟故事名字一样的数据目录
		cur_path = ''.join((stories_root, "\\", name))
		cur_story = name
		os.mkdir(cur_path)

		# 创建新的目录数据
		section_util.loadCategory(cur_story)
		return True

	return False


#-*- coding:utf-8 -*-

import file_util
import os
import json

cur_story = ''
story_path = ''


def parseStory(content):
	pass

def openStory(path):
	pass

def newStory(name):
	result = ''
	stories_root = file_util.getStroyFileRoot()

	# 读json
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

		os.mkdir(''.join((stories_root, "\\", name)))
		cur_story = name

		return True

	return False


newStory('bbc')
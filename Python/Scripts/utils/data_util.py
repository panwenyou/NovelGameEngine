#-*- coding:utf-8 -*-

import file_util
import os
import json
import section_util
import common_util


def OpenStory(story_id):
	return cur_story.LoadStory(story_id)

def NewStory(name):
	return cur_story.NewStory(name)

def SaveStory():
	cur_story.SaveStory()


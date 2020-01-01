#-*- coding:utf-8 -*-

import time

property_frame = None
last_id = ''
id_count = 1

def genId(obj):
	global last_id
	global id_count
	new_id = ''.join((str(time.time()), str(obj)))
	if last_id == new_id:
		# 模仿uuid的方式，保证唯一性
		id_count += 1
	else:
		id_count = 1
	last_id = new_id
	return ''.join((new_id, str(id_count)))
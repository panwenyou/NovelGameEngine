#-*- coding:utf-8 -*-

import time

property_frame = None

def genId(obj):
	return ''.join((str(time.time()), str(obj)))
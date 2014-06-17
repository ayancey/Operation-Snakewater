# Snakewater Chrome Metric
# Copyright Meanberg Design 2014
# Version 1.0
import json
from pprint import pprint
import sys
import os

def execute():
	sys.stdout.write('Is Google Chrome installed? ')
	if os.path.exists(os.environ['LOCALAPPDATA'] + '/Google/Chrome/User Data/Default/Preferences'):
		print 'Yes'
	#data = json.loads(open('manifest.json', 'rb').read())
	#print data["name"]
	#print data["version"]
	#print str(data["content_scripts"][0]["all_frames"]) + ' suspicious'
	#for permissions in data["permissions"]:
	#print permissions

if __name__ == "__main__":
	execute()
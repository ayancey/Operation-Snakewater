# Snakewater Chrome Metric
# Copyright Meanberg Design 2014
# Version 1.0
import json
from pprint import pprint
import sys
import os
from colorama import init, Fore, Back, Style
init()

def scanextension(path):
	if len(os.listdir(path)) >= 1:
		if (os.path.isfile(path + '/' + os.listdir(path)[0] + '/manifest.json')):
			print 'Found manifest at: ' + Fore.YELLOW + path + '/' + os.listdir(path)[0] + '/manifest.json' + Fore.RESET
			data = json.loads(open(path + '/' + os.listdir(path)[0] + '/manifest.json', 'rb').read())
			print 'Extension name: ' + data["name"]
			print 'Extension version: ' + data["version"]
			#print str(data["content_scripts"][0]["all_frames"]) + ' suspicious'
			print 'Permissions required:'
			for permission in data["permissions"]:
				if permission == 'management':
					print Fore.RED + permission + Fore.RESET + ' - ' + Fore.YELLOW + ' This extension is allowed to manage other extensions.' + Fore.RESET
				elif permission == 'http://*/*':
					print Fore.RED + permission + Fore.RESET + ' - ' + Fore.YELLOW + ' This extension is allowed to match with ALL non-secure webpages.' + Fore.RESET
				else:
					print permission

				


def execute():
	sys.stdout.write('Is Google Chrome installed? ')
	if os.path.exists(os.environ['LOCALAPPDATA'] + '/Google/Chrome/User Data/Default/Preferences'):
		print 'Yes'
	scanextension('hiollpollmacojhigkifgnajhgnoiool')


if __name__ == "__main__":
	execute()
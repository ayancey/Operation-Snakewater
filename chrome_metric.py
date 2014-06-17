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
			print 'Extension name: ' + data["name"].encode("ascii", "ignore")
			print 'Extension version: ' + data["version"].encode("ascii", "ignore")
			#print str(data["content_scripts"][0]["all_frames"]) + ' suspicious'
			print 'Permissions required:'
			if 'permissions' in data:
				for permission in data["permissions"]:
					if permission == 'management':
						print Fore.RED + permission + Fore.RESET + ' - ' + Fore.YELLOW + ' This extension is allowed to manage other extensions.' + Fore.RESET
					elif permission == 'http://*/*':
						print Fore.RED + permission + Fore.RESET + ' - ' + Fore.YELLOW + ' This extension is allowed to match with ALL non-secure webpages.' + Fore.RESET
					elif permission == 'https://*/*':
						print Fore.RED + permission + Fore.RESET + ' - ' + Fore.YELLOW + ' This extension is allowed to match with ALL secure webpages.' + Fore.RESET
					elif permission == 'tabs':
						print Fore.RED + permission + Fore.RESET + ' - ' + Fore.YELLOW + ' This extension is allowed to manipulate tab information.' + Fore.RESET
					else:
						print permission
			if 'content_scripts' in data:
				print 'Content scripts parameters:'
				for csparams in data['content_scripts'][0]:
					if csparams == 'matches':
						for matches in data['content_scripts'][0]['matches']:
							if matches == 'http://*/*':
								print Fore.RED + matches + Fore.RESET + Fore.YELLOW + ' - This extension embeds Javascript code into every non-secure webpage.' + Fore.RESET
							elif matches == 'https://*/*':
								print Fore.RED + matches + Fore.RESET + Fore.YELLOW + ' - This extension embeds Javascript code into every secure webpage.' + Fore.RESET
				


def execute():
	sys.stdout.write('Is Google Chrome installed? ')
	if os.path.exists(os.environ['LOCALAPPDATA'] + '/Google/Chrome/User Data/Default/Preferences'):
		print 'Yes'
	for extensions in os.listdir(os.environ['LOCALAPPDATA'] + '/Google/Chrome/User Data/Default/Extensions'):
		scanextension(os.environ['LOCALAPPDATA'] + '/Google/Chrome/User Data/Default/Extensions/' + extensions)
	


if __name__ == "__main__":
	execute()
# Snakewater Chrome Metric
# Copyright Meanberg Design 2014
# Version 1.0
# Developed in part Ettlin AP CS Period 1

import json
from pprint import pprint
import sys
import os
from colorama import init, Fore, Back, Style
import pup
init()

def scanextension(path):
	base_suspicion = 50
	if len(os.listdir(path)) >= 1:
		if (os.path.isfile(path + '/' + os.listdir(path)[0] + '/manifest.json')):
			print 'Found manifest at: ' + Fore.YELLOW + path + '/' + os.listdir(path)[0] + '/manifest.json' + Fore.RESET
			data = json.loads(open(path + '/' + os.listdir(path)[0] + '/manifest.json', 'rb').read())
			extension_name = get_extension_name_from_locale(path + '/' + os.listdir(path)[0] + '/manifest.json')
			print 'Extension name: ' + extension_name
			print 'Extension version: ' + data["version"].encode("ascii", "ignore")
			#print str(data["content_scripts"][0]["all_frames"]) + ' suspicious'
			print 'Permissions required:'
			if 'permissions' in data:
				for permission in data["permissions"]:
					if permission == 'management':
						print Fore.RED + permission + Fore.RESET + ' - ' + Fore.YELLOW + ' This extension is allowed to manage other extensions.' + Fore.RESET
					elif permission == 'http://*/*':
						pup.add(extension_name + ' in Chrome can match ALL non-SSL pages', 70, 3, "Disable " + extension_name + ' Chrome extension', path)
						print Fore.RED + permission + Fore.RESET + ' - ' + Fore.YELLOW + ' This extension is allowed to match with ALL non-secure webpages.' + Fore.RESET
					elif permission == 'https://*/*':
						pup.add(extension_name + ' in Chrome can match ALL SSL pages', 80, 3, "Disable " + extension_name + ' Chrome extension', path)
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
								pup.add(extension_name + ' in Chrome can embed JS into ALL non-SSL pages', 70, 3, "Disable " + extension_name + ' Chrome extension', path)
								print Fore.RED + matches + Fore.RESET + Fore.YELLOW + ' - This extension embeds Javascript code into every non-secure webpage.' + Fore.RESET
							elif matches == 'https://*/*':
								pup.add(extension_name + ' in Chrome can embed JS into ALL SSL pages', 80, 3, "Disable " + extension_name + ' Chrome extension', path)
								print Fore.RED + matches + Fore.RESET + Fore.YELLOW + ' - This extension embeds Javascript code into every secure webpage.' + Fore.RESET

def get_extension_name_from_locale(manifest, locale = 'en'):
	if os.path.exists(manifest): 
		data = json.loads(open(manifest).read())
		if "__MSG_" in data["name"].encode("ascii","ignore"):
			mess_man = ''
			if os.path.exists(os.path.dirname(manifest) + '/_locales/en_US'):
				mess_man = os.path.dirname(manifest) + '/_locales/en_US/messages.json'
				print Fore.GREEN + 'locales detected (en_US)' + Fore.RESET
			elif os.path.exists(os.path.dirname(manifest) + '/_locales/en'):
				mess_man = os.path.dirname(manifest) +  '/_locales/en/messages.json'
				print Fore.GREEN + 'locales detected (en)' + Fore.RESET
			else:
				return data["name"].encode("ascii","ignore")

			print mess_man
			if os.path.isfile(mess_man):
				moredata = json.loads(open(mess_man).read())
				if data["name"].encode("ascii", "ignore").replace("__MSG_","").replace("__","") in moredata:
					return moredata[data["name"].encode("ascii", "ignore").replace("__MSG_","").replace("__","")]['message']
				elif data["name"].encode("ascii", "ignore").replace("__MSG_","").replace("__","").lower() in moredata:
					return moredata[data["name"].encode("ascii", "ignore").replace("__MSG_","").replace("__","").lower()]['message']
				else:
					return data["name"].encode("ascii","ignore")
				#print moredata[data["name"].encode("ascii", "ignore").replace("__MSG_","").replace("__","")]
				#print moredata['app_name'] 
			else:
				return data["name"].encode("ascii","ignore")
		else:
			return data["name"].encode("ascii","ignore")

def execute():
	sys.stdout.write('Is Google Chrome installed? ')
	if os.path.exists(os.environ['LOCALAPPDATA'] + '/Google/Chrome/User Data/Default/Preferences'):
		print 'Yes'
	else:
		print 'No'
		exit()
	for extensions in os.listdir(os.environ['LOCALAPPDATA'] + '/Google/Chrome/User Data/Default/Extensions'):
		if not extensions == 'desktop.ini':
			scanextension(os.environ['LOCALAPPDATA'] + '/Google/Chrome/User Data/Default/Extensions/' + extensions)
	
if __name__ == "__main__":
	execute()
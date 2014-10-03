# Snakewater Chrome Metric
# Copyright Meanberg Design 2014
# Version 1.0
# Developed in part Ettlin AP CS Period 1


# To-do:
	# Modify suspicion based on:
		# Presence of key?
	# Add more comments

import json
from pprint import pprint
import sys
import os
from colorama import init, Fore, Back, Style
import pup
init()

all_extensions = []

# Scan path for extension (manifest file exists)
def scanextension(path):
	if len(os.listdir(path)) >= 1:
		# Extension exists
		if (os.path.isfile(path + '/' + os.listdir(path)[0] + '/manifest.json')):
			print 'Found manifest at: ' + Fore.YELLOW + path + '/' + os.listdir(path)[0] + '/manifest.json' + Fore.RESET
			data = json.loads(open(path + '/' + os.listdir(path)[0] + '/manifest.json', 'rb').read())
			extension_name = get_extension_name_from_locale(path + '/' + os.listdir(path)[0] + '/manifest.json')
			# List for name, version, location, suspicion level
			this_extension = [extension_name, data["version"].encode("ascii", "ignore"), path + '/' + os.listdir(path)[0] + '/manifest.json', 50, []]

			# This might be a little shitty, but let's see how it works out
			if extension_name == 'Google Slides':
				# Lower suspicion if it's a default Google extension
				this_extension[3] -= 15
			elif extension_name == 'Google Docs':
				this_extension[3] -= 15
			elif extension_name == 'Google Drive':
				this_extension[3] -= 15
			elif extension_name == 'Google Voice Search Hotword (Beta)':
				this_extension[3] -= 15
			elif extension_name == 'YouTube':
				this_extension[3] -= 15
			elif extension_name == 'Google Search':
				this_extension[3] -= 15
			elif extension_name == 'Google Sheets':
				this_extension[3] -= 15
			elif extension_name == 'Google Wallet':
				this_extension[3] -= 15
			elif extension_name == 'Gmail':
				this_extension[3] -= 15

			# This could totally work
			if "icons" in data:
				#print 'icons exist'
				this_extension[3] -= (len(data["icons"]) * 15)
				#print 

			print 'Extension name: ' + Fore.MAGENTA + extension_name + Fore.RESET
			print 'Extension version: ' + data["version"].encode("ascii", "ignore")
			print 'Permissions required:'
			if 'permissions' in data:
				for permission in data["permissions"]:
					# Dodgy permissions
					if permission == 'management':
						print Fore.RED + permission + Fore.RESET + ' - ' + Fore.YELLOW + ' This extension is allowed to manage other extensions.' + Fore.RESET
					elif permission == 'http://*/*':
						# Add 10 suspicion points
						this_extension[3] += 10
						this_extension[4].append('match-page')
						#pup.add(extension_name + ' in Chrome can match ALL non-SSL pages', 70, 3, "Disable " + extension_name + ' Chrome extension', path)
						print Fore.RED + permission + Fore.RESET + ' - ' + Fore.YELLOW + ' This extension is allowed to match with ALL non-secure webpages.' + Fore.RESET
					elif permission == 'https://*/*':
						this_extension[3] += 10
						this_extension[4].append('match-SSLpage')
						#pup.add(extension_name + ' in Chrome can match ALL SSL pages', 80, 3, "Disable " + extension_name + ' Chrome extension', path)
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
							# Downright suspicious
							if matches == 'http://*/*':
								# :\
								this_extension[3] += 15
								this_extension[4].append('js-match-page')
								#pup.add(extension_name + ' in Chrome can embed JS into ALL non-SSL pages', 70, 3, "Disable " + extension_name + ' Chrome extension', path)
								print Fore.RED + matches + Fore.RESET + Fore.YELLOW + ' - This extension embeds Javascript code into every non-secure webpage.' + Fore.RESET
							elif matches == 'https://*/*':
								this_extension[3] += 15
								this_extension[4].append('js-match-SSLpage')
								#pup.add(extension_name + ' in Chrome can embed JS into ALL SSL pages', 80, 3, "Disable " + extension_name + ' Chrome extension', path)
								print Fore.RED + matches + Fore.RESET + Fore.YELLOW + ' - This extension embeds Javascript code into every secure webpage.' + Fore.RESET

			# Still extension exists
			if 'match-page' in this_extension[4]:
				pup.add(extension_name + ' in Chrome can match ALL non-SSL pages', 2, this_extension[3], extension_name + ' could be pulling something.', path)

			if 'match-SSLpage' in this_extension[4]:
				pup.add(extension_name + ' in Chrome can match ALL SSL pages', 2, this_extension[3], extension_name + ' could be pulling something.', path)

			if 'js-match-page' in this_extension[4]:
				pup.add(extension_name + ' in Chrome can embed JS into ALL non-SSL pages', 2, this_extension[3], extension_name + ' could be pulling something.', path)

			if 'js-match-SSLpage' in this_extension[4]:
				pup.add(extension_name + ' in Chrome can embed JS into ALL SSL pages', 2, this_extension[3], extension_name + ' could be pulling something.', path)

# Pulls the extension name from the locale file, relative to the manifest file (default_locale, en_us, en, respectively)
def get_extension_name_from_locale(manifest):
	if os.path.exists(manifest): 
		data = json.loads(open(manifest).read())
		# Manifest references locales
		if "__MSG_" in data["name"].encode("ascii","ignore"):

			mess_man = ''
			# Check if default_locale is a thing
			if not data["default_locale"].encode("ascii","ignore") =='':
				# Default locale in manifest exists in locales folder
				if os.path.exists(os.path.dirname(manifest) + '/_locales/' + data["default_locale"].encode("ascii","ignore")):
					mess_man = os.path.dirname(manifest) + '/_locales/' + data["default_locale"].encode("ascii","ignore") + '/messages.json'
					print Fore.GREEN + 'locales detected (' + data["default_locale"].encode("ascii","ignore") + ') [default locale]' + Fore.RESET
			else:
				if os.path.exists(os.path.dirname(manifest) + '/_locales/en_US'):
					# en_US locale exists
					mess_man = os.path.dirname(manifest) + '/_locales/en_US/messages.json'
					print Fore.GREEN + 'locales detected (en_US)' + Fore.RESET
				elif os.path.exists(os.path.dirname(manifest) + '/_locales/en'):
					# en locale exists (good enough)
					mess_man = os.path.dirname(manifest) +  '/_locales/en/messages.json'
					print Fore.GREEN + 'locales detected (en)' + Fore.RESET
				else:
					# Fuck it, use defaule name (even though it is something ugly like __MSG_appName)
					return data["name"].encode("ascii","ignore")

			if os.path.isfile(mess_man):
				moredata = json.loads(open(mess_man).read())
				# Sometimes the manifest uses uppercase, and the json is lowercase :/
				if data["name"].encode("ascii", "ignore").replace("__MSG_","").replace("__","") in moredata:
					return moredata[data["name"].encode("ascii", "ignore").replace("__MSG_","").replace("__","")]['message']
				elif data["name"].encode("ascii", "ignore").replace("__MSG_","").replace("__","").lower() in moredata:
					return moredata[data["name"].encode("ascii", "ignore").replace("__MSG_","").replace("__","").lower()]['message']
				else:
					return data["name"].encode("ascii","ignore")

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
		# This should not be a thing.
		if not extensions == 'desktop.ini':
			scanextension(os.environ['LOCALAPPDATA'] + '/Google/Chrome/User Data/Default/Extensions/' + extensions)
	
if __name__ == "__main__":
	execute()
# Snakewater Executioner
# Alex Yancey
# Version 1.0
# Developed in part Ettlin AP CS Period 1

import sys
print 'Loading netstat_metric'
import netstat_metric
print 'Loading registry_metric'
import registry_metric
print 'Loading chrome_metric'
import chrome_metric
print 'Loading startup_metric'
import startup_metric
print 'Loading pup'
from colorama import init, Fore, Back, Style
import pup
import os
init()

os.system('cls' if os.name == 'nt' else 'clear')

print 'Snakewater Executioner v1.0'
sys.stdout.write("Press any key to begin...")
raw_input()

chrome_metric.execute()
registry_metric.execute()
netstat_metric.execute()
startup_metric.execute()

print str(len(pup.pups)) + ' possible potentially unwanted programs'

for thepup in pup.pups:
	print Fore.RED + str(thepup[0]) + Fore.RESET + ' (' + str(thepup[1]) + ') ' + str(thepup[2]) + '% ' + str(thepup[3])
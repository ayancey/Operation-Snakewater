# Snakewater Netstat Metric
# Alex Yancey
# Version 1.0
# Developed in part Ettlin AP CS Period 1

import sys
import csv
import psutil
from colorama import init, Fore, Back, Style
import pup
init()

def status(s):
    sys.stdout.write(s + " " * (78 - len(s)) + "\r")

def execute():	
	counter = 0
	ip_list = [];

	print 'Loading malicious IP list.'

	with open('mdl.csv', 'rb') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
			for row in spamreader:
				counter += 1
				status(str(counter) + ' loaded')
				try:
					if not row[2].replace('"','') == '127.0.0.1':
						ip_list.insert(0,(row[2].replace('"',''),row[4].replace('"','')))
				except:
					pass
			
	print 'Scanning open connections for maliciousness...'

	for con in psutil.net_connections():
		try:
			if con.raddr[0] == '127.0.0.1':
				continue
			if con.raddr[0] == '192.168.1.1':
				continue
			sys.stdout.write(con.raddr[0] + ' is ')
			try:
				badip = [i for i, v in enumerate(ip_list) if v[0] == con.raddr[0]]
			 	pup.add('Malicious IP connection on ' + con.raddr[0] + ' (' + ip_list[badip[0]][1] + ')', 2, 60)
				print Fore.RED + 'malicious. ' + Fore.YELLOW + ip_list[badip[0]][1] + Fore.RESET
				#print ' not malicious'
			except:
				print Fore.GREEN + 'not malicious' + Fore.RESET + '.'
		except:
			continue

if __name__ == "__main__":
	execute()
# Snakewater Registry Metric
# Copyright Meanberg Design 2014
# Version 1.0
# Developed in part Ettlin AP CS Period 1

import sys
import winreg_unicode
import platform
from colorama import init, Fore, Back, Style
import pup
init()

def regkey_value(path, name="", start_key = None):
    if isinstance(path, str):
        path = path.split("\\")
    if start_key is None:
        start_key = getattr(winreg_unicode, path[0])
        return regkey_value(path[1:], name, start_key)
    else:
        subkey = path.pop(0)
    with winreg_unicode.OpenKey(start_key, subkey) as handle:
        assert handle
        if path:
            return regkey_value(path, name, handle)
        else:
            desc, i = None, 0
            while not desc or desc[0] != name:
                desc = winreg_unicode.EnumValue(handle, i)
                i += 1
            return desc[1]

#----------------------------------------------------------------------------------------------------------------------------

def execute():

	#Get username to ensure registry access is working
	try: 
		username = regkey_value("HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\ComputerName\ComputerName", "ComputerName")
		print 'Your username is ' + username + ' (registry check)...' + Fore.GREEN + 'Good' + Fore.RESET
	except:
		print 'Registry check...' + Fore.RED + 'Bad' + Fore.RESET
		sys.exit(0)
		
	#----------------------------------------------------------------------------------------------------------------------------
	#Make sure user is running Windows
	
	sys.stdout.write('You are currently running ' + platform.platform() + ' with Python ' + sys.version.split(' ')[0] + '...')
	if platform.system() == 'Windows':
		print(Fore.GREEN + 'Good' + Fore.RESET)
	else:
		pup.add('Not running Windows', 0, 0)
		print(Fore.RED + 'Bad' + Fore.RESET)
		sys.exit(0)
		
	if platform.release() == 'XP':
		pup.add('Running Windows XP', 1, 30, 'It is recommend that you update to a newer version of Windows to continue receiving security updates.')
		print(Fore.RED + "Windows XP is insecure and diagristic techniques will be limited." + Fore.RESET)
	
	#----------------------------------------------------------------------------------------------------------------------------
	#Check for taskmgr accessibility
	try:
		if( regkey_value("HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System", "DisableTaskMgr") ):
			pup.add('Task Manager disabled', 1, 40, "If you or your sysadmin did not do this, it could be cause for suspicion.",None,'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System\DisableTaskMgr')
			print 'Task Manager access is currently ' + Fore.RED + 'DISABLED' + Fore.RESET + '.'
		else:
			print 'Task Manager access is currently ' + Fore.GREEN + 'ENABLED' + Fore.RESET + '.'
	except WindowsError:
		print 'Task Manager access is currently ' + Fore.GREEN + 'UNSET' + Fore.RESET + '.'
		
	#----------------------------------------------------------------------------------------------------------------------------
	#Check for LAN Proxy

	proxy = regkey_value("HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings", "ProxyEnable")
	proxy_host = 'nothing'
	if proxy:
		try:
			proxy_host = regkey_value("HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings", "ProxyServer")
		except:
			pass
		if '127.0.0.1' in proxy_host:
			pup.add('LAN proxy enabled on loopback', 2, 80, "There's a good chance this is a bad thing.",None,'HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings\ProxyServer')
			print 'Your LAN proxy is currently ' + Fore.RED + 'ON LOOPBACK' + Fore.RESET + ' and set to ' + Fore.RED + proxy_host + Fore.RESET + '.' + Fore.YELLOW + ' This is not good.' + Fore.RESET
		else:
			pup.add('LAN proxy enabled', 1, 40, "If you or your sysadmin did not do this, it could be cause for suspicion.",None,'HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings\ProxyServer')
			print 'Your LAN proxy is currently ' + Fore.RED + 'ON' + Fore.RESET + ' and set to ' + Fore.RED + proxy_host + Fore.RESET + '.' + Fore.YELLOW + ' If you did not set this, this can be a sign of adware or malware meant to intercept your internet connection.' + Fore.RESET

	else:
		print 'Your LAN proxy is currently ' + Fore.GREEN + 'OFF' + Fore.RESET + '.'

if __name__ == "__main__":
	execute()
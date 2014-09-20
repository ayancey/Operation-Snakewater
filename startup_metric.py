# Snakewater Startup Metric
# Copyright Alex Yancey & Meanberg Design 2014
# Version 1.0
# Developed in Ettlin AP CS Period 1

import winreg_unicode
import ctypes
import os

import sys
import win32com.client 

# Old function from registry_metric, don't remember if I stole this or not
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

# Reads registry and determines if system is 64-bit or not
def is64bit():
	architecture = regkey_value('HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 'PROCESSOR_ARCHITECTURE')
	if 'x86' in architecture:
		return False
	else:
		return True

# Found a really weird nuance in the registry. More here: http://windowsitpro.com/systems-management/whats-wow6432node-under-hkeylocalmachinesoftware-registry-subkey

## Checking if 64-bit or not (see above link)
if is64bit():
	print 'System is 64-bit, reflecting Wow6432Node.'

print '=== HKLM ==='
thekey = winreg_unicode.OpenKey(winreg_unicode.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Run')
#wkey = winreg_unicode.EnumKey(thekey,0)

for i in range(1024):
    try:
    	print str(winreg_unicode.EnumValue(thekey, i)[0])
    except WindowsError:
    	break

print '=== HKCU ==='

thekey = winreg_unicode.OpenKey(winreg_unicode.HKEY_CURRENT_USER,'SOFTWARE\Microsoft\Windows\CurrentVersion\Run')

for i in range(1024):
    try:
    	print winreg_unicode.EnumValue(thekey, i)[0]
    except WindowsError:
    	break


print '=== STARTUP ==='

for files in os.listdir('C:\Users\Alex\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'):
    if not files == 'desktop.ini':
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut("C:\Users\Alex\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\\" + files)
        print(shortcut.Targetpath)
        #print files

print '=== STARTUP_EXEC ==='

for files in os.listdir('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp'):
    print files

#wkey = winreg_unicode.EnumKey(thekey,0)

# C:\Users\Alex\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup

# C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp

#print winreg_unicode.EnumValue(thekey,0)
#print regkey_value("HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\ComputerName\ComputerName", "ComputerName")
#print regkey_value("HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run","AdobeAAMUpdater-1.0")
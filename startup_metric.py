# Snakewater Startup Metric
# Copyright Alex Yancey & Meanberg Design 2014
# Version 1.0
# Developed in Ettlin AP CS Period 1

import winreg_unicode
import ctypes
import os

import sys
import win32com.client 
import win32api
from colorama import init, Fore, Back, Style
init()



# Old function from registry_metric, definitely stole this
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

# Win32Api voodoo that I totally stole from SO
def getFileProperties(fname):
    """
    Read all properties of the given file return them as a dictionary.
    """
    propNames = ('Comments', 'InternalName', 'ProductName',
        'CompanyName', 'LegalCopyright', 'ProductVersion',
        'FileDescription', 'LegalTrademarks', 'PrivateBuild',
        'FileVersion', 'OriginalFilename', 'SpecialBuild')

    props = {'FixedFileInfo': None, 'StringFileInfo': None, 'FileVersion': None}

    try:
        # backslash as parm returns dictionary of numeric info corresponding to VS_FIXEDFILEINFO struc
        fixedInfo = win32api.GetFileVersionInfo(fname, '\\')
        props['FixedFileInfo'] = fixedInfo
        props['FileVersion'] = "%d.%d.%d.%d" % (fixedInfo['FileVersionMS'] / 65536,
                fixedInfo['FileVersionMS'] % 65536, fixedInfo['FileVersionLS'] / 65536,
                fixedInfo['FileVersionLS'] % 65536)

        # \VarFileInfo\Translation returns list of available (language, codepage)
        # pairs that can be used to retreive string info. We are using only the first pair.
        lang, codepage = win32api.GetFileVersionInfo(fname, '\\VarFileInfo\\Translation')[0]

        # any other must be of the form \StringfileInfo\%04X%04X\parm_name, middle
        # two are language/codepage pair returned from above

        strInfo = {}
        for propName in propNames:
            strInfoPath = u'\\StringFileInfo\\%04X%04X\\%s' % (lang, codepage, propName)
            ## print str_info
            strInfo[propName] = win32api.GetFileVersionInfo(fname, strInfoPath)

        props['StringFileInfo'] = strInfo
    except:
        pass

    return props

# Reads registry and determines if system is 64-bit or not
def is64bit():
	architecture = regkey_value('HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 'PROCESSOR_ARCHITECTURE')
	if 'x86' in architecture:  
		return False
	else:
		return True

# Uses multiple (two) methods to find a reasonable name for the executable
def Get_Reliable_Name(path):
    if not getFileProperties(path)['StringFileInfo'] == None:
        if not getFileProperties(path)['StringFileInfo']['FileDescription'] == None:
            return getFileProperties(path)['StringFileInfo']['FileDescription'].encode('ascii','ignore')
            #print 'u'
        else:
            return os.path.basename(path)
    else:
        return os.path.basename(path)

# For use in registry keys where full file path is provided in CLI form with quotes and appended parameters
def Strip_Quotes_and_Params(fullpath):
    if fullpath.count('"') == 2:
        return fullpath.split('"')[1]
    else:
        if fullpath == "":
            print Fore.RED + "I forgot what I did but if this happens it shouldn't." + Fore.RESET
        if fullpath.count(".exe") == 1:
            return fullpath.replace(fullpath.split('.exe')[1],"").strip()

# Found a really weird nuance in the registry. More here: http://windowsitpro.com/systems-management/whats-wow6432node-under-hkeylocalmachinesoftware-registry-subkey
# Even crazier shit, https://mail.python.org/pipermail/python-win32/2009-June/009263.html this didn't help
# Wow64 Filesystem Redirection needs to fuck off


## Checking if 64-bit or not (see above link)
if is64bit():
	print 'System is 64-bit, reflecting Wow6432Node.'

print '=== HKLM ==='
thekey = winreg_unicode.OpenKey(winreg_unicode.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Run')
#wkey = winreg_unicode.EnumKey(thekey,0)

for i in range(1024):
    try:
        if not str(winreg_unicode.EnumValue(thekey, i)[1]) == '':
            print Get_Reliable_Name(Strip_Quotes_and_Params(str(winreg_unicode.EnumValue(thekey, i)[1])))
    except WindowsError:
    	break

print '=== HKCU ==='

thekey = winreg_unicode.OpenKey(winreg_unicode.HKEY_CURRENT_USER,'SOFTWARE\Microsoft\Windows\CurrentVersion\Run')

for i in range(1024):
    try:
        if not str(winreg_unicode.EnumValue(thekey, i)[1]) == '':
            print Get_Reliable_Name(Strip_Quotes_and_Params(str(winreg_unicode.EnumValue(thekey, i)[1])))
    except WindowsError:
    	break


print '=== STARTUP ==='

for files in os.listdir('C:\Users\Alex\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'):
    if not files == 'desktop.ini':
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut("C:\Users\Alex\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\\" + files)
        the_real_path = shortcut.Targetpath

        if not os.path.exists(the_real_path):
            if not os.path.exists(the_real_path.replace("Program Files (x86)", "Program Files")):
                print "Shortcut path doesn't exist"
            else:
                print Fore.RED + 'Unreflected shortcut path exists...Wow6432Node bullshit' + Fore.RESET
                the_real_path = the_real_path.replace("Program Files (x86)", "Program Files")

        print Get_Reliable_Name(the_real_path)

        #.get('FileVersion','None?')
        #print files


print '=== STARTUP_EXEC ==='

for files in os.listdir('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp'):
    if not files == 'desktop.ini':
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut("C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\\" + files)
        print Get_Reliable_Name(shortcut.Targetpath)
        #print files

#wkey = winreg_unicode.EnumKey(thekey,0)

# C:\Users\Alex\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup

# C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp

#print winreg_unicode.EnumValue(thekey,0)
#print regkey_value("HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\ComputerName\ComputerName", "ComputerName")
#print regkey_value("HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run","AdobeAAMUpdater-1.0")
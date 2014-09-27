# Snakewater Startup Metric
# Copyright Alex Yancey & Meanberg Design 2014
# Version 1.0
# Developed in Ettlin AP CS Period 1

import ctypes
import os

import sys
import win32com.client 
import win32api
from colorama import init, Fore, Back, Style
init()
import _winreg


# Old function from registry_metric, definitely stole this
def regkey_value(path, name="", start_key = None):
    if isinstance(path, str):
        path = path.split("\\")
    if start_key is None:
        start_key = getattr(_winreg, path[0])
        return regkey_value(path[1:], name, start_key)
    else:
        subkey = path.pop(0)
    with _winreg.OpenKey(start_key, subkey) as handle:
        assert handle
        if path:
            return regkey_value(path, name, handle)
        else:
            desc, i = None, 0
            while not desc or desc[0] != name:
                desc = _winreg.EnumValue(handle, i)
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

# Uses multiple (three ) methods to find a reasonable name for the executable
def Get_Reliable_Name(path):
    if not getFileProperties(path)['StringFileInfo'] == None:
        if not getFileProperties(path)['StringFileInfo']['FileDescription'] == None:
            return Fore.GREEN + getFileProperties(path)['StringFileInfo']['FileDescription'].encode('ascii','ignore') + Fore.RESET
            #print 'u'
        else:
            if not getFileProperties(path)['StringFileInfo']['ProductName'] == None:
                return Fore.BLUE + getFileProperties(path)['StringFileInfo']['ProductName'].encode('ascii','ignore') + Fore.RESET
            else:
                return Fore.RED + os.path.basename(path) + Fore.RESET
    else:
        return Fore.RED + os.path.basename(path) + Fore.RESET

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

def execute():
    ## Checking if 64-bit or not (see above link)
    if is64bit():
    	print 'System is 64-bit, bypassing Wow6432Node with KEY_WOW64_64KEY flag.'

    if is64bit():
        print '=== HKLM 32-bit ==='
    else:
        print '=== HKLM ==='

    thekey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Run')

    for i in range(1024):
        try:
            if not str(_winreg.EnumValue(thekey, i)[1]) == '':
                print Get_Reliable_Name(Strip_Quotes_and_Params(str(_winreg.EnumValue(thekey, i)[1])))
        except WindowsError:
        	break

    if is64bit():
        print '=== HKLM 64-bit ==='
        thekey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Run',0,_winreg.KEY_READ | _winreg.KEY_WOW64_64KEY)
        for i in range(1024):
            try:
                if not str(_winreg.EnumValue(thekey, i)[1]) == '':
                    print Get_Reliable_Name(Strip_Quotes_and_Params(str(_winreg.EnumValue(thekey, i)[1])))
            except WindowsError:
                break


    print '=== HKCU ==='

    thekey = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,'SOFTWARE\Microsoft\Windows\CurrentVersion\Run')

    for i in range(1024):
        try:
            if not str(_winreg.EnumValue(thekey, i)[1]) == '':
                print Get_Reliable_Name(Strip_Quotes_and_Params(str(_winreg.EnumValue(thekey, i)[1])))
        except WindowsError:
            break


    print '=== STARTUP ==='

    try:
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
    except WindowsError:
        print ':/'


    print '=== STARTUP_EXEC ==='

    try:
        for files in os.listdir('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp'):
            if not files == 'desktop.ini':
                shell = win32com.client.Dispatch("WScript.Shell")
                shortcut = shell.CreateShortCut("C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\\" + files)
                print Get_Reliable_Name(shortcut.Targetpath)
                #print files
    except WindowsError:
        print ':/'

if __name__ == "__main__":
    execute()
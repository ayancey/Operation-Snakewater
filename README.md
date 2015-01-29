# Operation Snakewater #

Snakewater was a project I worked on in late 2014. The idea and design philosophy is that the main penetration for potentially unwanted programs (PUP) lies within poorly made adware that can easily be detected based on a few, key characteristics. Some (but not all) of these common characteristics are:

* Utilizing the global proxy settings (Internet Options > Connections > LAN options)
* Really silly assembly names
* Using stupid and obvious persistence methods

### Dependencies ###

* Python 2.7
* [winreg_unicode](https://pypi.python.org/pypi/winreg_unicode)
* [colorama](https://pypi.python.org/pypi/colorama)
* [psutil](https://github.com/giampaolo/psutil)
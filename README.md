# Operation Snakewater #

Snakewater is a brave attempt at *sufficient* heuristic security against malware for Windows users.

### Objectives ###

* Fast
* Non-intrusive
* Samples that require updating should be *kept to a minimum*
* High detection rate (end goal of 90+%) for our specified victim configurations

### Dependencies/How to Compile ###

* Install Python **2.7**
* [winreg_unicode](https://pypi.python.org/pypi/winreg_unicode) is currently required for the [registry metric](https://bitbucket.org/meanbergdesign/operation-snakewater/src/2da4203c97f638ee052d98e8ae3c3df8d530b28a/registry_metric.py?at=master)
* [colorama](https://pypi.python.org/pypi/colorama) is currently required
* [psutil](https://github.com/giampaolo/psutil) is currently required for the [netstat metric](https://bitbucket.org/meanbergdesign/operation-snakewater/src/2da4203c97f638ee052d98e8ae3c3df8d530b28a/netstat_metric.py?at=master)




### Contribution guidelines ###

* Be smart
* Don't fuck it up
* When in doubt, branch out
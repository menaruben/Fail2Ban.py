# Fail2Ban.py
This project is about my own implementation of a Fail2Ban (SSH) service for Windows 10+. 

## Flowchart / Functionality
![](./imgs/fail2ban-flowchart.jpg)

# 1. Checklist / To-Do
- [x] bans IP addresses based on the amount of failed logins and timespan for a defined duration (tested)
- [x] unbans IP adresses after checking the "age" or CreationTime of the firewall rule
- [x] runs as a windows service
- [x] add better logging
- [x] store firewall rules and unban date to sshjail table (Fail2Ban db using sqlite3) so that the SSHJail is saved even after restarting/stopping the script/service
- [x] installer
- [ ] improve performance (instead of getting FileContetDiff every x seconds use a "tail -f"-like function to print out new lines and use counter dictionary with FirstOccurranceDate)

# Known bugs/errors as of right now
None :)

# 3 Dependencies
- python (of course)
- Module: asyncio (used for asynchronous functions)
- Module: re (used for splitting an array into fields)
- Module: difflib (used for getting the difference between the previous and the current sshlogs)
- Module: datetime (self explanatory)
- Module: wget (installer)
- Module: requests (installer)
- Commandline tool: [NSSM - the Non-Sucking Service manager](https://nssm.cc/download) (used for creating a service for our python script)

## sshd_config
In order to have the sshd.log file the service needs you have to configure sshd. This is automated when using the installer.The ```sshd_config``` file is inside ```%programdata%\ssh`` and should look like this::
```
# Logging
SyslogFacility LOCAL0
LogLevel Debug3
```
Now save and restart the OpenSSH Server with the following PowerShell command:
```
net stop sshd
net start sshd
```

# 4 Documentation
## automated installation with [installer.py](installer.py)
The installer is used to configure the ```sshd.log``` file, installing [NSSM - the Non-Sucking Service manager](https://nssm.cc/download) and creating the windows service. Just clone or download the repository and run:
```
python .\installer.py
```
```
# Output
The OpenSSH SSH Server service was stopped successfully.

The OpenSSH SSH Server service is starting.
The OpenSSH SSH Server service was started successfully.

100% [............................................................................] 351793 / 351793Service "Fail2Ban" installed successfully!
You can now start the Fail2Ban service!
----------- installer is finished -----------
```

If  no errors occurred you can open the services panel with ```Windows Key > Services```. Press F to jump to the Services that start with the letter F. There should now be a Service called "Fail2Ban". To start it you can rightclick and click on Start. 

## uninstalling Fail2Ban Service
Currently there is no uninstaller but if you really want to uninstall the Service make sure to stop the service and open a terminal. Now go to the folder containing the ```nssm-24.4\win64\nssm.exe``` and type the following command:
```
nssm.exe remove "Fail2Ban"
```
If no errors occured the output should say ```Service "Fail2Ban" removed successfully!```. After uninstalling the service you will be able to delete the repository from you disk (Fail2Ban.log file stays inside ```%programdata%\ssh```). 
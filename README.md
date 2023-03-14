# Fail2Ban.py
This project is about my own implementation of a Fail2Ban (SSH) service for Windows 10+. 

## Flowchart / Functionality
![](./imgs/fcfail2ban.png)

# 1. Checklist / To-Do
- [x] bans IP addresses based on the amount of failed logins and timespan for a defined duration (tested)
- [x] unbans IP adresses after checking the "age" or CreationTime of the firewall rule
- [x] runs as a windows service
- [x] add better logging
- [x] store firewall rules and unban date to sshjail table (Fail2Ban db using sqlite3) so that the SSHJail is saved even after restarting/stopping the script/service
- [x] installer
- [ ] full documentation for manual and automated installation/configuration with screenshots

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
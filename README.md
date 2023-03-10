# Fail2Ban.py
This project is about my own implementation of a Fail2Ban (SSH) service for Windows 10+. 

## Flowchart / Functionality
![](./imgs/fcfail2ban.png)

# 1. Checklist / To-Do
- [x] bans IP addresses based on the amount of failed logins and timespan for a defined duration (tested)
- [x] unbans IP adresses after checking the "age" or CreationTime of the firewall rule
- [ ] runs as a windows service without any problem
- [ ] add better logging for script
- [x] store firewall rules and unban date to sshjail table (Fail2Ban db using sqlite3) so that the SSHJail is saved even after restarting/stopping the script/service
- [ ] installer (automate the creation of service)
- [ ] full documentation for manual and automated installation/configuration with screenshots

# 2 Known bugs/errors as of right now
- Fail2Ban.py isn't able to start as a service.
    - I am currently working on fixing this issue but for now I'm prioritizing the functionality of the script overall. I will fully focus on fixing this issue after making it run as expected.

- Fail2Ban.py stops after banning the first IP-address.
    - This probably occurs because I have been trying to save the FreeDate (which is a datetime) and save it to an xml file without converting it to a string beforehand. I am currently working on this error.

# 3 Dependencies
- python (of course)
- Module: asyncio (used for asynchronous functions)
- Module: re (used for splitting an array into fields)
- Module: difflib (used for getting the difference between the previous and the current sshlogs)
- Module: datetime (self explanatory)
- Module: wget
- Commandline tool: [NSSM - the Non-Sucking Service manager](https://nssm.cc/download) (used for creating a service for our python script)

## sshd_config
In order to have the sshd.log file the service needs you have to configure sshd. In the future this job will be done via the installer but for now we'll have to configure it manually. Go to ```%programdata%\ssh``` and open the ```sshd_config``` file. Now change the Logging part to this:
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
... documentation for the PRECISE functionality is coming soon ...

## automated installation with [installer.py](installer.py)
Please do not use the installer as of now since a lot of things inside the Fail2Ban.py script changed. I will be updating the installer as soon as possible. 
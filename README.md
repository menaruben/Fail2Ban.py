# Fail2Ban.py
This project is about my own implementation of a Fail2Ban (SSH) service for Windows 10+. 

# Checklist / To-Do
- [x] it bans IP addresses based on the amount of failed logins and timespan for a defined duration (tested)
- [ ] it unbans IP adresses after checking the "age" or CreationTime of the firewall rule
- [ ] it runs as a windows service

# Known bugs as of right now
- None

# Dependencies
## Modules
- asyncio (used for asynchronous functions)
- re (used for splitting an array into fields)
- difflib (used for getting the difference between the previous and the current sshlogs)
- datetime (self explanatory)

Note: pywin32 will be needed in the near future in order to run the script as a windows service. 

# Function documentation
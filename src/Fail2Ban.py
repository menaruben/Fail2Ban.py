import asyncio              # async functions
from winfw import *         # used for adding and removing windows firewall rules
from FileHandling import *  # used for handling files, arrays, lines and so on
from TimeHandling import *  # used for handling time specific topics
from DataHandling import *  # used to add and remove data to sql
import logging              # used for logging
from os import path         # used for getting script path and checking paths for their existence
from sqlite3 import connect # used for sql database

TableName = "sshjail"       # name for sql table
DbName = "Fail2Ban.db"      # name for sql database file
conn = connect(f"{DbName}") # connecting to database
cur = conn.cursor()         # needed for executing sql queries later on

# define important variables
SSHLOGS = "C:/ProgramData/ssh/logs/sshd.log"        # path to sshd.log file
F2BLOGS = "C:/ProgramData/ssh/logs/Fail2Ban.log"    # path to Fail2Ban.log file (this service)

FailedLoginLimit = 3        # maximum amount of failed logins
FailedLoginTime = 15        # timespan in which these failed logins have to appear (seconds)
BanDuration = 25            # amount of time that host get banned for in seconds

script_path = path.dirname(path.abspath(__name__))  # gets path to THIS file

# Logging configuration
logging.basicConfig(filename=F2BLOGS,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    encoding='utf-8',
                    level=logging.DEBUG,
                    datefmt='%Y-%m-%d %H:%M:%S')

# GetFailedHosts returns all the FailedHosts inside the FailedLines and stores them inside of an array
def GetFailedHosts(FailedLines: list, MaxLogonAttemps: int) -> dict:
    FailedHosts = []                            # array in which FailedHosts (IP) are stored
    for line in FailedLines:
        fields = line.split(" ")                # splits line into fields at " "
        FailedHosts.append(fields[-4])          # parses out IP from sshd.log file

    FailedHosts_counts = {}                     # dictionary for storing amount of times these hosts have failed
    for FailedHost in set(FailedHosts):
        count = FailedHosts.count(FailedHost)   # counts amount of times the IP occurs inside the FailedHosts array
        FailedHosts_counts[FailedHost] = count  # stores amount of times per IP to dictionary

    for Host, count in FailedHosts_counts.items():
        if count < MaxLogonAttemps:                         # if amount of failed logins is smaller than MaxLogonAttempts-times then..
            FailedHosts = RemoveItem(FailedHosts, Host)     # remove it from FailedHosts array

    FailedHosts = RemoveDuplicates(FailedHosts) # remove duplicates from FailedHosts array
    return FailedHosts

async def main():
    f = open(F2BLOGS, "w")                          # checks if F2BLOGS path exists and if not then it creates the file
    f.close()                                       # close filestream
    CreateTableIfNotExists(conn)                    # creates the sshjail table if it doesnt already exist

    logging.info("Fail2Ban service started")
    PrevTimestamp = path.getmtime(SSHLOGS)          # store modification time of SSHLOGS
    PrevFileContent = ReadFile(SSHLOGS)             # store filecontent of SSHLOGS

    while True:
        try: 
            logging.debug("New While-True loop started")
            await asyncio.sleep(FailedLoginTime)        # repeats this function every FailedLoginTime seconds
            CurrentTimestamp = path.getmtime(SSHLOGS)   # store modification date of SSHLOGS

            if CurrentTimestamp != PrevTimestamp:       # compare previous modification time to current and if they differ then..
                PrevTimestamp = CurrentTimestamp        # the previous timestamp becomes the current timestamp

                CurrentFileContent = ReadFile(SSHLOGS)  # get current FileContent of SSHLOGS
                FileContentDiff = GetContentDiff(PrevFileContent, CurrentFileContent, SSHLOGS)  # gets difference between the previous and current content
                PrevFileContent = CurrentFileContent    # previous file content is now equal to the current file content

                FailedLines = GetFailedLines(FileContentDiff, "Failed password for")    # GetFailedLines  returns and stores all failed lines inside file difference to FailedLines array

                FailedHosts = GetFailedHosts(FailedLines, FailedLoginLimit)             # stores all failed hosts that exceeded the FailedLoginLimit to FailedHosts array

                # For-Loop iterates through FailedHosts array and bans all the hosts
                for host in FailedHosts:
                    BanIP(host)                                                 # bans host
                    logging.debug(f"{host} banned")
                    # SSHJail[host] = GetFreeDate(BanDuration)                  # get release date for host
                    WriteToSQL(conn, host, DateToStr(GetFreeDate(BanDuration)))       # store banned host their freedate to sql table

            CheckBanAge(conn, FailedLoginTime)                         # CheckBanAge unbans hosts if the FreeDate (release date) is less or equal to the current date
        
        except Exception as e:
            logging.debug(e)

if __name__ == "__main__":
    asyncio.run(main())
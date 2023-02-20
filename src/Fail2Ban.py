import asyncio
from winfw import *
from FileHandling import *
from TimeHandling import *
from XmlHandling import *
import logging
from os import path

SSHLOGS = "C:/ProgramData/ssh/logs/sshd.log"
F2BLOGS = "C:/ProgramData/ssh/logs/Fail2Ban.log"
FailedLoginLimit = 3
FailedLoginTime = 60        # seconds
BanDuration = 90         # seconds
script_path = path.dirname(path.abspath(__name__))
logging.basicConfig(filename=F2BLOGS,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    encoding='utf-8',
                    level=logging.DEBUG,
                    datefmt='%Y-%m-%d %H:%M:%S')

def GetFailedHosts(FailedLines: list, MaxLogonAttemps: int) -> dict:
    FailedHosts = []
    for line in FailedLines:
        fields = line.split(" ")
        FailedHosts.append(fields[-4])

    FailedHosts_counts = {}
    for FailedHost in set(FailedHosts):
        count = FailedHosts.count(FailedHost)
        FailedHosts_counts[FailedHost] = count

    for Host, count in FailedHosts_counts.items():
        if count < MaxLogonAttemps:
            FailedHosts = RemoveItem(FailedHosts, Host)

    FailedHosts = RemoveDuplicates(FailedHosts)
    return FailedHosts

def CheckBanAge(dict: dict):
    for host, FreeDate in dict.items():
        if FreeDate <= GetDate():
            UnbannedHost = Host(host)
            UnbannedHost.UnbanIP()
            del dict[host]
            RemoveFromXml(f'{script_path}\src\SSHJail.xml', "Host", "ip", host)
            logging.debug(f"{host} unbanned and removed from sshjail")

async def main():
    f = open(F2BLOGS, "w")
    f.close()

    logging.info("Fail2Ban service started")
    PrevTimestamp = path.getmtime(SSHLOGS)
    PrevFileContent = ReadFile(SSHLOGS)

    if path.exists('{script_path}\src\SSHJail.xml'):
        SSHJail = XmlToDict(f'{script_path}\src\SSHJail.xml')
    else:
        SSHJail = {}        # IP, FreeDate

    while True:
        logging.debug("New While-True loop started")
        await asyncio.sleep(FailedLoginTime)
        CurrentTimestamp = path.getmtime(SSHLOGS)

        if CurrentTimestamp != PrevTimestamp:
            PrevTimestamp = CurrentTimestamp

            CurrentFileContent = ReadFile(SSHLOGS)
            FileContentDiff = GetContentDiff(PrevFileContent, CurrentFileContent, SSHLOGS)
            PrevFileContent = CurrentFileContent

            FailedLines = GetFailedLines(FileContentDiff, "Failed password for")

            FailedHosts = GetFailedHosts(FailedLines, FailedLoginLimit)


            for host in FailedHosts:
                BannedHost = Host(host)
                BannedHost.BanIP()
                logging.debug(f"{host} banned")
                SSHJail[host] = GetFreeDate(BanDuration)

        CheckBanAge(SSHJail)
        DictToXml(SSHJail, f'{script_path}\src\SSHJail.xml')

if __name__ == "__main__":
    asyncio.run(main())
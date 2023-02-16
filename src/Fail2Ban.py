import asyncio
from winfw import *
from FileHandling import *
from TimeHandling import *
from XmlHandling import *
import logging
from os import path

SSHLOGS = "C:/ProgramData/ssh/logs/sshd.log"
FailedLoginLimit = 3
FailedLoginTime = 60        # seconds
BanDuration = 90         # seconds
script_path = path.dirname(path.abspath(__file__))
logging.basicConfig(filename='logs\Fail2Ban.log', encoding='utf-8', level=logging.DEBUG)

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
            logging.debug(f"{host} unbanned and removed from sshjail")

async def main():
    logging.info("Fail2Ban service started")
    PrevTimestamp = path.getmtime(SSHLOGS)
    PrevFileContent = ReadFile(SSHLOGS)

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

        DictToXml(SSHJail, f'{script_path}\SSHJail.xml')
        CheckBanAge(SSHJail)

if __name__ == "__main__":
    asyncio.run(main())
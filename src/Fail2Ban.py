import asyncio
from winfw import *
from FileHandling import *
from TimeHandling import *

SSHLOGS = "C:/ProgramData/ssh/logs/sshd.log"
FailedLoginLimit = 3
FailedLoginTime = 60        # seconds
BanDuration = 90         # seconds

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

async def main():
    PrevTimestamp = path.getmtime(SSHLOGS)
    PrevFileContent = ReadFile(SSHLOGS)

    SSHJail = {}        # IP, FreeDate

    while True:
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
                SSHJail[host] = GetFreeDate(BanDuration)

        CheckBanAge(SSHJail)

        # tested until here works just fine :)

if __name__ == "__main__":
    asyncio.run(main())
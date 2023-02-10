from os import path # used for getting file change timestamps and checking paths
from subprocess import run # run powershell code for firewalls
from TimeHandling import GetDate

RegistryPath = "HKLM:\SOFTWARE\Fail2Ban"

class Host:
    def __init__(self, IPaddr: str, RuleName):
        self.IPaddr = IPaddr
        self.RuleName = RuleName

# powershell New-NetFirewallRule -Name {RuleName} -DisplayName {RuleName} -Direction Outbound -LocalPort Any -Protocol TCP -Action Block -RemoteAddress {IPaddr}
    def BanIP(self):
        try:
            run(
                [
                    "powershell",
                    "New-NetFirewallRule",
                    "-Name", f"{self.RuleName}", "-DisplayName", f"{self.RuleName}",
                    "-Direction", "Outbound",
                    "-LocalPort", "Any",
                    "-Protocol", "TCP",
                    "-Action", "Block",
                    "-RemoteAddress", f"{self.IPaddr}"
                ]
            )

        except Exception as ExceptionMessage:
            print(f"There was a problem banning {self.IPaddr}: ")
            print(ExceptionMessage)


    def UnbanIP(self):
        try:
            run(
                [
                    "powershell", "Remove-NetFirewallRule", "-Name", f"{self.RuleName}"
                ]
            )

        except Exception as ExceptionMessage:
            print(f"There was a problem unbanning {self.IPaddr}: ")
            print(ExceptionMessage)
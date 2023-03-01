from os import path # used for getting file change timestamps and checking paths
from subprocess import run # run powershell code for firewalls
from TimeHandling import GetDate

# powershell New-NetFirewallRule -Name {RuleName} -DisplayName {RuleName} -Direction Outbound -LocalPort Any -Protocol TCP -Action Block -RemoteAddress {IPaddr}
def BanIP(IPaddr: str):
    try:
        run(
            [
                "powershell",
                "New-NetFirewallRule",
                "-Name", f"{IPaddr}", "-DisplayName", f"{IPaddr}",
                "-Direction", "Outbound",
                "-LocalPort", "Any",
                "-Protocol", "TCP",
                "-Action", "Block",
                "-RemoteAddress", f"{self.IPaddr}/24"
            ]
        )

    except Exception as ExceptionMessage:
        print(f"There was a problem banning {IPaddr}: ")
        print(ExceptionMessage)


def UnbanIP(IPaddr: str):
    try:
        run(
            [
                "powershell", "Remove-NetFirewallRule", "-Name", f"{IPaddr}"
            ]
        )

    except Exception as ExceptionMessage:
        print(f"There was a problem unbanning {IPaddr}: ")
        print(ExceptionMessage)
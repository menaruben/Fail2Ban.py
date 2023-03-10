from os import path # used for getting file change timestamps and checking paths
from subprocess import run # run powershell code for firewalls
from TimeHandling import GetDate
import logging              # used for logging

# todo: improve logging so that it's only used in Fail2Ban.py and not modules

F2BLOGS = "C:/ProgramData/ssh/logs/Fail2Ban.log"    # path to Fail2Ban.log file (this service)

logging.basicConfig(filename=F2BLOGS,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    encoding='utf-8',
                    level=logging.DEBUG,
                    datefmt='%Y-%m-%d %H:%M:%S')

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
                "-RemoteAddress", f"{IPaddr}/24"
            ]
        )

    except Exception as ExceptionMessage:
        logging.debug(f"There was a problem banning {IPaddr}: ")
        logging.debug(ExceptionMessage)


def UnbanIP(IPaddr: str):
    try:
        run(
            [
                "powershell", "Remove-NetFirewallRule", "-Name", f"{IPaddr}"
            ]
        )

    except Exception as ExceptionMessage:
        logging.debug(f"There was a problem unbanning {IPaddr}: ")
        logging.debug(ExceptionMessage)
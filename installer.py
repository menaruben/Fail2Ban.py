# install latest nssm, extract zip and create service
# ! PLEASE RUN INSTALLER FROM MAINPATH
import wget
import zipfile
from os import path
from subprocess import run
from sys import exec_prefix
import win32serviceutil

# ! PLEASE CHANGE MAINPATH TO YOUR ACTUAL PATH
mainpath = "C:\\repos\\Fail2Ban.py"

pathtomain = f"{mainpath}\\src\\Fail2Ban.py"
pythonpath = exec_prefix
ServiceName = "Fail2Ban2.py"
NssmName = "nssm-2.24"
DownloadNSSM = f"https://nssm.cc/release/{NssmName}.zip"

if path.exists(f"{mainpath}\\{NssmName}") == False:
    try:
        wget.download(DownloadNSSM)

    except Exception as e:
        print(e)
        print(f"Error downloading from {DownloadNSSM}")

    try:
        with zipfile.ZipFile(f"{NssmName}.zip", 'r') as zip_ref:
            zip_ref.extractall()
    except Exception as e:
        print(e)

try:
    run(
        [
            f"{NssmName}\\win64\\nssm.exe", "install", f"{ServiceName}",
            f"{pythonpath}", f"{pathtomain}"
        ]
    )

except Exception as e:
    print(e)
    print("Error creating service")
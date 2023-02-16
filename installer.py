# install latest nssm, extract zip, create service and run service
# ! YOU MUST RUN THE INSTALLER AS ADMINISTRATOR
import zipfile
from os import path, system, chdir
from subprocess import run
from sys import exec_prefix
try:
    import wget
except:
    system("pip install wget")
    import wget

mainpath = input("Please enter current working directory: ")

pathtomain = f"src\\Fail2Ban.py"
pythonpath = exec_prefix
ServiceName = "Fail2Ban.py"
NssmName = "nssm-2.24"
DownloadNSSM = f"https://nssm.cc/release/{NssmName}.zip"
nssm = f"{NssmName}\\win64\\nssm.exe"

chdir(mainpath)

if path.exists(f"{NssmName}") == False:
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
            f"{nssm}", "install", f"{ServiceName}",
            f"{pythonpath}", f"{pathtomain}"
        ]
    )

except Exception as e:
    print(e)
    print("Error creating service")

print(f"You can now start the {ServiceName} service!")
print("----------- installer is finished -----------")
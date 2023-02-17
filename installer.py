# install latest nssm, extract zip, create service and run service
# ! YOU MUST RUN THE INSTALLER AS ADMINISTRATOR
import zipfile
from os import path, system, chdir
from subprocess import run
from sys import exec_prefix
import fileinput
try:
    import wget
except:
    system("pip install wget")
    import wget

mainpath = path.dirname(path.abspath(__name__))
chdir(mainpath)

try:
    # Specify the filename and the lines to search and replace
    filename = "C:\\ProgramData\\ssh\\sshd_config"
    search_lines = ["#SyslogFacility AUTH", "#LogLevel INFO"]
    replace_lines = ["SyslogFacility = LOCAL0", "LogLevel = Debug3"]

    # Use the fileinput module to modify the lines in-place
    with fileinput.FileInput(filename, inplace=True, backup=".bak") as file:
        for line in file:
            if line.strip() in search_lines:
                index = search_lines.index(line.strip())
                line = replace_lines[index] + "\n"
            print(line, end="")
except Exception as e:
    print(e)
    print("Please configure sshd_config manually")

pathtomain = f"src\\Fail2Ban.py"
pythonpath = exec_prefix
ServiceName = "Fail2Ban.py"
NssmName = "nssm-2.24"
DownloadNSSM = f"https://nssm.cc/release/{NssmName}.zip"
nssm = f"{NssmName}\\win64\\nssm.exe"

if path.exists(f"{NssmName}") == False:
    try:
        wget.download(DownloadNSSM)

    except Exception as e:
        print(e)
        print(f"Error downloading from {DownloadNSSM}")
        exit()

    try:
        with zipfile.ZipFile(f"{NssmName}.zip", 'r') as zip_ref:
            zip_ref.extractall()
    except Exception as e:
        print(e)
        exit()

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
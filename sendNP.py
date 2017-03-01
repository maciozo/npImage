import pysftp
import getpass
import os
import time

filePath = "./image.png"
hostname = "maciozo.com"
port = 8564
user = "pi"
password = ""

def main(filePath, hostname, user, password, port):
    if password:
        print("Don't put your password in the source file, dumbass.")
    else:
        password = getpass.getpass("Password for %s@%s: " % (user, hostname))
    
    oldmt = os.path.getmtime(filePath)
    
    mainloop(oldmt, hostname, user, password, port)
    
def mainloop(oldmt, hostname, user, password, port):
    global filePath
    print("mainloop")
    while(1):
        mt = os.path.getmtime(filePath)
        # Check if modification time has changed
        if (mt != oldmt):
            print("newfile")
            sendFile(filePath, hostname, user, password, port)
            oldmt = mt
        time.sleep(10)
            
def sendFile(filePath, hostname, user, password, port):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    with pysftp.Connection(hostname, username=user, password=password, port=port, cnopts=cnopts) as sftp:
        sftp.chdir("/home/pi/scripts/npImage/")
        sftp.put(filePath)

main(filePath, hostname, user, password, port)

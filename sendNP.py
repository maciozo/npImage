import pysftp
import os
import time
import traceback
import json
import sys

try:
    import getpass
    has_getpass = True
except:
    has_getpass = False
    
config = {}
defaultConfig = """{
    "imgPath" : "./image.png",
    "textPath" : "./np.txt",
    "font" : "arial.ttf",
    "fontSize" : 15,
    "colourFormat" : "RGBA",
    "fontColour" : [0, 0, 0, 255],
    "backgroundColour" : [0, 0, 0, 0],
    "borderWidth" : 0,
    "scanInterval" : 10,
    "blankImageSize" : [1, 1],
    "blankImageColourFormat" : "RGBA",
    "blankImageBackground" : [0, 0, 0, 0],
    "blankImageText" : [""],
    "blankImageFont" : "arial.ttf",
    "blankImageFontSize" : 15,
    "blankImageFontColour" : [0, 0, 0, 255],
    "blankImageBorderWidth": 0,
    "hostname" : "example.org",
    "port" : 22,
    "username" : "username",
    "remoteDir" : ".",
    "SFTPscanInterval" : 10
}"""

def getConfig():
    global defaultConfig, config
    confFile = "./npImage.json"
    if not os.path.isfile(confFile):
        cf = open(confFile, "w", encoding = "utf-8")
        cf.write(defaultConfig)
        cf.close()
        print("Generated new config file (npImage.json)")
        sys.exit(0)
    cf = open(confFile, "r", encoding = "utf-8")
    config = json.loads(cf.read())
    checkConfig()
    cf.close()
    
def checkConfig():
    global config
    expectedTypes = {
                        "imgPath" : str,
                        "textPath" : str,
                        "font" : str,
                        "fontSize" : int,
                        "colourFormat" : str,
                        "fontColour" : list,
                        "backgroundColour" : list,
                        "borderWidth" : int,
                        "scanInterval" : int,
                        "blankImageSize" : list,
                        "blankImageColourFormat" : str,
                        "blankImageBackground" : list,
                        "blankImageText" : list,
                        "blankImageFont" : str,
                        "blankImageFontSize" : int,
                        "blankImageFontColour" : list,
                        "blankImageBorderWidth": int,
                        "hostname" : str,
                        "port" : int,
                        "username" : str,
                        "remoteDir" : str,
                        "SFTPscanInterval" : int
                    }
                    
    for option, expectedType in expectedTypes.items():
        try:
            if (type(config[option]) != expectedType):
                print("Invalid %s. Expected type %s, got %s." % (option, str(expectedType), str(type(config[option]))))
                sys.exit(1)
        except KeyError:
            print("Missing option: %s" % option)
            sys.exit(1)
            
    for channel in config["fontColour"]:
        if (type(channel) != int):
            print("Invalid fontColour value: %s. Expected type %s, got %s." % (str(channel), str(int), str(type(channel))))
            sys.exit(1)
            
    for channel in config["backgroundColour"]:
        if (type(channel) != int):
            print("Invalid backgroundColour value: %s. Expected type %s, got %s." % (str(channel), str(int), str(type(channel))))
            sys.exit(1)
            
    for channel in config["blankImageSize"]:
        if (type(channel) != int):
            print("Invalid blankImageSize value: %s. Expected type %s, got %s." % (str(channel), str(int), str(type(channel))))
            sys.exit(1)
            
    for channel in config["blankImageBackground"]:
        if (type(channel) != int):
            print("Invalid blankImageBackground value: %s. Expected type %s, got %s." % (str(channel), str(int), str(type(channel))))
            sys.exit(1)
            
    for channel in config["blankImageText"]:
        if (type(channel) != str):
            print("Invalid blankImageText value: %s. Expected type %s, got %s." % (str(channel), str(str), str(type(channel))))
            sys.exit(1)
            
    for channel in config["blankImageFontColour"]:
        if (type(channel) != int):
            print("Invalid blankImageFontColour value: %s. Expected type %s, got %s." % (str(channel), str(int), str(type(channel))))
            sys.exit(1)
    

def main():
    global config
    getConfig()
    if has_getpass:
        password = getpass.getpass("Password for %s@%s: " % (config["username"], config["hostname"]))
    else:
        password = input("Password for %s@%s (WILL BE VISIBLE - USE GETPASS): " % (config["username"], config["hostname"]))
            
    while (1):
        try:
            oldmt = os.path.getmtime(config["imgPath"])
            break
        except FileNotFoundError:
            print("Cannot find file: %s" % config["imgPath"])
            time.sleep(config["SFTPscanInterval"])
            
    
    sendFile(password)
    mainloop(oldmt, password)
    
def mainloop(oldmt, password):
    global config
    while(1):
        while (1):
            try:
                mt = os.path.getmtime(config["imgPath"])
                break
            except FileNotFoundError:
                print("Cannot find file: %s" % config["imgPath"])
                time.sleep(config["SFTPscanInterval"])
        # Check if modification time has changed
        if (mt > oldmt):
            print("File has changed. %d > %d" % (mt, oldmt))
            sendFile(password)
            oldmt = mt
        time.sleep(config["SFTPscanInterval"])
            
def sendFile(password):
    global config
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    try:
        with pysftp.Connection(config["hostname"], username = config["username"], password = password, port = config["port"], cnopts = cnopts) as sftp:
            sftp.chdir(config["remoteDir"])
            sftp.put(config["imgPath"])
        print("File uploaded")
    except:
        print(traceback.format_exc())

main()

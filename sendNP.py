import json
import os

try:
    import pysftp
except ImportError:
    print("{ERROR} You need the 'PySFTP' module in order to run this program!")
    exit(1)

import time
import traceback

try:
    import getpass
    has_getpass = True
except ImportError:
    has_getpass = False


config = {}
default_config = """{
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

def get_config():
    global default_config
    global config
    
    conf_file = "./npImage.json"
    
    if not os.path.isfile(conf_file):
        with open(conf_file, "w", encoding="utf-8") as cf:
            cf.write(default_config)
        print("Generated new config file (npImage.json)")
        exit(1)
        
    with open(conf_file, encoding="utf-8") as cf:
        config = json.loads(cf.read())
        check_config()
    
def check_config():
    global config
    
    expected_types = {
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
                    
    for option, expected_type in expected_types.items():
        try:
            if not isinstance(config[option], expected_type):
                print("Invalid %s. Expected type %s, got %s." % (option, expected_type, type(config[option])))
                exit(1)
        except KeyError:
            print("Missing option: %s" % option)
            exit(1)
            
    for channel in config["fontColour"]:
        if not isinstance(channel, int):
            print("Invalid fontColour value: %s. Expected type %s, got %s." % (channel, int, type(channel)))
            exit(1)
            
    for channel in config["backgroundColour"]:
        if not isinstance(channel, int):
            print("Invalid backgroundColour value: %s. Expected type %s, got %s." % (channel, int, type(channel)))
            exit(1)
            
    for channel in config["blankImageSize"]:
        if not isinstance(channel, int):
            print("Invalid blankImageSize value: %s. Expected type %s, got %s." % (channel, int, type(channel)))
            exit(1)
            
    for channel in config["blankImageBackground"]:
        if not isinstance(channel, int):
            print("Invalid blankImageBackground value: %s. Expected type %s, got %s." % (channel, int, type(channel)))
            exit(1)
            
    for channel in config["blankImageText"]:
        if not isinstance(channel, str):
            print("Invalid blankImageText value: %s. Expected type %s, got %s." % (channel, str, type(channel)))
            exit(1)
            
    for channel in config["blankImageFontColour"]:
        if not isinstance(channel, int):
            print("Invalid blankImageFontColour value: %s. Expected type %s, got %s." % (channel, int, type(channel)))
            exit(1)
    

def main():
    global config
    
    get_config()
    
    if has_getpass:
        password = getpass.getpass("Password for %s@%s: " % (config["username"], config["hostname"]))
    else:
        password = input("Password for %s@%s (WILL BE VISIBLE - USE GETPASS): " % (config["username"], config["hostname"]))
            
    while 1:
        try:
            oldmt = os.path.getmtime(config["imgPath"])
            break
        except FileNotFoundError:
            print("Cannot find file: %s" % config["imgPath"])
            time.sleep(config["SFTPscanInterval"])
            
    
    send_file(password)
    mainloop(oldmt, password)
    
def mainloop(oldmt, password):
    global config
    
    while 1:
        while 1:
            try:
                mt = os.path.getmtime(config["imgPath"])
                break
            except FileNotFoundError:
                print("Cannot find file: %s" % config["imgPath"])
                time.sleep(config["SFTPscanInterval"])
        # Check if modification time has changed
        if mt > oldmt:
            print("File has changed. %d > %d" % (mt, oldmt))
            send_file(password)
            oldmt = mt
        time.sleep(config["SFTPscanInterval"])
            
def send_file(password):
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

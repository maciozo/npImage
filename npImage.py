from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import time
import json
import os
import sys

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
    
    config["fontColour"] = tuple(config["fontColour"])
    config["backgroundColour"] = tuple(config["backgroundColour"])
    config["blankImageSize"] = tuple(config["blankImageSize"])
    config["blankImageBackground"] = tuple(config["blankImageBackground"])
    config["blankImageFontColour"] = tuple(config["blankImageFontColour"])
    
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
    getConfig()
    mainLoop("")
    
def createImage(text):
    global config
    lengths = []
    for line in text:
        lengths.append(len(line))
    maxLengthIndex = lengths.index(max(lengths))
    font = ImageFont.truetype(config["font"], config["fontSize"])
    imageSize = font.getsize(text[maxLengthIndex])
    lineHeight = imageSize[1]
    imageSize = (imageSize[0] + (2 * config["borderWidth"]), (lineHeight * len(text)) + (2 * config["borderWidth"]))
    
    try:
        img = Image.new(config["colourFormat"], imageSize, config["backgroundColour"])
    except ValueError:
        return 1
    draw = ImageDraw.Draw(img)
    
    lineNumber = 0
    for line in text:
        draw.text((config["borderWidth"], (lineHeight * lineNumber) + config["borderWidth"]), line, config["fontColour"], font = font)
        lineNumber += 1
    img.save(config["imgPath"])
    
def createBlankImage(text):
    global config
    lengths = []
    for line in text:
        lengths.append(len(line))
    maxLengthIndex = lengths.index(max(lengths))
    font = ImageFont.truetype(config["blankImageFont"], config["blankImageFontSize"])
    imageSize = font.getsize(text[maxLengthIndex])
    lineHeight = imageSize[1]
    imageSize = (imageSize[0] + (2 * config["blankImageBorderWidth"]), (lineHeight * len(text)) + (2 * config["blankImageBorderWidth"]))
    
    try:
        img = Image.new(config["blankImageColourFormat"], imageSize, config["blankImageBackground"])
    except ValueError:
        return 1
    draw = ImageDraw.Draw(img)
    
    lineNumber = 0
    for line in text:
        draw.text((config["blankImageBorderWidth"], (lineHeight * lineNumber) + config["blankImageBorderWidth"]), line, config["blankImageFontColour"], font = font)
        lineNumber += 1
    img.save(config["imgPath"])
    
def clearImage():
    global config
    if config["blankImageText"] != [""]:
        createBlankImage(config["blankImageText"])
    else:
        img = Image.new(config["blankImageColourFormat"], config["blankImageSize"], config["blankImageBackground"])
        img.save(config["imgPath"])

def mainLoop(oldSong):
    global config
    blankImage = False
    paused = False
    while (1):
        songInfo = getSongInfo()
        if (songInfo["isplaying"] != "1"):
            if not blankImage:
                clearImage()
                blankImage = True
        elif ((songInfo["path"] != oldSong) or ((songInfo["ispaused"] == "1") and (paused == False)) or ((songInfo["ispaused"] != "1") and (paused == True))):
            paused = False
            # print("New song: %s - %s" % (songInfo["artist"], songInfo["title"]))
            imageText = []
            
            if songInfo["ispaused"] == "1":
                paused = True
                imageText.append("Now playing (Paused)")
            else:
                imageText.append("Now playing")
            imageText.append("%s - %s" % (songInfo["artist"], songInfo["title"]))
            
            if songInfo["album"]:
                imageText.append(songInfo["album"])
                
            imageText.append("%s / %skb/s / %sbit / %sHz / %s / %s" % (songInfo["codec"], songInfo["bitrate"], songInfo["bitdepth"], songInfo["samplerate"], songInfo["channels"], songInfo["filesize"]))
            imageText.append(songInfo["playcount"])
            
            createImage(imageText)
            oldSong = songInfo["path"]
        time.sleep(config["scanInterval"])
    
def getSongInfo():
    global config
    songinfo = {}
    output = []
    with open(config["textPath"], "r", encoding="utf-8") as file:
        for line in file.readlines():
            line = line.replace("\r", "")
            if len(line.split("=")) > 2:
                songinfo[line.split("=")[0]] = "=".join(line.split("=").pop(0))[:-1]
            elif len(line.split("=")) < 2:
                songinfo[line.split("=")[0]] = ""
            elif len(line.split("=")) == 2:
                songinfo[line.split("=")[0]] = line.split("=")[1][:-1]
    if songinfo["isplaying"] == "1":
        songinfo["title"] = songinfo["title"].rstrip() # Fix for Heartfire's broken title metadata
        
        if songinfo["album"] == "?":
            if songinfo["path"][:4] == "http":
                songinfo["album"] = songinfo["path"]
            else:
                songinfo["album"] = ""
            
        if songinfo["length"] == "?":
            songinfo["length"] = ""
            
        if songinfo["filesize"] == "?":
            songinfo["filesize"] = ""
            
        if songinfo["playcount"] == "1":
            songinfo["playcount"] = "%s total play" % songinfo["playcount"]
            
        else:
            songinfo["playcount"] = "%s total plays" % songinfo["playcount"]
            
        if songinfo["channels"] == "1":
            songinfo["channels"] = "%s channel" % songinfo["channels"]
        else:
            songinfo["channels"] = "%s channels" % songinfo["channels"]
    
    return songinfo
    
main()

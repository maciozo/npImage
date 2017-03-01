from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import time
import os

imgPath = "./image.png"
textPath = "D:/np.txt"

def main():
    global imgPath, textPath
    mainLoop("", imgPath, textPath)
    
def createImage(text, imgPath):
    lengths = []
    for line in text:
        # print(line)
        lengths.append(len(line))
    maxLengthIndex = lengths.index(max(lengths))
    font = ImageFont.truetype("unifont-9.0.04.ttf", 15)
    imageSize = font.getsize(text[maxLengthIndex])
    lineHeight = imageSize[1]
    imageSize = (imageSize[0], lineHeight * len(text))
    
    try:
        img = Image.new("RGBA", imageSize, (0, 0, 0, 0))
    except ValueError:
        return 1
    draw = ImageDraw.Draw(img)
    
    lineNumber = 0
    for line in text:
        draw.text((0, lineHeight * lineNumber), line, (255, 255, 255, 255), font=font)
        lineNumber += 1
    img.save(imgPath)
    
def clearImage(imgPath):
    img = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    img.save(imgPath)

def mainLoop(oldSong, imgPath, textPath):
    while (1):
        songInfo = getSongInfo(textPath)
        if (songInfo["isplaying"] != "1"):
            clearImage(imgPath)
        elif (songInfo["path"] != oldSong):
            print("New song")
            imageText = []
            
            imageText.append("Now playing")
            imageText.append("%s - %s" % (songInfo["artist"], songInfo["title"]))
            
            if songInfo["album"]:
                imageText.append(songInfo["album"])
                
            imageText.append("%s / %skb/s / %sbit / %sHz / %s / %s" % (songInfo["codec"], songInfo["bitrate"], songInfo["bitdepth"], songInfo["samplerate"], songInfo["channels"], songInfo["filesize"]))
            imageText.append(songInfo["playcount"])
            
            createImage(imageText, imgPath)
            oldSong = songInfo["path"]
        time.sleep(10)
    
def getSongInfo(textFile):
    songinfo = {}
    output = []
    with open(textFile, "r", encoding="utf-8") as file:
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
            
        if songinfo["playcount"] == 1:
            songinfo["playcount"] = "%s total play" % songinfo["playcount"]
            
        else:
            songinfo["playcount"] = "%s total plays" % songinfo["playcount"]
            
        if songinfo["channels"] == 1:
            songinfo["channels"] = "%s channel" % songinfo["channels"]
        else:
            songinfo["channels"] = "%s channels" % songinfo["channels"]
    
    return songinfo
    
main()
# npImage
Generates image with info of the currently playing song. Requires preformatted file with metadata.

![Preview](https://u.nya.is/vacgoy.png)

## Metadata file format
`textPath` must point to a UTF-8 text file with at least these fields.
```
artist=<artist>
title=<title>
codec=<codec>
bitrate=<bitrate>
bitdepth=<bitdepth>
samplerate=<samplerate>
channels=<channels>
filesize=<filesize>
isplaying=<isplaying> (must be 1 when true)
ispaused=<ispaused> (must be 1 when true)
path=<path> (Can also just be any unique identifier for each song. This is only used to check if the song has changed.)
playcount=<playcount>
```

Example
```
ispaused=1
playcount=9
filesize=46.5 MB
channels=2
bitdepth=16
codec=FLAC
samplerate=44100
isplaying=1
artist=bothneco
title=choco-mint flavor
album=mikgazer vol.1
bitrate=1042
path=G:\Music\[2012] V.A. - mikgazer vol.1 [FLAC]\08. choco-mint flavor.flac
```

Will produce a PNG with a transparent background and the text below in white
```
Now playing (Paused)
bothneco - choco-mint flavor
mikgazer vol.1
FLAC / 1042kb/s / 16bit / 44100Hz / 2 channels / 46.5 MB
9 total plays
```

If nothing is playing (`isplaying=x` where `x` is not `1`), it will produce a 1x1 transparent PNG.

## Sending to SFTP server
Configure values in `npImage.json` and run seperately.

## Configuration
The `npImage.json` file is used to configure `npImage`.
```
{
    "imgPath" : "./image.png", // Where to save the generated image
    "textPath" : "./np.txt", // Path of text from which to generate the image
    
    "font" : "arial.ttf", // The font to use in the image
    "fontSize" : 15, // The size of the font
    
    // Make sure that this format is compatible with your image format.
    // Adjust the colours accordingly. e.g., don't include an alpha value for an RGB image.
    // e.g. for RGB, (255, 255, 255) will be white.
    // See https://pillow.readthedocs.io/en/4.0.x/handbook/concepts.html#concept-modes for more info.
    "colourFormat" : "RGBA",
    
    "fontColour" : [0, 0, 0, 255], // 8bpc RGBA
    "backgroundColour" : [0, 0, 0, 0], // Background colour of the image. Default is transparent.
    
    "borderWidth" : 0, // In pixels. Amount of white space around the generated text
    
    "scanInterval" : 10, // How often to check for playback changes. In seconds.
    
    // Paramaters for the image to be generated when no music is playing
    // Default is a 1x1 transparent pixel.
    "blankImageSize" : (1, 1), // Ignored if blankImageText specified. (width, height)
    "blankImageColourFormat" : "RGBA",
    "blankImageBackground" : [0, 0, 0, 0],
    "blankImageText" : [""], // Will override blankImageSize if not empty. Each line is its own element in the list.
    "blankImageFont" : "arial.ttf",
    "blankImageFontSize" : 15,
    "blankImageFontColour" : [0, 0, 0, 255],
    "blankImageBorderWidth": 0, // Ignored if no text specified.
    
    // For SFTP (setup not required if not using sendNP.py)
    "hostname" : "example.org", // Address of server.
    "port" : 22, // Default SSH/SFTP port is 22
    "username" : "username",
    "remoteDir" : ".", // Directory on the server to upload image to.
    "SFTPscanInterval" : 10, // How often to check for an updated image. In seconds.
}
```
Note that the actual json file will not be annotated.

## Dependancies
- Python 3.5 (May work on others - not tested. Will probably work on 3.4)
- Pillow
- pysftp (If using `sendNP.py`)
- getpass (Recommended, SSH password will be visible otherwise)

## Todo
### Customisation
- Coloured border

### Functionality
- Album art in image
- Host verification for SSH

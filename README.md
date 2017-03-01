# npImage
Generates image with info of the currently playing song. Requires preformatted file with metadata.

Preview best visible on a dark background.
![Preview](https://u.nya.is/apzfbr.png)

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
Configure values in `sendNP.py` and run seperately.

## Dependancies
- Python 3.5 (May work on others - not tested)
- Pillow
- pysftp
- getpass (Recommended, SSH password will be visible otherwise)
- unifont-9.0.04

## Todo
### Customisation
- Font selection (to remove unifont dependancy)
- Colour selection
- Format selection

### Functionality
- Album art in image
- Host verification for SSH
- Use config file rather than hardcoded variables

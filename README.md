# Minecraft Depth Extractor
An Optifine shader and a Python script to extract live depth data from Minecraft

## Requirements
- Minecraft Java Edition with Optifine
- Python 3 with the following modules `mss`, `pywin32`, `opencv-python`
- Windows (while this could be made to work on any OS, the window-identification part of the screen recording code is currently tailored for Windows)

## Steps
1) Put the DepthExtractor folder into your shaderpacks folder (e.g. `C:\Users\Username\AppData\Roaming\.minecraft\shaderpacks\`)
2) Enable the DepthExtractor shader in Minecraft (Options… -> Video Settings… -> Shaders…)
3) Run stream.py
4) Both RGB and Depth data are now streamed in MJPEG format. You can hook them into your streaming/recording software or view them live by visiting http://localhost:9090/ in your browser.

![Demo](https://github.com/jankais3r/Minecraft-Depth-Extractor/blob/main/demo.gif)


## Tips
- If you are getting low FPS, decrease the size of your Minecraft window.
- If you are processing the video streams in any way, don't leave the browser window open to avoid wasting your computer's resources.

## Inspiration
The basic idea behind this shader is based on [this video](https://www.youtube.com/watch?v=nakyctgYDM8).

# NYCC - Not so clever YeeLight CLI controller

A CLI controller to manage some YeeLight properties from your terminal.
With this really not so clever piece of code you can:

- turn on/of your YeeLight;
- change its color, temperature, brightness;
- save and apply preset scenes.


## Installation

NYCC works with *Python 3* and requires Python YeeLight library so

```
pip install yeelight
```
It's important that you enable LAN mode on your YeeLight settings
from the Yeelight application.
As of this moment the controller does not implement discovery so you 
must know the IP address of your light.

To initialize run
```
yeelight_controller.py -i <IP_ADDRESS>
```

this will create the config folders in `~/.config/yeelight_controller`

## Usage
```
-i --init <IP_ADDRESS>
-c --color <HEX_COLOR>
-t --temperature <COLOR_TEMPERATURE>  #color settings override temperature
-b --brightness <BRIGHTNESS[0-100]>
-o --off
-l --list-scenes #list all scene presets
-s --scene <SCENE_NAME> #apply scene preset
-j --save-json <SCENE_NAME> #save current settings as new scene
-r --reset
```

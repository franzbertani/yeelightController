#!/usr/bin/env python3

import getopt
import sys
import json
from yeelight import *
from os.path import expanduser


def usage():
    print("Usage:")
    print("-i --init IP_ADDRESS")
    print("-c --color HEX_COLOR or -t --temperature COLOR_TEMPERATURE; color settings override temperature")
    print("-b --brightness BRIGHTNESS[0-100]")
    print("-o --off")
    print("-r --reset")


def create_default_file(ip_addr):
    properties['brightness'] = DEFAULT_BRIGHTNESS
    properties['color_rgb'] = DEFAULT_COLOR_RGB
    properties['color_temp'] = DEFAULT_COLOR_TEMP
    properties['ip_addr'] = ip_addr
    with open(DEFAULT_JSON_NAME, "w") as outFile:
        json.dump(properties, outFile)


def reset():
    global properties
    properties = {}
    with open(USER_JSON_NAME, "w") as outFile:
        json.dump(properties, outFile)


def save_user_file():
    with open(USER_JSON_NAME, "w") as outFile:
        json.dump(user_properties, outFile)


def read_properties():
    global properties
    global user_properties
    try:
        with open(DEFAULT_JSON_NAME, "r") as infile:
            properties = json.load(infile)
    except IOError:
        print("default settings file missing, baaad!\nRun with -i IP_ADDRESS")
        sys.exit(2)
    try:
        with open(USER_JSON_NAME, "r") as infile:
            user_properties = json.load(infile)
            for k, v in user_properties.items():
                properties[k] = v
                print("Found user settings for " + k)
    except IOError:
        print("Default settings applied")


def read_scene(scene_name):
    global properties
    try:
        with open(DEFAULT_SCENE_LOCATION + scene_name + ".json", "r") as infile:
            scene_properties = json.load(infile)
            for k, v in scene_properties.items():
                properties[k] = v
                print("Applied scene setting for " + k)
    except IOError:
        print("Scene file missing, no scene called " + scene_name)


def apply_properties(bulb):
    bulb.turn_on()
    bulb.set_brightness(int(properties['brightness']))
    if properties['color_rgb']:
        bulb.set_rgb(properties['color_rgb'][0], properties[
                     'color_rgb'][1], properties['color_rgb'][2])
    else:
        bulb.set_color_temp(int(properties['color_temp']))


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:c:t:b:s:ro", [
                                   "help", "color", "temperature", "brightness", "scene", "off", "reset"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-i", "--init"):
            create_default_file(a)
        elif o in ("-r", "--reset"):
            reset()

    read_properties()
    bulb = Bulb(properties['ip_addr'])
    updateUserFile = False

    for o, a in opts:
        if o in ("-c", "--color"):
            red = int(a[0:2], 16)
            green = int(a[2:4], 16)
            blue = int(a[4:6], 16)
            user_properties['color_rgb'] = (red, green, blue)
            properties['color_rgb'] = (red, green, blue)
            updateUserFile = True
        elif o in ("-t", "--temperature"):
            user_properties['color_temp'] = a
            properties['color_temp'] = a
            updateUserFile = True
        elif o in ("-b", "--brightness"):
            user_properties['brightness'] = a
            properties['brightness'] = a
            updateUserFile = True
        elif o in ("-s", "--scene"):
            read_scene(a)
        elif o in ("-o", "--off"):
            bulb.turn_off()
            return

    if updateUserFile:
        print("Saving new user properties")
        save_user_file()

    apply_properties(bulb)


if __name__ == "__main__":

    DEFAULT_BRIGHTNESS = "100"
    DEFAULT_COLOR_TEMP = "4411"
    DEFAULT_COLOR_RGB = []
    home = expanduser("~")
    DEFAULT_SCENE_LOCATION = home + "/.yeelight_scene/"
    DEFAULT_JSON_NAME = home + "/.default_yeelight_properties.json"
    USER_JSON_NAME = home + "/.user_yeelight_properties.json"

    properties = {}
    user_properties = {}

    main()

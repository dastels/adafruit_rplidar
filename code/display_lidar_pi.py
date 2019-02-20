"""
Consume LIDAR measurement file and create an image for display.

Adafruit invests time and resources providing this open source code.
Please support Adafruit and open source hardware by purchasing
products from Adafruit!

Written by Dave Astels for Adafruit Industries
Copyright (c) 2019 Adafruit Industries
Licensed under the MIT license.

All text above must be included in any redistribution.
"""

import time
import os
import sys
from math import cos, sin, pi
import pygame
from rplidar import RPLidar


os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()
lcd = pygame.display.set_mode((480,320))
pygame.mouse.set_visible(False)
lcd.fill((0,0,0))
pygame.display.update()
PORT_NAME = '/dev/ttyUSB0'


def run():
    '''Main function'''
    max_distance = 0
    lidar = RPLidar(PORT_NAME)
    try:
        print('Recording measurments... Press Crl+C to stop.')
        for scan in lidar.iter_scans():
            if len(scan) > 100:
                lcd.fill((0,0,0))
                for (_, angle, distance) in scan:
                    max_distance = max([min([5000, distance]), max_distance])
                    radians = angle * pi / 180.0
                    x = distance * cos(radians)
                    y = distance * sin(radians)
                    point = (240 + int(x / max_distance * 159), 160 + int(y / max_distance * 159))
                    lcd.set_at(point, pygame.Color(255, 255, 255))
                pygame.display.update()
                print(max_distance)

    except KeyboardInterrupt:
        print('Stoping.')
    lidar.stop()
    lidar.disconnect()
    outfile.close()

if __name__ == '__main__':
    run()

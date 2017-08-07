
# ESP32_GPS
Getting GPS data from the u-blox NEO-6M GPS module

A simple serial connection gets the data from the GPS.

I first tried the very comprehensive micropyGPS.py from Michael Calvin McCoy, but I found this a little heavy going for the ESP32 so I made my own basic parser

nmea.py just needs all the serial data throwing at it and it populates a few variables.

To see how to use it see gps.py. This uses my ST7735 library to display the GPS data on a small TFT.

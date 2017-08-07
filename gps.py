from machine import UART, Pin, SPI
from micropyGPS import MicropyGPS
import utime
import lcd_gfx
from bmp import bmp
import ST7735
import nmea

def display(my_nmea, margin, d):
	d.p_string(margin,5,my_nmea.time)
	d.p_string(margin,15,my_nmea.date)
	d.p_string(margin,25,'{:10.4f}'.format(my_nmea.latitude))
	d.p_string(margin,35,'{:10.4f}'.format(my_nmea.longitude))
	d.p_string(margin,45,'{:02d}'.format(my_nmea.satcount))

margin = 72

spi = SPI(-1, baudrate=80000000, polarity=1, phase=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))

d = ST7735.ST7735(spi, offset=3, c_mode='BGR')
d.reset()
d.begin()

d._bground = 0x0000
d.fill_screen(d._bground)

utime.sleep(1)

d._bground = 0x001f
d.fill_screen(d._bground)

d._color = 0xffff

d.set_rotation(1)

d.p_string(2,5, '      Time: ')
d.p_string(2,15,'      Date: ')
d.p_string(2,25,'  Latitude: ')
d.p_string(2,35,' Longitude: ')
d.p_string(2,45,'Satellites: ')


my_gps = MicropyGPS(location_formatting='dd')

uart = UART(2, 9600)
now = utime.ticks_ms()
sentence = ''
state = ''
my_nmea = nmea.nmea(debug=1)

while 1:
	while uart.any():
		b = uart.read()
		my_nmea.parse(b)
		
	if utime.ticks_diff(utime.ticks_ms(), now) > 5000:
		now = utime.ticks_ms()
		print('{} {} {} {}'.format(my_nmea.time, my_nmea.date, my_nmea.latitude, my_nmea.longitude))
		display(my_nmea, margin, d)

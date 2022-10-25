import math

from neopixel import *

#-----------------------------------------------------------------------------------------
# CONGIFURE YOUR BOARD HERE!
# LED strip configuration:
NUM_BALLS		= 41				# Number of balls on your board #CHANGED FOR XL
NUM_POS		= 7				# position of the ball
PIXEL_DENSITY	= 30				# This is how dense your strip is with pixels. 30 is the ideal density to buy (LEDs/meter)

PIXEL_RATIO		= PIXEL_DENSITY/30	# Needed for the odd strips like mine
LED_PIN        	= 18      			# GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    	= 800000  			# LED signal frequency in hertz (usually 800khz)
LED_DMA        	= 10       			# DMA channel to use for generating signal (try 5)
LED_INVERT     	= False   			# True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    	= 0       			# set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      	= ws.WS2811_STRIP_RGB   # Strip type and colour ordering

# Define the rows the grid by defining the ball numbers.

# THIS IS IMPORTANT AND MAY BE DIFFERENT FOR YOUR BOARD!!!!!!

# This is the only way the program knows the correct LED numbers for each ball AND is essential to displaying text and things properly
#-----------------------------------------------------------------------------------------

colorListColor = [
	Color(255,0,0),		# Red
	Color(255,255,0),	# Yellow
	Color(255,0,255),	# Pink
	Color(0,255,255),	# Teal
	Color(0,255,0),		# Green
	Color(0,0,255),		# Blue
	Color(125,0,255),	# Fuscia
	Color(200,255,0),	# Optic Yellow
	Color(50,0,255),	# Purple
	Color(255,125,0),	# Orange
	Color(255,0,50),	# Hot Pink
	Color(52,192,235),	# Lblue
	Color(52,192,235)	# Mint
]

colorListRGB = [
	[255,0,0],		# Red
	[52,192,235],		# Lblue
	[52,235,161],		# Mint
	[255,255,0],	# Yellow
	[255,0,255],	# Pink
	[0,255,255],	# Teal
	[0,255,0],		# Green
	[0,0,255],		# Blue
	[125,0,255],	# Fuscia
	[200,255,0],	# Optic Yellow
	[50,0,255],		# Purple
	[255,125,0],	# Orange
	[255,0,50]		# Hot Pink
]
class Ball:
	def __init__(self, pos):   #location is a list of two variables, [row, col]
		self.pos = pos    #[row,col]

		self.ledNum = ledAddresses[self.location[0]]   #[pos]	
      
		self.wings = False           #this is used to determine whether the ball is being used for text display or not
		self.accent = False
		self.color = Color(0,0,0)   #current ball color
		
# Buffer
buffer = [                          # This is tricky and must be defined this way. I'm creating 7 instances of a list that contains 20 instances of Color(0,0,0). They must all be separately defined
	[Color(0,0,0)] * 20,
	[Color(0,0,0)] * 20,
	[Color(0,0,0)] * 20,
	[Color(0,0,0)] * 20,
	[Color(0,0,0)] * 20,
	[Color(0,0,0)] * 20,
	[Color(0,0,0)] * 20
]      


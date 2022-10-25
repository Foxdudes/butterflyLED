import argparse
import json
import math
import random
import signal
import sys
import time

import requests
from neopixel import *
from Utils import *

# This is the PingPongBoard class that drives everything. All functions related to lighting and writing are in here. 
class PingPongBoard:
	def __init__(self):
		self.num_balls = NUM_BALLS		# Needed for changing board type
		self.num_pos = NUM_POS		# Needed for changing board type
		

		self.animationFrame = 0				# Used for animations, start at 0
		self.animationEnd = 1				# Default animation end frame. This is always changed
		self.animationStartTime = [0,0]		# Used for animations and when to move the string
		self.animationTimeElapsed = [0,0]	# Used for animations and when to move the string
		self.breathColor = None				# Necessary for the breathing animation
		
		self.displayString = ['', '']			# This is the string that will be ultimately displayed on screen
		self.displayStringPrev = ['', '']		# This is what the display string was during the previous loop
		self.displayStringLength = [0, 0]		# This is calculated and used to determine when we have cycled through an entire string during animations

		self.minsPrev = None			# Used to calculate when a minute has elapsed. This is useful to only update the weather once a minute TODO Change this

		# Load settings that are saved to files 
		self.loadSettings()

		# Set up the ball objects // NIET ZEKER!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		self.balls = []
		for i in range(self.num_pos):
			self.balls.append([0]) 

		# Initialize the ball objects
		self.setupBalls()

		#Intialize the strip
		self.strip = Adafruit_NeoPixel(self.led_count, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, self.brightness, LED_CHANNEL, LED_STRIP)
		self.strip.begin()

	# Sets up a ball object for every single ball on the board. The ball object definition can be found in Utils
	def setupBalls(self):
		for y in range(self.num_pos):
			self.balls[y] = Ball([y])    #passes [row,col], and the type of board which is used for the ledAdresses

	# Actually lights a specic ball (LED) with the color provided to the function. This will check to see if the color is different than the one already set for the ball first. If it is the same then it will not rewrite.
	def writeBallColor(self,pos,color):
		# Do not proceed if bad coordinates (could maybe replace with try/catch)
		if pos < 0 or pos >= self.num_pos:
			return

		# If the color is different than what the buffer has stored, write it and show it
		if self.balls[pos].color != color:
			self.strip.setPixelColor((self.balls[pos].ledNum)*PIXEL_RATIO,color)
			self.balls[pos].color = color

	# Changes the text state of a specific ball. This does NOT actually change the color. Merely whether or not the ball is used to display text. Will not rewrite state if the same.
	def writeBallState(self,pos,wings,accent):
		# Do not proceed if bad coordinates (could maybe replace with try/catch)
		if pos < 0 or pos >= self.num_pos:
			return

		# If the text state is different than what the buffer has stored, change it
		if self.balls[pos].wings != wings:
			self.balls[pos].wings = wings
		
		if self.balls[pos].accent != accent:
			self.balls[pos].accent = accent

	# This steps the animation frame by one. If the animation frame has reached animationEnd, reset the frame to 0
	def updateFrame(self, animationEnd):
		self.animationFrame += 1
		self.animationEnd = animationEnd
		if(self.animationFrame>=self.animationEnd):
			self.animationFrame = 0
		return self.animationFrame

	# This sets every ball's text state to False on the board
	def StateWipe(self):
		for y in range(self.num_pos):
			self.writeBallState(y,False,False)

	# Fills sections/the whole board with the provided color. This function can fill: the whole board, only non-text balls, only text balls
	def (self,color,fullwipe=False,wingsOnly=False,accentOnly=False):
		# Fill the full screen
		if fullwipe:
			for y in range(self.num_pos):
				self.writeBallState(y,False,False)
				self.writeBallColor(y,color)
		# Fill only the text
		elif wingsOnly:
			for y in range(self.num_pos):
				if self.balls[y].wings == True:
					self.writeBallColor(y,color)
		
		elif accentOnly:
			for y in range(self.num_pos):
				if self.balls[y].accent == True:
					self.writeBallColor(y,color)
						
		# Fill only the non-text
		else:
			for y in range(self.num_pos):
				if (self.balls[y].wings == False) and (self.balls[y].accent == False):
					self.writeBallColor(y,color)
		self.strip.show()

	# The core function that updates both the background color and text colors
	def updateBoardColors(self):
		# Write the BG. Will not overwrite text per the function
		if self.
		
		
		[0] == "animation":
			if self.bgColor[1] == "rainbow":
				self.rainbow()
			elif self.bgColor[1] == "rainbowCycle":
				self.rainbowCycle()
			elif self.bgColor[1] == "test":
				self.test()
			elif self.bgColor[1] == "breathing":
				self.breathing(False)
		elif self.bgColor[0] == "solid" and self.bgDisplayChanged:
			# print "writing BG color..."	#debugging
			self.colorFill(self.bgColor[1])
		self.bgDisplayChanged = False

		# Color the Wings
		# Check to see if we have a text color animation
		if self.wingsColor[0] == "animation":
			if self.wingsColor[1] == "rainbow":
				self.rainbowWings()
			elif self.wingsColor[1] == "rainbowCycle":
				self.rainbowCycleWings()
			elif self.wingsColor[1] == "testText":
				self.testWings()
			elif self.wingsColor[1] == "breathing":
				self.breathing(True)
		# Else, check for solid notification
		elif self.wingsColor[0] == 'solid' and self.wingsDisplayChanged:
			for y in range(self.num_pos):
				if self.balls[y].wings == True:
					if self.textColor[0] == 'animation':
						return
					else:
						self.writeBallColor(y,self.wingsColor[1])
			self.strip.show()
		# Reset the display changed boolean now that it has been updated
		self.accentDisplayChanged = False
		
		# Color the Text
		# Check to see if we have a text color animation
		if self.accentColor[0] == "animation":
			if self.accentColor[1] == "rainbow":
				self.rainbowAccent()
			elif self.accentColor[1] == "rainbowCycle":
				self.rainbowCycleAccent()
			elif self.accentColor[1] == "testText":
				self.testAccent()
			elif self.accentColor[1] == "breathing":
				self.breathing(True)
		# Else, check for solid notification
		elif self.accentColor[0] == 'solid' and self.accentDisplayChanged:
			for y in range(self.num_pos):
				if self.balls[y].accent == True:
					if self.accentColor[0] == 'animation':
						return
					else:
						self.writeBallColor(y,self.accentColor[1])
			self.strip.show()
		
		# Reset the display changed boolean now that it has been updated
		self.accentDisplayChanged = False

	
# COLOR ANIMATIONS ---------------------------------------------------------------------
	# Used in rainbow and rainbowCycle to determine the color during the cycle. Makes for nice smooth transitions
	def wheel(self,pos):
		# Generate rainbow colors across 0-255 positions.
		if pos < 85:
			return Color(pos * 3, 255 - pos * 3, 0)     #green to red
		elif pos < 170:
			pos -= 85
			return Color(255 - pos * 3, 0, pos * 3)     #red to blue
		else:
			pos -= 170
			return Color(0, pos * 3, 255 - pos * 3)     #blue to green
		
	def wheel2(self,pos):
		# Generate rainbow colors across 0-255 positions.
		return Color(0, 204 - pos, 255 - pos)
	
	# Rainbow color animation
	def rainbow(self,wait_ms=18):
		# Draw rainbow that fades across all pixels at once.
		j = self.updateFrame((self.led_count+self.led_count))

		for y in range(self.num_pos):
			i = self.num_pos + y
			if self.balls[y].wings == False and self.balls[y].accent == False:
				self.writeBallColor(y,self.wheel(((i*PIXEL_RATIO)+j) & 255))
		self.strip.show()
		time.sleep(wait_ms/1000.0)
		
	def rainbowWings(self,wait_ms=18):
		# Draw rainbow that fades across all pixels at once.
		j = self.updateFrame((self.led_count+self.led_count))

		for y in range(self.num_pos):
			i = self.num_pos + y
			if self.balls[y].wings == True and self.balls[y].accent == False:
				self.writeBallColor(y,self.wheel(((i*PIXEL_RATIO)+j) & 255))
		self.strip.show()
		time.sleep(wait_ms/1000.0)
		
	def rainbowAccent(self,wait_ms=18):
		# Draw rainbow that fades across all pixels at once.
		j = self.updateFrame((self.led_count+self.led_count))

		for y in range(self.num_pos):
			i = self.num_pos + y
			if self.balls[y].wings == False and self.balls[y].accent == True:
				self.writeBallColor(y,self.wheel(((i*PIXEL_RATIO)+j) & 255))
		self.strip.show()
		time.sleep(wait_ms/1000.0)
		
	# test color animation
	def test(self,wait_ms=18):
		# Draw rainbow that fades across all pixels at once.
		j = self.updateFrame((self.led_count+self.led_count))

		for y in range(self.num_pos):
			i = self.num_pos + y
			if self.balls[y].wings == False and self.balls[y].accent == False:
				self.writeBallColor(y,self.wheel2(((i*PIXEL_RATIO)+j) & 150))
		self.strip.show()
		time.sleep(wait_ms/1000.0)
		
	# testtext color animation
	def testWings(self,wait_ms=1):
		# Draw rainbow that fades across all pixels at once.
		j = self.updateFrame((self.led_count+self.led_count))

		for y in range(self.num_pos):
			i = self.num_pos + y
			if self.balls[y].wings == True and self.balls[y].accent == False:
				self.writeBallColor(y,self.wheel2(((i*PIXEL_RATIO)+j) & 150))
		self.strip.show()
		time.sleep(wait_ms/1000.0)
		
	def testAccent(self,wait_ms=1):
		# Draw rainbow that fades across all pixels at once.
		j = self.updateFrame((self.led_count+self.led_count))

		for y in range(self.num_pos):
			i = self.num_pos + y
			if self.balls[y].wings == False and self.balls[y].accent == True:
				self.writeBallColor(y,self.wheel2(((i*PIXEL_RATIO)+j) & 150))
		self.strip.show()
		time.sleep(wait_ms/1000.0)
		
		
	# Rainbow cycle makes all of the BG balls the same color and changes the color over time
	def rainbowCycle(self,wait_ms=20):
		# Draw rainbow that uniformly distributes itself across all pixels.
		j = self.updateFrame((self.led_count+self.led_count))

		for y in range(self.num_pos):
			i = self.num_pos + y
			if self.balls[y].wings == False and self.balls[y].accent == False :
				self.writeBallColor(y,self.wheel((((i*PIXEL_RATIO)/(self.num_balls*PIXEL_RATIO))+j) & 255))
		self.strip.show()
		time.sleep(wait_ms/1000.0)

		# Rainbow cycle makes all of the text the same color and changes the color over time
	def rainbowCycleWings(self,wait_ms=20):
		# Draw rainbow that uniformly distributes itself across all pixels.
		j = self.updateFrame((self.led_count+self.led_count))

		for y in range(self.num_pos):
			i = self.num_pos + y
			if self.balls[y].wings == True and self.balls[y].accent == False :
				self.writeBallColor(y,self.wheel((((i*PIXEL_RATIO)/(self.num_balls*PIXEL_RATIO))+j) & 255))
		self.strip.show()
		time.sleep(wait_ms/1000.0)
		
	def rainbowCycleAccent(self,wait_ms=20):
		# Draw rainbow that uniformly distributes itself across all pixels.
		j = self.updateFrame((self.led_count+self.led_count))

		for y in range(self.num_pos):
			i = self.num_pos + y
			if self.balls[y].wings == False and self.balls[y].accent == True :
				self.writeBallColor(y,self.wheel((((i*PIXEL_RATIO)/(self.num_balls*PIXEL_RATIO))+j) & 255))
		self.strip.show()
		time.sleep(wait_ms/1000.0)

	# Breathing color animation. Uses the random color list in Utils
	def breathing(self,wings=True,accent=False,wait_ms=20):
		# Cycle in and out of random colors from colorList
		j = self.updateFrame(100)

		# If we are on a new cycle, or a color has not been picked then pick a color
		if j == 0 or self.breathColor == None:
			self.breathColor = random.choice(colorListRGB)

		# The brightness factor 0-1.0. Adjusts the brightness of the color
		brightnessFactor = math.sin(j*(math.pi/100))

		# Apply the brightness factor to the color selected
		self.breathColorModified = [int(i*brightnessFactor) for i in self.breathColor]

		# Color the balls
		self.colorFill(Color(self.breathColorModified[0],self.breathColorModified[1],self.breathColorModified[2]),False,wings)
		time.sleep(wait_ms/1000.0)	# wait time

# CONTENT GENERATION --------------------------------------------------------------------

	# This function obtains the time and concatenates it to the display string
	def time(self, lineNum):
		# Get the current local time and parse it out to usable variables
		t = time.localtime()
		hours = t.tm_hour
		mins = t.tm_min
		secs = t.tm_sec

		# If the time format calls for 12 hour, convert the time
		if self.timeFormat == '12h':
			# Convert 24h time to 12h time
			if hours > 12:
				hours -= 12

			# If it is midnight, change the clock to 12
			if hours == 0:
				hours = 12

		# Create the minute string
		if mins < 10:
			minStr = '0' + str(mins)
		else:
			minStr = str(mins)

		# Create the hour string
		if hours < 10 and self.animationSpeed[lineNum] == 0:
			if self.timeFormat == '12h':
				hourStr = ' ' + str(hours)
			elif self.timeFormat == '24h':
				hourStr = '0' + str(hours)
		else:
			hourStr = str(hours)

		# Used to determine colon lit state
		if secs % 2 == 1 and self.animationSpeed[lineNum] <= 5.0 and self.lineCount == 1:
			# Even seconds, concatenate the strings with a colon in the middle
			timeStr = hourStr + ';' + minStr
		else:
			# Odd seconds, concatenate the strings with a semicolon(blank) in the middle
			timeStr = hourStr + ':' + minStr 

		# Concatenate the date string to the master string with a space termination
		if lineNum == 0:
			self.displayString[0] += timeStr + ' '
		elif lineNum == 1:
			self.displayString[1] += timeStr + ' '

		# Check to see if the minute has changed this is to update the weather. 
		if mins != self.minsPrev:
			self.updateWeather = True
			self.minsPrev = mins

	# This function obtains the date and concatenates it to the display string
	def date(self, lineNum):
		# Get the current local time and parse it out to usable variables
		t = time.localtime()
		mon = t.tm_mon
		day = t.tm_mday
		year = t.tm_year

		monStr = str(mon)
		dayStr = str(day)
		yearStr = str(year)

		# Write the date string
		dateStr = monStr + '-' + dayStr + '-' + yearStr[-2:]
		
		# Concatenate the date string to the master string with a space termination
		if lineNum == 0:
			self.displayString[0] += dateStr + ' '
		elif lineNum == 1:
			self.displayString[1] += dateStr + ' '

	# This function concatenates the custom text to the display string
	def text(self, lineNum):
		textStr = self.customText.upper()

		if lineNum == 0:
			self.displayString[0] += textStr + ' '
		elif lineNum == 1:
			self.displayString[1] += textStr + ' '

	# This function obtains the weather and concatenates it to the display string
	def weather(self, lineNum):
		# In case we are not displaying the time, check the time to see if we need to update the weather
		# Get the current local time and parse it out to usable variables
		t = time.localtime()
		mins = t.tm_min

		# Check to see if the minute has changed this is to update the weather. 
		if mins != self.minsPrev:
			self.updateWeather = True
			self.minsPrev = mins		

		# base_url variable to store url //
		base_url = "http://api.openweathermap.org/data/2.5/weather?"

		# If the zip code field is not empty then use the zip code. Otherwise use the filled city name
		if self.weatherZipLocation != '':
			complete_url = base_url + "appid=" + self.openWeatherKey + "&zip=" + self.weatherZipLocation
		else:
			complete_url = base_url + "appid=" + self.openWeatherKey + "&q=" + self.weatherCityLocation

		if self.updateWeather:
			try:
				response = requests.get(complete_url)
			except:
				return

			self.weatherResponse = response.json()
			self.updateWeather = False

			# Stringify the cod element for error checking
			self.weatherResponse['cod'] = str(self.weatherResponse['cod'])

		if self.weatherResponse['cod'] == '401':
			weatherStr = 'key error'
		if self.weatherResponse['cod'] == '404':
			weatherStr = 'city not found'
		elif self.weatherResponse['cod'] == '200':
			y = self.weatherResponse['main']

			current_temperature = float(y['temp'])

			if self.tempUnits == 'k':
				current_temperature = str(int(round(current_temperature)))
				unit = ' K '
			elif self.tempUnits == 'c':
				current_temperature = str(int(round(current_temperature - 273.15)))
				unit = '`C '
			elif self.tempUnits == 'f':
				current_temperature = str(int(round(current_temperature * (9.0/5) - 459.67)))	
				unit = '`F '	# Convert to fahrenheit

			weather_description = self.weatherResponse['weather'][0]['description']

			weatherStr = current_temperature + unit + weather_description
		else:
			weatherStr = 'error'

		# Concatenate the weather string to the display string
		weatherStr = weatherStr.upper() 	# Uppercase the string

		if lineNum == 0:
			self.displayString[0] += weatherStr + ' '
		elif lineNum == 1:
			self.displayString[1] += weatherStr + ' '

# SETTING HANDLING -------------------------------------------------------------------

	# This will dump the current settings to settings.txt
	def dumpSettings(self):
		# Create a settings dictionary
		settings = {
			'animationSpeed' : self.animationSpeed,		# Balls/s for animations. Needs to be a float (.0). Static default
			'textColor' : self.textColor,
			'fontName' : self.fontName,
			'textSpacing' : self.textSpacing,
			'customText' : self.customText,
			'weatherZipLocation' : self.weatherZipLocation,
			'weatherCityLocation' : self.weatherCityLocation,
			'tempUnits' : self.tempUnits,
			'content' : self.content,
			'bgColor' : self.bgColor,
			'brightness' : self.brightness,
			'timeFormat' : self.timeFormat,
			'boardType'  : self.boardType,
			'lineCount'  : self.lineCount
		}

		# Dump the settings to settings.txt
		with open('/home/pi/ledppbc/code/settings.txt', 'w') as filehandle:
			json.dump(settings, filehandle)

	# This will load the settings from settings.txt
	def loadSettings(self,bootup=True):
		# Get the settings dictionary from settings.txt
		with open('/home/pi/ledppbc/code/settings.txt', 'r') as filehandle:
			settings = json.load(filehandle)

		# Get the API keys from apikeys.txt
		with open('/home/pi/ledppbc/code/apikeys.txt', 'r') as filehandle:
			apikeys = json.load(filehandle)
		
		# Set the API Key variables
		self.openWeatherKey = apikeys['openweather']

		# Set variables from the settings 
		self.animationSpeed = settings['animationSpeed']									 # Balls/s for animations. Needs to be a float (.0). Static default
		self.textColor = settings['textColor']
		self.fontName = settings['fontName']
		self.textSpacing = settings['textSpacing']
		self.customText = settings['customText']
		self.weatherZipLocation = settings['weatherZipLocation']
		self.weatherCityLocation = settings['weatherCityLocation']
		self.tempUnits = settings['tempUnits']
		self.content = settings['content']
		self.bgColor = settings['bgColor']
		self.brightness = settings['brightness']
		self.timeFormat = settings['timeFormat']
		self.boardType = settings['boardType']
		self.lineCount = settings['lineCount']

		# Since we have loaded new settings, assume the displays have changed
		self.bgDisplayChanged = True
		self.WingsDisplayChanged = True
		self.AccentDisplayChanged = True
		self.updateWeather = True

		# Establish the text origin list with spaces for 2 lines
		self.textOrigin = [0,0]

		# Address possible different settings based on the board type
		if self.boardType == 'normal':
			self.textOrigin[0] = [1,1]		#[line #][x,y]
		elif self.boardType == 'xl':
			self.num_balls = 257				# Number of balls on your board #CHANGED FOR XL
			self.num_rows = 13				# How many rows of balls are on your board #CHANGED FOR XL
			self.num_cols = 23				# How many effective columns are on your board. This is equal to your widest row. #CHANGED FOR XL

			if self.lineCount == 1:
				self.textOrigin[0] = [2,4]
			elif self.lineCount == 2:
				self.textOrigin[0] = [4,1]
				self.textOrigin[1] = [1,7]

		# Calculate the LED count
		self.led_count = self.num_balls * PIXEL_RATIO

		# Address possible font change
		if self.fontName == 'slanted':
			self.font = slanted
		elif self.fontName == 'digits':
			self.font = digits

		# Fix unicode content list
		for i in range(len(self.content)):
			self.content[i] = str(self.content[i])

		# Set brightness if we are not in bootup
		if bootup == False:
			self.strip.setBrightness(self.brightness)

# Initialize an instance of the LEDStrip class
PPB = PingPongBoard()

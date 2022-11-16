import os
import sys

from flask import Flask, render_template, request
from LEDUtils import *
from Utils import *

#Setup the flask object and get it going
app = Flask(__name__)

# Flask Index
@app.route("/", methods=['GET'])
def index():
	return render_template('index.html')

# Flask BG Color API
@app.route("/api/bgcolor", methods=['POST'])
def setBGColor():
	# Read the values from the POST
	program = request.form['color']
	red = int(request.form['red'])
	green = int(request.form['green'])
	blue = int(request.form['blue'])
	
	PPB.bgDisplayChanged = True
	# Change the bg color accordingly
	if program == "solid":
		PPB.bgColor = ["solid", Color(red,green,blue)]
	else:
		PPB.bgColor = ["animation", program]
	return ""

# Flask Text Color API
@app.route("/api/wingscolor", methods=['POST'])
def setWingsColor():
	# Read the values from the POST
	program = request.form['color']
	red = int(request.form['red'])
	green = int(request.form['green'])
	blue = int(request.form['blue'])
	
	PPB.wingsDisplayChanged = True
	# Change the bg color accordingly
	if program == "solid":
		PPB.wingsColor = ["solid", Color(red,green,blue)]
	else:
		PPB.wingsColor = ["animation", program]
	return ""

@app.route("/api/accentcolor", methods=['POST'])
def setAccentColor():
	# Read the values from the POST
	program = request.form['color']
	red = int(request.form['red'])
	green = int(request.form['green'])
	blue = int(request.form['blue'])
	
	PPB.accentDisplayChanged = True
	# Change the bg color accordingly
	if program == "solid":
		PPB.accentColor = ["solid", Color(red,green,blue)]
	else:
		PPB.accentColor = ["animation", program]
	return ""

# Flask Font API
@app.route("/api/font", methods=['POST'])
def setFont():
	# Read the values from the POST
	font = request.form['font']
	
	# Assign the font variable in LED class
	if font == "slanted":
		PPB.font = slanted
	elif font == "digits":
		PPB.font = digits

	PPB.fontName = font
	PPB.fontChanged = True
	PPB.updateDisplayString()

	return ""


# Flask Select Content API
@app.route("/api/setcontent", methods=['POST'])
def setContent():
	# Read the values from the POST
	content = str(request.form['content'])
	lineNum = str(request.form['lineNum'])
	checked = str(request.form['checked'])

	contentChunk = content + ' ' + lineNum

	if checked == 'true' and (contentChunk in PPB.content) == False:
		PPB.content.append(contentChunk)
	elif checked == 'false' and (contentChunk in PPB.content) == True:
		PPB.content.remove(contentChunk)

	print (PPB.content)
	PPB.wingsStateWipe()
	PPB.accentStateWipe()
	return ""

# Flask Settings API
@app.route("/api/settings", methods=['POST'])
def updateSettings():
	# Read the values from the POST
	action = str(request.form['action'])

	if action == 'save':
		PPB.dumpSettings()
	elif action == 'load':
		PPB.loadSettings(False)

	return ""

# Flask Set Brightness API
@app.route("/api/brightness", methods=['POST'])
def setBrightness():
	# Read the values from the POST
	brightness = int(request.form['brightness'])

	PPB.strip.setBrightness(brightness)

	return ""

# Flask Web PageSettings API
@app.route("/api/webpagesettings", methods=['GET','POST'])
def updateWebPageSettings():
	if request.method == 'GET':
		# Get the web page settings from webpagesettings.txt
		with open('/home/pi/butterflyLED/code/webpagesettings.txt', 'r') as filehandle:
			return filehandle.read()
	
	elif request.method == 'POST':
		settings = str(request.form['settings'])
		# Write the settings to webpagesettings.txt
		with open('/home/pi/butterflyLED/code/webpagesettings.txt', 'w') as filehandle:
			filehandle.write(settings)
		return ""

# Board Type API
@app.route("/api/boardtype", methods=['POST'])
def setBoardType():
	# Read the values from the POST
	boardType = str(request.form['boardType'])

	if boardType == 'normal':
		PPB.lineCount = 1

	# Change the board type and save the settings
	PPB.boardType = boardType
	PPB.dumpSettings()

	return ""

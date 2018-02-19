#!/usr/bin/python

import evdev
import uinput
import sys
import signal
import os
import time
import threading
import RPi.GPIO as GPIO
from evdev import UInput, ecodes as e

# Set pinmode on Broadcom SOC.
GPIO.setmode(GPIO.BCM)
# disable warnings
GPIO.setwarnings(False)
# Set output led left controller connected
GPIO.setup(26, GPIO.OUT)
# Set output led right controller connected
GPIO.setup(16, GPIO.OUT)

# arguments L for left R for right controller
argument = sys.argv[1:]

chkcontroller = 0

if argument == ['L']:
	chkcontroller = 1
if argument == ['R']:
	chkcontroller = 2

# Mac addresses bluetooth joy-con controllers
# addresses copied out of emulationmachine
JoyConMacL = "04:03:D6:BD:B6:28"
JoyConMacR = "04:03:D6:BC:B7:FF"

# when program interrupts goto here and exit program
def signal_handler(signal, frame):
	print
	print("Program interrupted")
	if chkcontroller == 1:
		# Reset LED
		GPIO.output(26, 0)
	if chkcontroller == 2:
		# Reset LED
		GPIO.output(16, 0)
	GPIO.cleanup()
	os.system('kill $PPID')

# Main program
def main():

	def Idle():
		if connected == True:
			# Ping to keep connection of joy-cons alive...
			# this is a dirty trick outerwise controllers disconnect to early
			# when not in use
			if chkcontroller==1:
				joymacL = "l2ping -c 1 " + JoyConMacL
				response = os.system(joymacL)
			if chkcontroller==2:
				joymacR = "l2ping -c 1 " + JoyConMacR
				response = os.system(joymacR)
		time.sleep(1.0)
		Idle()

	t = threading.Timer(1.0, Idle)
	t.start()

	signal.signal(signal.SIGINT, signal_handler)
	# joy-con bluetooth id codes controller
	JL_BUTTON_UP = 306
	JL_BUTTON_DOWN = 305
	JL_BUTTON_LEFT = 304
	JL_BUTTON_RIGHT = 307
	JL_BUTTON_SELECT = 317
	JL_BUTTON_MINUS = 312
	JL_BUTTON_L1 = 318
	JL_BUTTON_L2 = 319
	JL_BUTTON_TUMB = 314

	JL_STICK_UP = 16
	JL_STICK_DOWN = 16
	JL_STICK_LEFT = 17
	JL_STICK_RIGHT = 17

	JR_BUTTON_A = 304
	JR_BUTTON_X = 305
	JR_BUTTON_B = 306
	JR_BUTTON_Y = 307
	JR_BUTTON_START = 316
	JR_BUTTON_PLUS = 313
	JR_BUTTON_R1 = 318
	JR_BUTTON_R2 = 319
	JR_BUTTON_TUMB = 315

	JR_STICK_UP = 16
	JR_STICK_DOWN = 16
	JR_STICK_LEFT = 17
	JR_STICK_RIGHT = 17

	# sub set/reset virtual key
	def handle_button(ev, keystroke):

		#print "TYPE:" + str(event.type)
		#print "CODE:" + str(event.code)
		#print "VALUE:" + str(event.value)

		# DIGITAL
		# SET KEY
		if event.type == 1 and event.code == ev and event.value == 1:
			ui.write(e.EV_KEY, keystroke, 1)
			ui.syn()
		# RELEASE KEY
		if event.type == 1 and event.code == ev and event.value == 0:
			ui.write(e.EV_KEY, keystroke, 0)
			ui.syn()

	def handle_stick(ev1, ev2, keystroke1, keystroke2):
		# ANALOG
		# SET KEY SIDE 1
		if event.type == 3 and event.code == ev1 and event.value == 1:
			ui.write(e.EV_KEY, keystroke1, 1)
			ui.syn()
		# SET KEY SIDE 2
		if event.type == 3 and event.code == ev2 and event.value == -1:
			ui.write(e.EV_KEY, keystroke2, 1)
			ui.syn()
		# RELEASE SIDES 1,2
		if event.type == 3 and (event.code == ev1 or event.code == ev2) and event.value == 0:
			ui.write(e.EV_KEY, keystroke1, 0)
			ui.write(e.EV_KEY, keystroke2, 0)
			ui.syn()

	# Search for joy-con device
	print ("JoyCon program startup")
	print
	print("Finding Joy-con controller...")

	connected = False
	notfound = False
	try:
		while not connected:
			devices = devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
			for device in devices:
				#print device.name
				#if device.name == "Nintendo Gamepad":
				if device.name == "Joy-Con (L)" and chkcontroller==1:
					#print device.info.product
					# print device.info.bustype
					#if device.info.product == 8198 and chkcontroller==1:
					print 'Joy-con left found'
					joycondevL = device.fn
					print device.info
					gamepadL = evdev.InputDevice(joycondevL)
					connected = True
					# Set LED left controller connected
					GPIO.output(26, 1)
				if device.name == "Joy-Con (R)" and chkcontroller==2:
					#if device.info.product == 8199 and chkcontroller==2:
					print 'Joy-con right found'
					joycondevR = device.fn
					print device.info
					gamepadR = evdev.InputDevice(joycondevR)
					connected = True
					# Set LED right controller connected
					GPIO.output(16, 1)

		#time.sleep(1)
	except NameError:
		if not notfound:
			print "Nothing found. <polling>"
			notfound = True
			pass
	except KeyboardInterrupt:
		t.cancel()

	print 'Connected!'

	""" Devices for keystrokes """
	device = uinput.Device([uinput.KEY_E])
	ui = UInput()

	# reading input from selected controller
	# Left controller
	if chkcontroller == 1:
		while True:
			try:
				for event in gamepadL.read_loop():   #this loops infinitely

					time.sleep(0.02)
					# Left controller
					handle_button(JL_BUTTON_UP,e.KEY_UP)
					handle_button(JL_BUTTON_DOWN,e.KEY_DOWN)
					handle_button(JL_BUTTON_LEFT,e.KEY_LEFT)
					handle_button(JL_BUTTON_RIGHT,e.KEY_RIGHT)
					handle_button(JL_BUTTON_SELECT,e.KEY_LEFTALT)
					handle_button(JL_BUTTON_MINUS,e.KEY_1)
					handle_button(JL_BUTTON_L1, e.KEY_O)
					handle_button(JL_BUTTON_L2, e.KEY_P)
					handle_button(JL_BUTTON_TUMB, e.KEY_M)

					handle_stick(JL_STICK_UP, JL_STICK_DOWN, e.KEY_3, e.KEY_4)
					handle_stick(JL_STICK_LEFT, JL_STICK_RIGHT, e.KEY_5, e.KEY_6)

			except IOError:
				print "Connection lost"
				connected = False
				# Reset LED left controller disconnected
				GPIO.output(26, 0)
				main()
			except KeyboardInterrupt:
				t.cancel()

	# reading input from selected controller
	# Right controller
	if chkcontroller==2:
		while True:
			try:
				for event in gamepadR.read_loop():  # this loops infinitely

					time.sleep(0.02)
					# Right controller
					handle_button(JR_BUTTON_A, e.KEY_Q)
					handle_button(JR_BUTTON_B, e.KEY_B)
					handle_button(JR_BUTTON_X, e.KEY_X)
					handle_button(JR_BUTTON_Y, e.KEY_Y)
					handle_button(JR_BUTTON_START,e.KEY_RIGHTALT)
					handle_button(JR_BUTTON_PLUS,e.KEY_ESC)
					handle_button(JR_BUTTON_R1, e.KEY_U)
					handle_button(JR_BUTTON_R2, e.KEY_I)
					handle_button(JR_BUTTON_TUMB, e.KEY_N)

					handle_stick(JR_STICK_UP, JR_STICK_DOWN, e.KEY_7, e.KEY_8)
					handle_stick(JR_STICK_LEFT, JR_STICK_RIGHT, e.KEY_9, e.KEY_0)

			except IOError:
				print "Connection lost"
				connected = False
				# Reset LED right controller disconnected
				GPIO.output(16, 0)
				main()
			except KeyboardInterrupt:
				t.cancel()

main()

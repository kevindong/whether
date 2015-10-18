import requests # For easy API access
import json # For json file parsing
import os # For turning LED lights on/off and initialization
import time # For forcing the program to sleep

os.system("gpio mode 0 out") # Initializes the LED lights for use
os.system("gpio mode 1 out")
os.system("gpio mode 2 out")

while True: # This program is intended to be an infinite loop.
	os.system("gpio write 0 0") # Ensures that the lights are off to start out; precipitation
	os.system("gpio write 1 0") # Sweater sweater
	os.system("gpio write 2 0") # Status
	
	# =================
	# Getting location
	# =================
	inputtedLocation = open('location.txt', 'r') # Reads the desired location from file
	apiKey = open('key.txt', 'r') # Reads the API key from file
	location = "http://api.wunderground.com/api/" + apiKey.readline() + "/hourly/q/" + inputtedLocation.readline() + ".json" # Concantenates the request URL
	inputtedLocation.close() # Closes both files
	apiKey.close()
	
	# =================
	# Grabbing data
	# =================
	print("Opening file to be written to...")
	original = open('West_Lafayette.json', 'w') # Opens the file for writing
	print("Accessing .json file...")
	page = requests.get(location) # Grabs .json file
	print("Writing .json file to disk...")
	original.write(page.text) # Writes downloaded .json file to disk
	print("Closing file that got written to...")
	original.close() # Closes the file

	# =================
	# Times of interest
	# =================
	schedule = open('schedule.txt', 'r') # Reads the user's schedule from file
	schedule_list = [] # Establishes empty list for storing schedule
	for i in (range(0,7)): # Iterates through the first 7 lines of the schedule (one for each day)
		transition = schedule.readline().split() # Splits each line into elements with a space being the delimiter
		transition_two = [] # Establishes empty list for storing values in transition from string to integers
		for i in transition: # Loops through every element of a line...
			transition_two.append(int(i)) # Converts each element into an integer
		schedule_list.append(transition_two) # Stores the end result into schedule_list
	schedule.close() # Closes the file

	# =================
	# Parses data file
	# =================
	original = open('West_Lafayette.json', 'r')
	original_str = original.read()
	original.close()
	original_data = json.loads(original_str) # Parses the .json file into a dictionary

	# =================
	# Finds schedule of interest
	# =================
	# Checks .json file to see which schedule to compare against
	if (original_data["hourly_forecast"][0]["FCTTIME"]["weekday_name"] == "Monday"):
		target = 0
		target_day = "Monday"
	elif (original_data["hourly_forecast"][0]["FCTTIME"]["weekday_name"] == "Tuesday"):
		target = 1
		target_day = "Tuesday"
	elif (original_data["hourly_forecast"][0]["FCTTIME"]["weekday_name"] == "Wednesday"):
		target = 2
		target_day = "Wednesday"
	elif (original_data["hourly_forecast"][0]["FCTTIME"]["weekday_name"] == "Thursday"):
		target = 3
		target_day = "Thursday"
	elif (original_data["hourly_forecast"][0]["FCTTIME"]["weekday_name"] == "Friday"):
		target = 4
		target_day = "Friday"
	elif (original_data["hourly_forecast"][0]["FCTTIME"]["weekday_name"] == "Saturday"):
		target = 5
		target_day = "Saturday"
	elif (original_data["hourly_forecast"][0]["FCTTIME"]["weekday_name"] == "Sunday"):
		target = 6
		target_day = "Sunday"
	else:
		print("You dun goofed.")

	# ===============
	# The meat of the program
	# ===============
	modifier = int(original_data["hourly_forecast"][0]["FCTTIME"]["hour"]) # Factor by which to shift indices
	preIndicator = False # It is assumed you don't need an umbrella
	preCounter = 0 # This...
	preTotal = 0 # ...and this are used to calculate average values
	# ---------------
	# Percipitation checker
	# ---------------
	for hour in schedule_list[target]: # Loops through every hour of interest in the user's schedule
		if (modifier > hour or hour < 0 or hour > 23): # Ensures inputs are valid; 'modifier > hour' makes sure...
			pass # that hours in the past are not used in calculating whether or not to light the LED
		else:
			preTotal += int(original_data["hourly_forecast"][hour - modifier]["pop"]) # This...
			preCounter += 1 #... and this are used for calculating averages
			if (int(original_data["hourly_forecast"][hour - modifier]["pop"]) >= 30): # If any hour has a greater than...
				preIndicator = True # 30% chance of raining, indicator is switched on
				break
	if (preCounter == 0): # Catches an edge case where the following elif would throw an exception due to division by 0.
		pass
	elif (preTotal/preCounter >= 15): # If the average chance of precipitation over the course of the day is >= 15%, indicator...
		preIndicator = True # is flipped on
	# ---------------
	# Temperature checker
	# ---------------
	tempIndicator = False # It is assumed that you don't need a sweater
	tempCounter = 0 # This...
	tempTotal = 0 # ...and this are used to calculate average values
	for hour in schedule_list[target]: # Loops through every hour of interest in the user's schedule
		if (modifier > hour or hour < 0 or hour > 23): # Ensures inputs are valid; 'modifier > hour' makes sure...
			pass # that hours in the past are not used in calculating whether or not to light the LED
		else:
			tempTotal += int(original_data["hourly_forecast"][hour - modifier]["feelslike"]["english"]) # This...
			tempCounter += 1 # ...and this are used for calculating averages
			if (int(original_data["hourly_forecast"][hour - modifier]["feelslike"]["english"]) <= 50): # If any hour has a...
				tempIndicator = True # ..."feels like" temp of <= 50 degrees, indicator is switched on
				break
	if (tempCounter == 0): # Catches an edge case where the following elif would throw an exception due to division by 0.
		pass
	elif (tempTotal/tempCounter <= 50): # if the average 'feels like' temperature over the course of the day is <= 50 degrees...
		tempIndicator = True # ...the indicator will be flipped on.
	if (preIndicator == True): # Checks to see if the umbrella notification light needs to be turned on
		print("preIndicator invoked")
		os.system("gpio write 0 1") # Turns light on
	if (tempIndicator == True): # Checks to see if the sweather weather notification light needs to be turned on
		print("tempIndicator invoked")
		os.system("gpio write 1 1") # Turns light on
	if (preIndicator == False and tempIndicator == False): # If neither of the other two lights are on, this status light comes on.
		os.system("gpio write 2 1") # Turns light on
	print("\nPowered by Weather Underground.")
	time.sleep(3600) # Sleeps for 3,600 seconds (= 1 hour) and then reruns the entire program
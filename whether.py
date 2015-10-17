import requests
import json
import os
import time

os.system("gpio mode 0 out")
os.system("gpio mode 1 out")

while True:
	os.system("gpio write 0 0")
	os.system("gpio write 1 0")
	
	# =================
	# Getting location
	# =================
	inputtedLocation = open('location.txt', 'r')
	location = "http://api.wunderground.com/api/eacd09822c4fab15/hourly/q/" + inputtedLocation.readline() + ".json"
	inputtedLocation.close()
	
	# =================
	# Grabbing data
	# =================
	print("Opening file to be written to...")
	original = open('West_Lafayette.json', 'w')
	print("Accessing .json file...")
	page = requests.get(location) # Grabs webpage
	print("Writing .json file to disk...")
	original.write(page.text)
	print(page.text)
	print("Closing file that got written to...")
	original.close()

	# =================
	# Times of interest
	# =================
	schedule = open('schedule.txt', 'r')
	schedule_list = []
	for i in (range(0,7)):
		transition = schedule.readline().split()
		transition_two = []
		for i in transition:
			transition_two.append(int(i))
		schedule_list.append(transition_two)
	#print(schedule_list)
	schedule.close()

	# =================
	# Parses data file
	# =================
	original = open('West_Lafayette.json', 'r')
	original_str = original.read()
	original.close()
	original_data = json.loads(original_str)
	for i in range(0,10):
		if (int(original_data["hourly_forecast"][i]["pop"]) >= 10):
			#print("rain")
			broken = True
			break
	#if (broken == True):
	#	print("")
	
	#print(json.loads(original_str)[0])

	# =================
	# Finds schedule of interest
	# =================
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
	modifier = int(original_data["hourly_forecast"][0]["FCTTIME"]["hour"])
	#print modifier
	preIndicator = False
	counter = 0
	total = 0
	for hour in schedule_list[target]: # precipitation
		print("PRECIPITATION")
		print("hour: " + str(hour))
		print("modifier: " + str(modifier))
		print("accessed index: " + str(hour - modifier))
		print("pop: " + original_data["hourly_forecast"][hour - modifier]["pop"])
		if (modifier > hour or hour < 0 or hour > 23):
			pass
		else:
			total += int(original_data["hourly_forecast"][hour - modifier]["pop"])
			counter += 1
			if (int(original_data["hourly_forecast"][hour - modifier]["pop"]) >= 30):
				#print("rain")
				preIndicator = True
				break
		print("\n")
	if (counter == 0):
		pass
	elif (total/counter >= 15):
		preIndicator = True
	counter = 0
	total = 0
	tempIndicator = False
	for hour in schedule_list[target]: # temperature
		print("TEMPERATURE")
		print("hour: " + str(hour))
		print("modifier: " + str(modifier))
		print("accessed index: " + str(hour - modifier))
		print("feelslike [english]: " + original_data["hourly_forecast"][hour - modifier]["feelslike"]["english"])
		if (modifier > hour or hour < 0 or hour > 23):
			pass
		else:
			total += int(original_data["hourly_forecast"][hour - modifier]["feelslike"]["english"])
			counter += 1
			if (int(original_data["hourly_forecast"][hour - modifier]["feelslike"]["english"]) >= 50):
				tempIndicator = True
				break
		print("\n")
	if (counter == 0):
		pass
	elif (total/counter >= 15):
		tempIndicator = True
	if (preIndicator == True):
		print("preIndicator invoked")
		print("")
		os.system("gpio write 0 1")
	if (tempIndicator == True):
		print("tempIndicator invoked")
		print("")
		os.system("gpio write 1 1")
	#time.sleep(3600)
	break
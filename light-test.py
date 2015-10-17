import os

os.system("gpio mode 0 out")
os.system("gpio mode 1 out")

while True:
	os.system("gpio write 0 1")
	os.system("gpio write 1 1")
	time.sleep(0.25)
	os.system("gpio write 0 0")
	os.system("gpio write 1 0")
	time.sleep(0.25)
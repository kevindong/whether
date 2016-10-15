# Whether

### Description
This project uses a Raspberry Pi, two LED lights, and a breadboard. 

Most weather apps will give you pretty much everything you need to know about today's weather. But, they also overload you with information. You don't actually care if it rains when you're not outside. Most people are only going to care about the weather when they're outside (for white collar workers, this would be something like 8-9am and 5-6pm). This program simply takes in your schedule and location and compares it against the weather data for the current day. If you indicate that you're going to be outside at a certain time and it's reasonably likely that it'll rain at that time, the umbrella indicator light will come on. Likewise, there's a sweater weather light.

### Instructions

1. Please note that you must generate your own API key from [Weather Underground](http://www.wunderground.com/weather/api/). Place a file called `key.txt` into the same directory as `whether.py`. In that file, place your API key on the very first line and nothing else. Do not leave a space after the key.
2. In `location.txt`, you must indicate the city where you would like the weather information to be based upon. You must follow the format of `<capitalized 2 letter abbreviation of the state>/<city name>`. If there are spaces in the city name, use underscores (`_`) in their place.
3. In `schedule.txt`, place the hours you wish to be referenced. Line 1 is Monday, line 2 is Tuesday, etc. Separate each hour with a space. If you are not interested in a day, place a `0` in that line. Take the following as an example. On Monday, the user is interested in the weather between 12pm and 5pm (inclusive). On Sunday, the user is interested in the weather at 6pm only. 

```
12 13 14 15 16 17
10 11 13 14 15
0
1 2 3 4 5 9 15 18 19
20 21 22
11 12 13 16 18
18
```

### Included Examples/Tests
This repository includes West Lafayette, IN as an example. It is safe to edit every file in this repository except for `whether.py`. `light-test.py` checks to make sure that Python programs can actually turn the lights on and off.

----------

### Credits
All data is sourced from [Weather Underground](http://www.wunderground.com). Powered by Weather Underground. 

### License
All rights reserved.

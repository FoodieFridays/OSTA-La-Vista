# OSTA-La-Vista
[OSTA](http://www.ottawaschoolbus.ca/) web scraper, for checking the status of school buses in Ottawa

## Getting Started
1. Using a Raspberry Pi, download Python 3 and your IDE of choice. 
2. From this repository, download `OSTA_La_Vista.py` for the most up-to-date version of the program. `temp_alarm_sound.mp3` is also needed for the alarm sound
3. Ensure you have the required external libraries downloaded using `pip`. Namely:
   - `requests`
   - `bs4`
   - `gtts`
   - `RPi.GPIO`
   - `smtplib`
   - `tkinter`
   - `mpg321` (command line audio file player)
5. Hook up green, yellow, and red LEDs to GPIO ports 18, 19, and 20, respectively.
6. Run the Python file, and things should work as planned.
   - Recommended: see the following [explanation slideshow](https://docs.google.com/presentation/d/1XV7Bb-6rav0R7EuzITrXO-rq_EEMCxDK4tkTRmWyCxw/edit?usp=sharing) to understand exactly what this program is capable of!

**Important Note:** You may think that the email password in the `.py` file will give you access to my entire Google account. This is an incorrect assumption:
- This password is what's known as an "App Password", that can only be used for the sole purpose of sending emails via a script.
- 2-Factor Authentication has been set up for this account.
- This account is worthless anyways; it has only been set up to work as a "bus bot" emailing system.

## Licence
This project is free and open-source, so long that it is not used for commercial purposes [(CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/).

SOFTWARE IS PROVIDED “AS-IS”, WITHOUT A WARRANTY OF ANY KIND.

## About
This project was only made as part of my high school CS class; it is by no means a comprehensive program, nor was it intended to be.
If you experience issues, that's expected. This program is not yet bullet-proof!

## Support
Should you run into any issues while using this program, please feel free to start and "Issues Thread" or contact me. I'm always happy to help, but you probably know more than I do :)

## Features Coming in v2.0
This program is just the very beginning. I still have lots of ideas for how I want to expand this project, inlcuded, but not limited to, the following:
- Extra support for Windows PCs
- An enhanced alarm scheduling system
- Added error-trapping
- SMS alerts, in addition to emails already
- A dedicated user support email

See my [explanation slideshow](https://docs.google.com/presentation/d/1XV7Bb-6rav0R7EuzITrXO-rq_EEMCxDK4tkTRmWyCxw/edit?usp=sharing) for more in-depth ideas for the future.

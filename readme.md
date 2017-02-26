Weather
=======
An all-in-one tool to get the weather!
Prints an ANSII weather report.

Installation
------------
None!  Just get the script and run with Python 3.

Requirements
------------
- Python 3+
- ANSII support

How to Use
----------
Run `weather` to get the weather in your zip code (checks ipinfo.io for your zip code)

Run `weather <location>` to get the weather at the given location (can be zip code/city/IATA code/whatever wttr.in likes)

Use the `-l / --lang` flag to pass a language code (e.g., "en", "it"). Only changes the report, and must be supported by wttr.in. Default is "en".

Sources
-------
This tool uses [wttr.in](http://wttr.in) for weather reports, and [ipinfo.io](http://ipinfo.io) to find zip codes.

Weather
=======
Dumb wrapper around [wttr.in](http://wttr.in).
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
Run `weather` to get the weather in your zip code (wherever wttr.in thinks you are).

Run `weather <location>` to get the weather at the given location (can be zip code/city/IATA code/whatever wttr.in likes)

Use the `-l / --lang` flag to pass a language code (e.g., "en", "it"). Only changes the report, and must be supported by wttr.in. Default is "en".

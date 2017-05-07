#!/usr/local/bin/python3

"""
An all-in-one tool to get the weather!
"""

import argparse
import json
import sys
import urllib.request


URL_LOCATION_BASE = "ipinfodb.com"
URL_LOCATION = f"http://{URL_LOCATION_BASE}/ip_locator.php"
URL_WEATHER_BASE = "wttr.in"
URL_WEATHER_FORM = f"http://{URL_WEATHER_BASE}/{{}}?lang={{}}"
DEFAULT_LANG = "en"
CURL_HEADER = {
    'User-Agent': 'curl/7.43.0',
}


def get_location_by_ip():
    req = urllib.request.Request(
        URL_LOCATION,
        data=None,
        headers=CURL_HEADER,
    )

    resp = urllib.request.urlopen(req)
    data = resp.read().decode('utf-8')

    city = data.split("<li>City : ")[1].split("</li>")[0]
    region = data.split("<li>State/Province : ")[1].split("</li>")[0]
    country = data.split("<li>Country : ")[1].split(" <")[0]

    return f"{city}, {region}, {country}"


def try_to_guarantee_location(location):
    if location:
        print(f"[+] Location provided: {location}")
        return location

    print("[ ] No location provided, finding location by IP...")
    try:
        location = get_location_by_ip()
        if location:
            print(f"[+] Got location: {location}")
            return location
        else:
            print(f"[-] Got bad location info from {URL_LOCATION_BASE}")
    except urllib.error:
        print(f"[!] Couldn't reach {URL_LOCATION_BASE}")

    print(f"[ ] Trying {URL_WEATHER_BASE} default...")
    return location


def get_weather_by_location(location, language, full):
    url = URL_WEATHER_FORM.format(location, language) + ("" if full else "&n&1")
    full_msg = "full" if full else "today's"
    location_msg = f" for {location}" if location else ""
    print(f'\n[ ] Getting {full_msg} weather report{location_msg}...')
    print(f'    ("{url}")\n')

    req = urllib.request.Request(
        url,
        data=None,
        headers=CURL_HEADER,
    )
    resp = urllib.request.urlopen(req)
    report = resp.read().decode('utf-8')
    return report


def parse_args():
    parser = argparse.ArgumentParser(
        description="Prints a weather report for the given location. Does a reverse-lookup on your IP if no location provided."
    )
    parser.add_argument("location", help="Zip code, city, etc. (optional)", nargs="?")
    parser.add_argument("-f", "--full", help="Show the full weather report (exceeds 80x24)", default=False, action="store_true")
    parser.add_argument("-l", "--lang", help="The weather report langauge", default=DEFAULT_LANG)
    return parser.parse_args()


def main():
    args = parse_args()
    location = try_to_guarantee_location(args.location)
    print(get_weather_by_location(location, args.lang, args.full))


if __name__ == '__main__':
    main()

#!/usr/local/bin/python3

"""
An all-in-one tool to get the weather!
"""

import argparse
import json
import sys
import urllib.request


URL_WEATHER_FORM = "http://wttr.in/{}?lang={}"

DEFAULT_LANG = "en"

CURL_HEADER = {
    'User-Agent': 'curl/7.43.0',
}


def get_zipcode_by_ip():
    req = urllib.request.Request(
        URL_ZIPCODE,
        data=None,
        headers=CURL_HEADER,
    )

    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    return data['postal']


def is_valid_zipcode(zipcode):
    return zipcode.isdigit() and len(zipcode) == 5


def get_weather_by_location(location, language):
    url = URL_WEATHER_FORM.format(location, language)
    print("[ ] Getting weather for {}... ({})".format(location, url))

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
        description="Prints a weather report for the given location. Uses your zip code if no location provided."
    )
    parser.add_argument("location", help="Zip code or city (optional)", nargs="?")
    parser.add_argument("-l", "--lang", help="The weather report langauge", default=DEFAULT_LANG)
    return parser.parse_args()


def main():
    args = parse_args()
    location = args.location if args.location else ''
    print(get_weather_by_location(location, args.lang))


if __name__ == '__main__':
    main()

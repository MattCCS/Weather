#!/usr/local/bin/python3

"""
An all-in-one tool to get the weather!
"""

import argparse
import json
import sys
import urllib.request


URL_ZIPCODE = "http://ipinfo.io"
URL_WEATHER_FORM = "http://wttr.in/{}"

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


def get_location():
    args = parse_args()
    location = args.location

    # default behavior is to find zip code
    if not location:
        print("[ ] No location provided, finding zip code...")
        zipcode = get_zipcode_by_ip()
        if not is_valid_zipcode(zipcode):
            print("[!] Got bad zip code from ipinfo.io: {}".format(zipcode))
            sys.exit()
        print("[+] Got zip code: {}".format(zipcode))
        location = zipcode

    # can be zipcode or city name, wttr.io don't care!
    return location


def is_valid_zipcode(zipcode):
    return zipcode.isdigit() and len(zipcode) == 5


def get_weather_by_location(location):
    print("[ ] Getting weather for {}...".format(location))
    req = urllib.request.Request(
        URL_WEATHER_FORM.format(location),
        data=None,
        headers=CURL_HEADER,
    )
    resp = urllib.request.urlopen(req)
    report = resp.read().decode('utf-8')
    return report


def parse_args():
    parser = argparse.ArgumentParser(
        description="Prints a weather report for the given location.  Uses your zip code if no location provided."
    )
    parser.add_argument("location", help="Zip code or city (optional)", nargs="?")
    return parser.parse_args()


def main():
    location = get_location()
    print(get_weather_by_location(location))


if __name__ == '__main__':
    main()
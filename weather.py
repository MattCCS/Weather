#!/usr/local/bin/python3

"""
An all-in-one tool to get the weather!
"""

import argparse
import urllib.parse
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

    city = data.split("<strong>City</strong>")[1].split("<div>")[0].split("</div>")[1].strip()
    region = data.split("<strong>Region</strong>")[1].split("</td>")[0].split("</div>")[1].strip()
    country = data.split("<strong>Country</strong>")[1].split("</td>")[0].split("</span>")[1].strip()

    # The tilde tells wttr.in to search for the
    # location name, which tends to resolve name errors.
    return f"~{city}, {region}, {country}"


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
    except urllib.error.HTTPError:
        print(f"[!] Couldn't reach {URL_LOCATION_BASE}")

    print(f"[ ] Trying {URL_WEATHER_BASE} default...")
    return location


def get_weather_by_location(location, language, full):
    location = urllib.parse.quote_plus(location)
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
    parser.add_argument("location", help="Zip code, city, etc. (optional)", nargs="*")
    parser.add_argument("-f", "--full", help="Show the full weather report (exceeds 80x24)", default=False, action="store_true")
    parser.add_argument("-l", "--lang", help="The weather report langauge (en, es, ...)", default=DEFAULT_LANG)
    parser.add_argument("-p", "--place", help="Treat the location as a place name (passes '~' to wttr.in)", default=False, action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    location = try_to_guarantee_location(" ".join(args.location))
    if args.place and not location.startswith("~"):
        location = "~" + location
    print(get_weather_by_location(location, args.lang, args.full))


if __name__ == '__main__':
    main()

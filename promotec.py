import os
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

URL = "https://client.somee.com/"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36"
VIEWSTATE_GENERATOR = "CA0B0334"


def get_lockers_state():
    payload = {
        "__EVENTTARGET": "__Page",
        "__EVENTARGUMENT": "PBArg",
        "__VIEWSTATE": os.getenv("VIEWSTATE_LOCKERS"),
        "__VIEWSTATEGENERATOR": VIEWSTATE_GENERATOR,
        "__EVENTVALIDATION": os.getenv("EVENTVALIDATION_LOCKERS"),
    }
    headers = {
        "user-agent": USER_AGENT,
        "Cookie": f"ASP.NET_SessionId={os.getenv('SESSIONID_LOCKERS')}; UserInfo=Name={os.getenv('USER')}",
    }

    response = requests.request("POST", URL, headers=headers, data=payload, timeout=10)

    html_content = response.text

    soup = BeautifulSoup(html_content, "html.parser")

    locker_buttons = soup.find_all("input", class_="BtnSpecificLocker")

    lockers = {}

    for btn in locker_buttons:
        locker_number = btn.get("value")
        style_attr = btn.get("style", "")

        color_match = re.search(r"background-color:\s*([^;]+)", style_attr)
        color = color_match.group(1) if color_match else "Unknown"

        lockers[locker_number] = color == "Green"

    return lockers


def get_lockers_amount():
    payload = {
        "__VIEWSTATE": os.getenv("VIEWSTATE_AMOUNT"),
        "__VIEWSTATEGENERATOR": VIEWSTATE_GENERATOR,
        "__EVENTVALIDATION": os.getenv("EVENTVALIDATION_AMOUNT"),
        "monthList": f"{datetime.now():%m/%Y}",
        "BtnGetCounterRecords": "Get Incoming",
    }
    headers = {
        "user-agent": USER_AGENT,
        "Cookie": f"ASP.NET_SessionId={os.getenv('SESSIONID_AMOUNT')}; UserInfo=Name={os.getenv('USER')}",
    }

    response = requests.request("POST", URL, headers=headers, data=payload, timeout=10)

    html_content = response.text

    soup = BeautifulSoup(html_content, "html.parser")

    incoming_input = soup.find("input", id="TxtIncomming")
    if not incoming_input:
        return None

    incoming_value = incoming_input.get("value")
    incoming_float = float(incoming_value)

    return incoming_float

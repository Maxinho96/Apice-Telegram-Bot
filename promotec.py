import os
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

URL = "https://client.somee.com/"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36"


def authenticate(session: requests.Session):
    response = session.post(URL, timeout=10)

    user_payload = {
        **get_tokens(response.text),
        "txtUserName": os.getenv("USER"),
        "btnSelecUser": "Select",
    }
    user_response = session.post(URL, data=user_payload, timeout=10)

    password_payload = {
        **get_tokens(user_response.text),
        "txtSysPsw": os.getenv("PASSWORD"),
        "btnSelectSystem_2": "Roma Prati cloud",
    }
    password_response = session.post(URL, data=password_payload, timeout=10)

    return get_tokens(password_response.text)

def get_tokens(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    viewstate_element = soup.find("input", {"id": "__VIEWSTATE"})
    viewstate_value = viewstate_element["value"] if viewstate_element else None

    eventvalidation_element = soup.find("input", {"id": "__EVENTVALIDATION"})
    eventvalidation_value = (
        eventvalidation_element["value"] if eventvalidation_element else None
    )

    return {
        "__VIEWSTATE": viewstate_value,
        "__EVENTVALIDATION": eventvalidation_value,
    }

def get_lockers_state():
    session = requests.Session()
    tokens = authenticate(session)
    payload = {
        "__EVENTTARGET": "__Page",
        "__EVENTARGUMENT": "PBArg",
        **tokens
    }
    headers = {
        "user-agent": USER_AGENT,
    }

    response = session.post(URL, headers=headers, data=payload, timeout=10)

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
    session = requests.Session()
    tokens = authenticate(session)

    payload_counters = {
        "BtnCounters": "Counters",
        **tokens
    }
    response_counters = session.post(URL, data=payload_counters, timeout=10)
    tokens_counters = get_tokens(response_counters.text)

    payload_incomming = {
        "__EVENTTARGET": "__Page",
        "__EVENTARGUMENT": "PBArg",
        "TxtIncomming": "0",
        **tokens_counters
    }
    response_incomming = session.post(URL, data=payload_incomming, timeout=10)
    tokens_incomming = get_tokens(response_incomming.text)

    payload = {
        "monthList": f"{datetime.now():%m/%Y}",
        "BtnGetCounterRecords": "Get Incoming",
        **tokens_incomming
    }

    response = session.post(URL, data=payload, timeout=10)

    html_content = response.text

    soup = BeautifulSoup(html_content, "html.parser")

    incoming_input = soup.find("input", id="TxtIncomming")
    if not incoming_input:
        return None

    incoming_value = incoming_input.get("value")
    incoming_float = float(incoming_value)

    return incoming_float

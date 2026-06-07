import requests
import re
from bs4 import BeautifulSoup
import os


def get_lockers_state():
    url = "https://client.somee.com/"

    payload = {
        "__EVENTTARGET": "__Page",
        "__EVENTARGUMENT": "PBArg",
        "__VIEWSTATE": os.getenv("VIEWSTATE"),
        "__VIEWSTATEGENERATOR": "CA0B0334",
        "__EVENTVALIDATION": os.getenv("EVENTVALIDATION"),
    }
    files = []
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
        "Cookie": "ASP.NET_SessionId=iz4bzx2qafwb44vzxmmdxp4f; UserInfo=Name=baggy_romaprati",
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    html_content = response.text

    soup = BeautifulSoup(html_content, "html.parser")

    # Find all input tags that represent the specific lockers
    locker_buttons = soup.find_all("input", class_="BtnSpecificLocker")

    lockers = {}

    # Extract the value (number) and background color from style
    for btn in locker_buttons:
        locker_number = btn.get("value")
        style_attr = btn.get("style", "")

        # Use regex to isolate the color after 'background-color:'
        color_match = re.search(r"background-color:\s*([^;]+)", style_attr)
        color = color_match.group(1) if color_match else "Unknown"

        lockers[locker_number] = color == "Green"

    return lockers

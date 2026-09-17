#!/usr/bin/env python3
import json, urllib.request, datetime, re, pathlib

FILTER_FILE = pathlib.Path("blocklist.txt")
START = "! BEGIN REDLIB"
END = "! END REDLIB"

data = json.load(urllib.request.urlopen(
    "https://raw.githubusercontent.com/redlib-org/redlib-instances/main/instances.json"))
domains = sorted({re.sub(r"^https?://|/$", "", i["url"]) for i in data["instances"]})
domain_list = ",".join(domains)

block = [
    START,
    f"! Updated: {datetime.date.today().isoformat()}",
    f"{domain_list}##a#redlib",
    f"{domain_list}##details#feeds",
    END,
]

text = FILTER_FILE.read_text().splitlines() if FILTER_FILE.exists() else []

if START in text:
    start_idx = text.index(START)
    end_idx = text.index(END)
    text[start_idx:end_idx + 1] = block
else:
    text += [""] + block

FILTER_FILE.write_text("\n".join(text) + "\n")
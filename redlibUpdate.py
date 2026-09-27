#!/usr/bin/env python3
import json, urllib.request, datetime, re, pathlib

FILTER_FILE = pathlib.Path("blocklist.txt")
START = "! BEGIN REDLIB"
END = "! END REDLIB"

data = json.load(urllib.request.urlopen(
    "https://raw.githubusercontent.com/redlib-org/redlib-instances/main/instances.json"))

all_domains = {
    re.sub(r"^https?://|/$", "", i["url"]): i.get("description", "")
    for i in data["instances"]
    if "url" in i
}

sfw_domains = sorted(d for d, desc in all_domains.items() if re.search(r"\bsfw\b", desc, re.IGNORECASE))
other_domains = sorted(set(all_domains) - set(sfw_domains))
sfw_domain_list = ",".join(sfw_domains)

frontpage_rules = []
for d in sfw_domains:
    frontpage_rules.append(f"|https://{d}/|$document")
    frontpage_rules.append(f"|https://{d}|$document")

fullblock_rules = [f"||{d}^$document" for d in other_domains]

block = [
    START,
    f"! Updated: {datetime.date.today().isoformat()}",
    *frontpage_rules,
    *fullblock_rules,
    f"{sfw_domain_list}##a#redlib",
    f"{sfw_domain_list}##details#feeds",
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
import json
import os
import sys

from bs4 import BeautifulSoup

FASTAPI_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if FASTAPI_ROOT not in sys.path:
    sys.path.insert(0, FASTAPI_ROOT)

FIXTURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


def load_json(name):
    with open(os.path.join(FIXTURES_DIR, name), encoding="utf-8") as fh:
        return json.load(fh)


def load_html(name):
    with open(os.path.join(FIXTURES_DIR, name), encoding="utf-8") as fh:
        return BeautifulSoup(fh.read(), "html.parser")


def load_text(name):
    with open(os.path.join(FIXTURES_DIR, name), encoding="utf-8") as fh:
        return fh.read()

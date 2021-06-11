#! /usr/bin/python3

import csv
import os
import traceback
import sys
import xml.etree.ElementTree as ET
import logging
from logging.handlers import RotatingFileHandler
import datetime

from jinja2 import Environment, FileSystemLoader
import settings


def initiate_logging():
    # Initiate error logging
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    critical_fh = logging.FileHandler(settings.error_log_file)
    formatter = logging.Formatter("%(message)s")
    critical_fh.setFormatter(formatter)
    critical_fh.setLevel(logging.CRITICAL)
    log.addHandler(critical_fh)

    ch = logging.StreamHandler()
    formatter = logging.Formatter("%(message)s")
    ch.setFormatter(formatter)
    ch.setLevel(logging.DEBUG)
    log.addHandler(ch)

    normal = RotatingFileHandler(settings.log_file)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    normal.setFormatter(formatter)
    normal.setLevel(logging.INFO)
    log.addHandler(normal)

    return log


def excepthook(exctype, value, tb):
    logger.critical(
        """An unhandled error occured, please contact the developer:
    Error type : {type}
    Error value: {value}
    Traceback: {tb}""".format(
            type=exctype, value=value, tb=traceback.format_tb(tb)
        )
    )


def read_wordlist():
    try:
        with open(settings.word_list_file, "r", encoding="utf8") as csvfile:
            reader = csv.reader(csvfile)
            words = [str(w).lstrip("'[").rstrip("]'") for w in reader]
    except FileNotFoundError:
        logger.error("Word list file not found, can't highlight things in red")
        return []
    return words


def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    data = [t for t in root]

    texts = []

    for t in list(data):
        text = {}
        try:
            text["title"] = t.get("title").strip()
        except AttributeError:  # It's none
            text["title"] = ""
        for elem in t:
            try:
                text[elem.tag] = elem.text.strip()
            except AttributeError:  # It's none
                text[elem.tag] = ""

        if not text["kovol"]:  # Use the matat if no imengis is available
            if text["matat"]:
                text["kovol_interlinear"] = text["matat"].strip().split(" ")
        else:
            text["kovol_interlinear"] = text["kovol"].strip().split(" ")
        text["english_interlinear"] = text["literal"].strip().split(" ")

        texts.append(text)

    return texts


def html_it(texts, user):
    # Use a Jinja template to create the web page
    file_loader = FileSystemLoader(settings.code_folder)
    env = Environment(loader=file_loader, autoescape=True)
    template = env.get_template("text_template.j2")
    file_name = user + "_texts.html"
    html_file = os.path.join(settings.html_folder, file_name)
    with open(html_file, "w") as file:
        print(template.render(texts=texts, wordlist=wordlist), file=file)
    print("HTML created for {user}".format(user=file_name))


def create_index():
    file_loader = FileSystemLoader(settings.code_folder)
    env = Environment(loader=file_loader, autoescape=True)
    template = env.get_template("index.j2")
    html_file = os.path.join(settings.html_folder, "index.html")

    pages = [
        p
        for p in os.listdir(settings.html_folder)
        if p != "index.html" and p.endswith(".html")
    ]
    date = datetime.datetime.now().strftime("%-I:%m %p %A %-d %B")
    with open(html_file, "w") as file:
        print(template.render(pages=pages, date=date), file=file)


if __name__ == "__main__":
    logger = initiate_logging()
    sys.excepthook = excepthook
    logger.info('<span style="white-space: pre;">Program ran')
    wordlist = read_wordlist()
    for xml in os.listdir(settings.xml_folder):
        # don't bother with the user guide to the xml scheme
        if not xml.endswith(".xml"):
            continue
        user = os.path.basename(xml).rstrip(".xml")
        try:
            text_file = os.path.join(settings.xml_folder, xml)
            texts = parse_xml(text_file)
            html_it(texts, user)
        except Exception as e:
            print("Error: " + str(e))
    create_index()
    logger.info("Program finished \n</span>")

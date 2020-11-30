#! /usr/bin/python3

import csv
import os
import xml.etree.ElementTree as ET

from jinja2 import Environment, FileSystemLoader
import settings


def read_wordlist():
    with open(settings.word_list_file, 'r', encoding='utf8') as csvfile:
        reader = csv.reader(csvfile)
        words = [str(w).lstrip("'[").rstrip("]'") for w in reader]
    return words


def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    data = [t for t in root]

    texts = []

    for t in list(data):
        text = {}
        try:
            text['title'] = t.get('title').strip()
        except AttributeError:  # It's none
            text['title'] = ''
        for elem in t:
            try:
                text[elem.tag] = elem.text.strip()
            except AttributeError:  # It's none
                text[elem.tag] = ''

        if not text['kovol']:  # Use the matat if no imengis is available
            if text['matat']:
                text['kovol_interlinear'] = text['matat'].strip().split(' ')
        else:
            text['kovol_interlinear'] = text['kovol'].strip().split(' ')
        text['english_interlinear'] = text['literal'].strip().split(' ')
        
        texts.append(text)
        
    return texts


def html_it(texts, user):
    # Use a Jinja template to create the web page
    file_loader = FileSystemLoader(settings.code_folder)
    env = Environment(loader=file_loader, autoescape=True)
    template = env.get_template('text_template.j2')
    file_name = user + '_texts.html'
    html_file = os.path.join(settings.html_folder, file_name)
    with open(html_file, 'w') as file:
        print(template.render(texts=texts, wordlist=wordlist), file=file)
    print('HTML created for {user}'.format(user=file_name))


def create_index():
# Create a basic index page for Apache to use
    with open(os.path.join(settings.html_folder, 'index.html'), 'w') as index_file:
        index_file.write('<div class="container">')
        for file in os.listdir(settings.html_folder):
            if file == 'index.html':
                continue
            if file.endswith('.html'):
                index_file.write(
                    '<h3><li><a href="{filename}">{page}</a></li></h3>'.format(filename=file, page=file))
        index_file.write('</div>')


if __name__ == '__main__':
    wordlist = read_wordlist()
    for xml in os.listdir(settings.xml_folder):
    # don't bother with the user guide to the xml scheme
        if xml == 'text_xml_schema.md':
            continue
        elif xml == 'audio':
            continue
        user = os.path.basename(xml).rstrip('.xml')
        try:
            texts = parse_xml(os.path.join(settings.xml_folder, xml))
            html_it(texts, user)
        except Exception as e:
            print("Error: " + e)
    create_index()


# Text interlinearizer
A simple python script that turns a language texts filed in an .xml into a interlinear .html file.
![interlinear_example](https://raw.githubusercontent.com/stevetasticsteve/text_interlinear/master/interlinear_example.jpg)

## Features
- Word by word interlinear texts
- Words appear in red if they aren't in your wordlist allowing you to spot new vocabulary or spelling mistakes
- Text audio alongside the transcription

## Requirements
- Jinja2

## How to use
- Create a new file settings.py that follows the pattern laid out in settings_example, defining paths
to where the .xml, code and audio can be found.

- Write up a text following the instructions laid out in text_xml_schema.md

- Run text_interlinear.py (or run_interlinear.sh) The .xml will be read and turned into a .html file.
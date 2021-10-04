#!/usr/bin/env python3

import re
import lxml.etree as ET
from collections import defaultdict
from greek_normalisation.utils import nfc


DATA = defaultdict(set)

XMLFILE = 'longus.xml'

OUTPUT_FILE = 'daphnis_lemmatisation.txt'

DOM = ET.parse(XMLFILE)

WORDS = DOM.getroot().findall(".//word")

print(len(WORDS), "found in XMLFILE")

for word in WORDS:
    form = word.get('form')
    lemma = word.get('lemma')
    DATA[form].add(lemma)

with open(OUTPUT_FILE, 'w', encoding="UTF-8") as f:
    for form, lemmas in DATA.items():
        print(f"{form} {' '.join(lemmas)}", file=f)

print("DONE!")

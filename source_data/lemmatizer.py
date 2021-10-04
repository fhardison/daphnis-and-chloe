import sys
import os
from collections import defaultdict
from greek_normalisation.utils import nfc, grave_to_acute

FILE = os.path.join(os.path.dirname(__file__), 'gr_lemma_form_mapping.txt')

DATA = defaultdict(list)

with open(FILE, 'r', encoding="UTF-8") as f:
    for line in f:
        form, lemma, parse = line.strip().split('\t', maxsplit=2)
        if not (lemma, parse) in DATA[form]:
            DATA[form].append((lemma,parse))
NOT_FOUND = set()

def lemmatize(f, verbose=False):
    #f = strip_accents(nfc(f))
    f = grave_to_acute(nfc(f))
    if f in DATA:
        return DATA[f]
    else:
        NOT_FOUND.update([f])
        if verbose:
            print(f"{f} not in lemmatizer DATA", file=sys.stderr)
        return None

def get_not_found():
    return NOT_FOUND
    

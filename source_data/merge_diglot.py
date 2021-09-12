from morpheus_glosser import load_glosser

from gnt_data import get_tokens, TokenType
from greek_normalisation.utils import grave_to_acute
from collections import Counter
import re

gnt_counts = Counter()

gnt_tokens = get_tokens(TokenType.form)

for x in gnt_tokens:
    gnt_counts[x] += 1

GR = "gr_daphnis_and_chloe_.txt"
EN = "en_daphnis_and_chloe_wiki_modified.txt"


def clean(x):
    return grave_to_acute(re.sub('[·;“ʼ”,.)(!?]', '', x)).lower()



nums = [str(x) for x in range(0,10)]

def load_to_dict(fpath):
    out = {}
    line_counter = 0
    last_address = ''
    with open(fpath, 'r', encoding="UTF-8") as f:
        for line in f:
            if not line.strip():
                continue
            line_counter += 1
            try:
                if not(line.strip()[0] in nums):
                    out[last_address] += '  ' + line.strip()
                else:
                    address, cons = line.strip().split(' ', maxsplit=1)
                    last_address = address
                    out[address] = cons
            except ValueError as ve:
                if line[0] not in range(0,10):
                    out[last_address] += '  ' + line.strip()
                else:
                    print(line_counter, line)
                    raise ve
            except Exception as e:
                print(line_counter, line)
                raise e
    return out
    
    
    
greek_text = load_to_dict(GR)

eng_text = load_to_dict(EN)

gr_out = []


with open("daphnis_merged.txt", 'w', encoding="UTF-8") as f:

    for key, text in eng_text.items():
        assert key + "@gr" in greek_text
        gr_line = greek_text[key + "@gr"]
        print(key + "@gr" + gr_line, file=f)
        print(key + "@en" + text, file=f)
        print('', file=f)

print("DONE")
    

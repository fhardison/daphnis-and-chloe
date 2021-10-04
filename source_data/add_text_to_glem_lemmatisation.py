import sys
from collections import defaultdict


IFILE = 'poss_disambigs.txt'
# IFILE = 'daphnis_and_chloe_glem_lemmatisation.txt'
TEXT_FILE = "daphnis_text.txt"


OUTPUT = "daphnis_and_chloe_tokens.txt"

TEXT_BUFFER = []

with open(TEXT_FILE, 'r', encoding="UTF-8") as f:
    for line in f:
        TEXT_BUFFER.append(line.strip())
# then output.

COUNTER = 0
LINE_NUM = 1
with open(IFILE, 'r', encoding="UTF-8") as f, open(
        OUTPUT, 'w', encoding="UTF-8") as g:
    for line in f:
        if '3.11' in line:
            print(line)
        if '@' in line:
            print(line.strip().replace('.norm', '') + '\t' + "NONE", file=g)
            print(f"{LINE_NUM} has {line.split()[0]}")
        else:
            text = TEXT_BUFFER[COUNTER]
            print(text + "\t" + line.strip(), file=g)
        COUNTER += 1
        LINE_NUM += 1


print("DONE")

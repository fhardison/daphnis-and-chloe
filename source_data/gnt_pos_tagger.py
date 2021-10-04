#!/usr/bin/env python3

from collections import defaultdict, Counter
from gnt_data import TokenType, get_tokens
from greek_normalisation.utils import nfc, grave_to_acute


tokens = get_tokens(TokenType.all)

MODEL = defaultdict(Counter)

for (_, form, pos, _) in tokens:
    MODEL[grave_to_acute(nfc(form.lower()))][pos] += 1


# LXX data taken from Eliranwong's GreekResources repo :
with open("lxx_Lemma_pos_map.txt", 'r', encoding="UTF-8") as f:
    for line in f:
        if not line.strip():
            continue
        lemma, pos = line.strip().split(' ', maxsplit=1)
        MODEL[grave_to_acute(nfc(lemma.lower()))][pos] +=1


print(MODEL)
def tag_pos_word(w, opt_number=1):
    word = grave_to_acute(nfc(w)).lower()
    if word in MODEL:
        return [x[0] for x in MODEL[word].most_common(opt_number)]
    return None


if __name__ == '__main__':
    print(MODEL['βίβλος'])
    res = tag_pos_word('βίβλος')
    print(res)
    assert res[0] == 'N-'
    print(tag_pos_word('ἐγέννησε(ν)', 2))

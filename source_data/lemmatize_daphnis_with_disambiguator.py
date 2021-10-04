#!/usr/bin/env python3

from collections import defaultdict, Counter
import unicodedata
from greek_accentuation.characters import strip_length
from greek_normalisation.utils import nfc
from morpheus import Morpheus
from gnt_data import get_tokens, TokenType
from bigram_disambiguator import make_bigram_model, disambiguate


tokens = get_tokens(TokenType.all)

lemmas_in_gnt = [x[4] for x in tokens]

bigram_model = make_bigram_model(lemmas_in_gnt)
uni_gram_model = Counter(lemmas_in_gnt)
print(len(bigram_model), "Items in bigram model")
results = defaultdict(list)
last_lemmatisation = []
max_line = 999999
res = []
ambigs = []
counter = 0
overides = {}

with open('lemma_overrides.txt', 'r', encoding="UTF-8") as f:
    for line in f:
        if not line.strip():
            continue
        override, lemma = nfc(line).strip().split(",")
        overides[override.strip()] = lemma.strip()

with Morpheus("morpheus.json") as morpheus, open(
        'daphnis_and_chloe_tokens.txt', 'r', encoding='UTF-8') as f, open(
            'daphnis_and_chloe_tokens_2.txt', 'w', encoding="UTF-8"
        ) as g:

    for line in f:
        counter += 1
        if not line.strip():
            continue
        out_parse = '??'
        text, norm, lemma, parse = line.strip().split('\t', maxsplit=3)

        lemmas, cache_hit = morpheus.lookup(
            strip_length(norm), lang="grc", engine="morpheusgrc"
        )

        if len(lemmas) > 1:

            res = disambiguate(
                lemmas, last_lemmatisation, bigram_model, uni_gram_model
            )

        if res != []:
            lemmas = res
        last_lemmatisation = lemmas
        lout = ' | '.join(lemmas)
        if lout in overides:
            lout = overides[lout]
        elif len(lemmas) > 1:
            ambigs.append((counter, lout))
        if len(lemmas) > 0 and lemmas[0] == lemma:
            out_parse = parse
        if lemmas == []:
            lemmas = ['??']
        print('\t'.join([text, norm, lout, out_parse]), file=g)
        res = []

with open('lemma_problems.txt', 'w', encoding="UTF-8") as f:
    counter = 0
    for (line_num, lemmas) in sorted(ambigs, key=lambda x: x[1]):
        counter += 1
        print(f"{line_num}: {lemmas}", file=f)
    print(f"{counter} ambigeous words")

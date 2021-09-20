#!/usr/bin/env python3

from collections import defaultdict, Counter
import unicodedata


from utils import print_interlinear, display_ambigeous_lemmas

from greek_accentuation.characters import strip_length
import yaml

from bigram_lemmatizer import lemmatise_word_with_bigram, make_bigrams
from gnt_data import get_tokens, TokenType
from morpheus_lemmatizer import load_lemmatiser_data
from abott_glosser import Glosser
import sys

glosser = None
if len(sys.argv) > 1:
    if not '--no-gloss' in sys.argv[1]:
        glosser = Glosser('custom-glosses.tab')



IFILE = 'daphnis_merged.txt'
OFILE = 'daphnis_interlinear.txt'

lemma_data = load_lemmatiser_data()

bigram_model = Counter(make_bigrams([x.lower() for x in get_tokens(TokenType.lemma)]))
lemma_overrides = {}

try:
    with open("lemma-overides.yaml", encoding="UTF-8") as f:
        lemma_overrides = yaml.safe_load(f)
except FileNotFoundError:
    lemma_overrides = {}

problems = defaultdict(list)


input_filename = f"daphnis.sent.norm.txt"
output_filename = f"daphnis.sent.lemma.txt"

with open(input_filename, encoding="UTF-8") as f, open(output_filename, "w", encoding="UTF-8") as g:
    last_lemma = ['?']
    for line in f:
        if ".text" in line:
            text_list = line.strip().split()
        if ".flags" in line:
            flags_list = line.strip().split()
        if ".norm" in line:
            ref = line.split(".norm")[0]
            norm_list = line.strip().split()
            lemma_list = [f"{ref}.lemma"]
            if "1.4" in ref:
                break
            for norm in line.split()[1:]:

                # see if we have an override

                lemma = None
                prefix = None
                
                if norm in lemma_overrides:
                    lemma = lemma_overrides[norm].get("default")
                    for k, v in lemma_overrides[norm].items():
                        if not isinstance(k, str):
                            print(f"*** {k} is not a string (under {norm})")
                            break
                        if k != "default" and ref.startswith(k):
                            if prefix is None or len(k) > len(prefix):
                                prefix = k
                                lemma = v

                # otherwise check morpheus

                if lemma is None:
                    # (word, norm, ref,  lemmas, last_lemma, bmodel, overrides)
                    (_, lemmas), ll = lemmatise_word_with_bigram(
                        norm, norm, ref, 
                        lemma_data, last_lemma, 
                        bigram_model, lemma_overrides)
                    last_lemma = ll
                    if len(lemmas) != 1:
                        problems[(norm, "|".join(sorted(lemmas)))].append(ref)
                        lemma = "-"
                    else:
                        
                        lemma = lemmas[0]
                        if lemma == None:
                            lemma = '-'
                lemma_list.append(lemma)
            
            print_interlinear([norm_list, lemma_list], g)
            with open("problems.txt", 'a', encoding="UTF-8") as h:
                res = display_ambigeous_lemmas(line, problems, glosser)
                h.write('\n'.join(res))
            
                
                



for norm, lemmas in problems.keys():
    print(norm, problems[(norm, lemmas)], lemmas.split("|"))

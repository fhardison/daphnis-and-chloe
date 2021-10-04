from collections import defaultdict
from morpheus_lemmatizer import load_lemmatiser_data
from greek_normalisation.utils import nfc
from lemmatizer import lemmatize

IFILE = 'daphnis_and_chloe_glem_lemmatisation.txt'
# OFILE = 'daphnis_and_chloe_sents.lemmas.txt'


LEMMA_LIST = defaultdict(list)
# PARSE_LIST = defaultdict(list)

LEMMA_DATA = load_lemmatiser_data()

CUR_SENT = None

AMBIGEOUS = []

with open(IFILE, 'r', encoding="UTF-8") as f, open('poss_disambigs.txt', 'w', encoding="UTF-8") as g:
    for line in f:
        if not '\t' in line.strip():
            print(line.strip(), file=g)
            continue
        form, lemma, parse = line.strip().split('\t', maxsplit=3)
        form = nfc(form)
        if '1.' in form or '2.' in form or '3.' in form or '4.' in form:
            CUR_SENT = form
            
        if not lemma == "NONE":
            print(line.strip(), file=g)
        else:
            if form in LEMMA_DATA:
                poss = LEMMA_DATA[form]
                if len(poss) == 1:
                    print('\t'.join([form, poss[0], '??']), file=g)
                else:
                    AMBIGEOUS.append([CUR_SENT, form, poss])
                    print(line.strip(), file=g)
            else:
                poss = lemmatize(form)
                if poss:
                    if len(poss) != 1:
                        if len(set([x[0] for x in poss])) == 1:
                            print('\t'.join([form, poss[0][0], '??']), file=g)
                        else:
                            AMBIGEOUS.append([CUR_SENT, form, poss])
                            print(line.strip(), file=g)
                    else:
                        print('\t'.join([form, poss[0][0], poss[0][1]]), file=g)
                else:
                    print(line.strip(), file=g)
        
        

with open('ambigeous.txt', 'w', encoding="UTF-8") as h:
    for (sent, form, poss) in AMBIGEOUS:
        output = ' | '.join(
          [f"{w}, {p}" for w, p in poss])
        print(f"{sent} - {form} => {output}", file=h)
print(len(AMBIGEOUS), "words with multiple possibilities")
print("DONE")
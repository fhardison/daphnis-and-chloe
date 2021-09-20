from collections import defaultdict


DATAFILE = 'morpheus_form_gloss.txt'
FORM_LEMMA_GLOSS = 'morpheus_form_lemma_gloss.txt'


def load_glosser():
    data = {}
    with open(DATAFILE, 'r', encoding="UTF-8") as f:
        for line in f:
            form, gloss = line.strip().split('\t', maxsplit=1)
            if form in data:
                data[form] =  data[form] + ", " + gloss
            else:
                data[form] = gloss
        return data

        
def load_glosser_with_lemmas():
    """ -> dict[form] -> dict[(lemma, parse)] -> glosses"""
    data = defaultdict(dict)
    with open(FORM_LEMMA_GLOSS, 'r', encoding="UTF-8") as f:
        for line in f:
            form, lemma, parse, gloss  = line.strip().split('\t', maxsplit=3)
            key = (lemma, parse)
            if key in data[form]:
                data[form][key] =  data[form][key] + f" | " + gloss
            else:
                data[form][key] = gloss
        return data
        
        
if __name__ == '__main__':
    data = load_glosser_with_lemmas()
    res = data['ἀάατον']
    print(data['ἀάατον'])
    assert len(list(res.items())) == 9
    
    
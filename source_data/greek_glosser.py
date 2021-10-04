#
# Gloss data taken from https://github.com/helmadik/shortdefs which contains
# data taken from Perseus (perseus.uchicago.edu/greek.html)
# and Logeion (https://logeion.uchicago.edu/lexidium)
#
import os
from greek_normalisation.utils import nfc


class Glosser():
    def __init__(self, custom=None):

        self.data = dict()
        source_dir = os.path.join(os.path.dirname(__file__))
        with open(os.path.join(source_dir, "ShortdefsforOKLemma_perseus.txt"),
                  'r', encoding="UTF-8") as f:
            for line in f:
                if not line.strip():
                    continue
                lemma, gloss = line.strip().split('\t', maxsplit=1)
                self.data[nfc(lemma)] = gloss
        if custom:
            with open(custom, 'r', encoding="UTF-8") as f:
                for line in f:
                    parts = line.split("\t", maxsplit=1)
                    if len(parts) > 1 and not nfc(parts[0]) in self.data:
                        self.data[nfc(parts[0])] = parts[1]

    def get(self, l, default='??'):
        normed = nfc(l)
        return self.data.get(normed, default)


if __name__ == '__main__':
    GLOSSER = Glosser()
    assert GLOSSER.get('Αἰακίδης') == 'son of Aeacus', "Αἰακίδης not not match 'son of Aeacus in gloss data'"
    print(len(GLOSSER.data.items()), "items in glosser")

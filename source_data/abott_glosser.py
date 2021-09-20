from greek_normalisation.utils import nfc
import yaml
import sys

class Glosser():
    def __init__(self, *args):
        self.data = dict()
        with open("lexemes_with_abbott.yaml", encoding="utf-8") as f:
            self.data = yaml.load(f, Loader=yaml.FullLoader)
        if len(args) > 0:
            with open(args[0], 'r', encoding="UTF-8") as f:
                for line in f:
                    parts = line.split("\t", maxsplit=1)
                    if len(parts) > 1 and not nfc(parts[0]) in self.data:
                        self.data[nfc(parts[0])] = {'gloss': parts[1]}

    def get(self, l):
        normed = nfc(l)
        if normed in self.data:
            try:
                return self.data[normed]['gloss']
            except:
                try:
                    #print(f"{normed} does not have gloss, trying abott-smith-gloss")
                    return self.data[normed]['abott-smith-gloss']
                except:
            #        print(f"{normed} does not have any known gloss in list")
                    return ''
        else:
            #print(f"{normed} not found in gloss list")
            return ''

    def get_abott(self, l):
        normed = nfc(l)
        if normed in self.data:
            try:
                return self.data[normed]['abott-smith-gloss']
            except:
                try:
                    print(f"{normed} does not have abott-smith-gloss, trying gloss", file=sys.stderr)
                    return self.data[normed]['gloss']
                except:
                    print(f"{normed} does not have any known gloss in list", file=sys.stderr)
                    return ''


        else:
            print(f"{normed} not found in gloss list", file=sys.stderr)
            return ''

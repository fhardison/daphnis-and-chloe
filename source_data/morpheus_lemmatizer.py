from collections import defaultdict
from greek_normalisation.utils import nfc

DATAFILE = 'morpheus_form_lemma.txt'


def load_lemmatiser_data():
    with open(DATAFILE, 'r', encoding="UTF-8") as f:
        data = defaultdict(list)
        for line in f:
            form, lemma, parse = line.strip().split('\t', maxsplit=2)
            if not lemma in data[form]:
                data[form].append(lemma)
        return data


if __name__ == '__main__':
    data = load_lemmatiser_data()
    print(data['ἀάατον'])
    assert data['ἀάατον'] == ['ἀάατος', 'ἀάατος', 'ἀάατος', 'ἀάατος', 'ἀάατος', 'ἀάω', 'ἀάω', 'ἀάω', 'ἀάω']

            
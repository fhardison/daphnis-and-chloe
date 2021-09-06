DATAFILE = 'morpheus_form_gloss.txt'


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
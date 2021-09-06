from morpheus_glosser import load_glosser

glosser = load_glosser()


with open("..\\daphnis_and_chloe_tokens.txt", 'r', encoding="UTF-8") as f:
    with open("..\\daphnis_and_chloe_gloss_tokens.txt", 'w', encoding="UTF-8") as ofile:
        for line in f:
            try:
                index, text, form, lemmas = line.strip().split('\t', maxsplit=3)
                olemmas = []
                if "OR" in line:
                    for lemma in lemmas.split(' OR '):
                        if not lemma:
                            continue
                        l, ps = lemma.split(' ', maxsplit=1)
                        if l in glosser:
                            olemmas.append(f"{l} - {glosser[l]}")
                        else:
                            olemmas.append("??")
                ofile.write('\t'.join([index, text, form, lemmas.strip(), ' OR '.join(olemmas)]).strip() + "\n")
            except:
                print(line)
                exit()
            
print("DONE")
            
        
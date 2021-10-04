import re
import subprocess
from collections import Counter
from booklet2 import main
from gnt_data import get_tokens, TokenType
from greek_normalisation.utils import grave_to_acute
from morpheus_glosser import load_glosser
from greek_glosser import Glosser


gnt_counts = Counter()

#gnt_tokens = get_tokens(TokenType.form)
gnt_tokens = get_tokens(TokenType.lemma)

for x in gnt_tokens:
    gnt_counts[x] += 1

# GR = "..\\daphnis_merged.txt"
GR = "daphnis_and_chloe_tokens_2.txt"


def clean(x):
    return grave_to_acute(re.sub('[·;“ʼ”,.)(!?]', '', x)).lower()


def load_tokens(fpath):
    out = []
    buffer = []
    with open(fpath, 'r', encoding="UTF-8") as f:
        for line in f:
            if not line.strip():
                continue
            text, norm, lemma, parse = line.strip().split('\t', maxsplit=3)
            if '@' in text:
                out.append(buffer)
                buffer = [(text.split('@')[0], '')]
            else:
                buffer.append((text, lemma))
        out.append(buffer)
    return out
            
    

nums = [str(x) for x in range(0,10)]

def load_to_dict(fpath):
    out = {}
    line_counter = 0
    last_address = ''
    with open(fpath, 'r', encoding="UTF-8") as f:
        for line in f:
            #if not line.strip():
            #    continue
            if not "@gr" in line:
                continue
            line_counter += 1
            try:
                if not(line.strip()[0] in nums):
                    out[last_address] += '  ' + line.strip()
                else:
                    adr, cons = line.strip().split(' ', maxsplit=1)
                    address = adr.replace("@gr", '')
                    last_address = address
                    out[address] = cons
            except ValueError as ve:
                if line[0] not in range(0,10):
                    out[last_address] += '  ' + line.strip()
                else:
                    print(line_counter, line)
                    raise ve
            except Exception as e:
                print(line_counter, line)
                raise e
    print(line_counter)
    return out
    
    
# greek_text = load_to_dict(GR)

greek_text = load_tokens(GR)

#eng_text = load_to_dict(EN)

gr_out = []


#GLOSSER= load_glosser()
GLOSSER = Glosser()


excludes = ['δέ', 'καί', 'Δάφνις']

MISSED_COUNTER = 0

def format_section_tokens(text, counts, glosser, lim):
    output = []
    missed = 0
    for form, lemma in text:
        
        if lemma in excludes:
            output.append(form)
        elif '.' in form:
            output.append(form)
        else:
            if counts[lemma] < lim:
                gloss = glosser.get(lemma)
                
                if not gloss == '??':
                    output.append(form + "\\footnote{\\tiny{" + lemma + ": " +
                                  gloss + "}}")
                else:
                    output.append(form + "*")
                    missed += 1
            else:
                output.append(form)
    return ' '.join(output).replace('&', '\\&'), missed


def format_section(key, text, counts, glosser, lim):
    output = [f"{key}"]
    missed = 0
    for word in [x for x in text.split(' ') if x.strip()]:
        cleaned = clean(word)
        if cleaned in excludes:
            output.append(word)
        else:
            if counts[cleaned] < lim:
                if cleaned in glosser:
                    output.append(word + "\\footnote{\\tiny{" +
                                  glosser.get(cleaned, '??') + "}}")
                else:
                    output.append(word + "*")
                    missed += 1
            else:
                output.append(word)
    return ' '.join(output).replace('&', '\\&'), missed


#for key, text in greek_text.items():
for text in greek_text:
    if not text:
        continue
    if not text[0][0].startswith('2.'):
        continue
    text, missed = format_section_tokens(text, gnt_counts, GLOSSER, 10)
    gr_out.append(text)
    MISSED_COUNTER += missed


print("missed: " + str(MISSED_COUNTER))


HALF_LETTER = """\\usepackage{geometry}
\\geometry{
  paperheight=8.5in,
  paperwidth=5.5in,
  margin=0.5in,
  heightrounded,
}"""


HEADER = "\\documentclass[12pt]{book}\n" + HALF_LETTER + """
\\usepackage{polyglossia}
\\setmainlanguage[variant=ancient]{greek}
\\setmainfont{Libertinus Serif}
\\usepackage{reledmac}
\\usepackage{setspace}
\\usepackage{etoolbox}
\\arrangementX[A]{twocol}
\\colalignX{\\justifying}
\\makeatletter
\\bhooknoteX[A]{\\setstretch {\\setspace@singlespace}}
\\bhookgroupX[A]{\\setstretch {\\setspace@singlespace}}
\\makeatother
\\let\\footnote\\footnoteA

\\usepackage{microtype}

\\begin{document}"""

FOOTER = "\\end{document}"


with open("reader.tex", 'w', encoding="UTF-8") as f:
    f.write(HEADER)
    f.write('\n\n'.join(gr_out))
    f.write(FOOTER)

subprocess.run(['tectonic.exe', 'reader.tex'])

pdf_name = "reader.pdf"

main(pdf_name)

print("DONE")

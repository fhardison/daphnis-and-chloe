from morpheus_glosser import load_glosser

from gnt_data import get_tokens, TokenType
from greek_normalisation.utils import grave_to_acute
from collections import Counter
import re

gnt_counts = Counter()

gnt_tokens = get_tokens(TokenType.form)

for x in gnt_tokens:
    gnt_counts[x] += 1

GR = "daphnis_and_chloe.txt"



def clean(x):
    return grave_to_acute(re.sub('[·;“ʼ”,.)(!?]', '', x)).lower()



nums = [str(x) for x in range(0,10)]

def load_to_dict(fpath):
    out = {}
    line_counter = 0
    last_address = ''
    with open(fpath, 'r', encoding="UTF-8") as f:
        for line in f:
            if not line.strip():
                continue
            line_counter += 1
            try:
                if not(line.strip()[0] in nums):
                    out[last_address] += '  ' + line.strip()
                else:
                    address, cons = line.strip().split(' ', maxsplit=1)
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
    return out
    
    
    
greek_text = load_to_dict(GR)

#eng_text = load_to_dict(EN)

gr_out = []


USE_SILE = False

EN_CMARKER = "\ledleftnote{s}"

glosser = load_glosser()

excludes = ['δὲ', 'καὶ']

MISSED_COUNTER = 0

def format_section(key, text, counts, glosser, lim):
    output = [f"{key} "]    
    for word in [x for x in text.split(' ') if x.strip()]:
        cleaned = clean(word)
        if cleaned in excludes:
            output.append(word)
        else:
            if counts[cleaned] < lim:
                if cleaned in glosser:
                    output.append(word + "\\footnote{\\tiny{" + glosser[cleaned] + "}}")
                else:
                    #output.append(word + "\\footnote{\\tiny{" + "??}}")
                    output.append(word + "*")
                    MISSED_COUNTER += 1
            else:
                output.append(word)
    return ' '.join(output)
    


def format_section_sile(key, text, counts, glosser, lim):
    output = [f"{key} "]    
    for word in text.split(' '):
        cleaned = clean(word)
        if cleaned in excludes:
            output.append(word)
        else:
            if counts[cleaned] < lim:
                if cleaned in glosser:
                    output.append(word + "\\footnote{\\font[size=10pt]{" + glosser[cleaned] + "}}")
                else:
                    #output.append(word + "\\footnote{\\tiny{" + "??}}")
                    output.append(word + "*")
            else:
                output.append(word)
    return ' '.join(output)


for key, text in greek_text.items():
    if not key.startswith('1.'): 
        continue
    if USE_SILE:
        gr_out.append(format_section_sile(key, text, gnt_counts, glosser, 10))
    else:
        gr_out.append(format_section(key, text, gnt_counts, glosser, 10))
    
print("missed: " + MISSED_COUNTER)
HALF_LETTER = """\\usepackage{geometry}
\\geometry{
  paperheight=8.5in,
  paperwidth=5.5in,
  margin=0.5in,
  heightrounded,
}"""

SILE_HEADER = r"""\begin[papersize=5.5inx8.5in,class=book]{document}
\nofolios
\font[family=Gentium Plus,size=10pt]
\footnote:separator{\em{Separator}\skip[height=5mm]}
\footnote:options[interInsertionSkip=3mm]
"""

SILE_FOOTER = r"""\end{document}
"""


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

FOOTER =  "\\end{document}"



with open("reader.tex", 'w', encoding="UTF-8") as f:
    if USE_SILE:
        f.write(SILE_HEADER)
        f.write('\n\n'.join(gr_out))
    
        f.write(SILE_FOOTER)
    else:
        f.write(HEADER)
        f.write('\n\n'.join(gr_out))
    
        f.write(FOOTER)

print("DONE")


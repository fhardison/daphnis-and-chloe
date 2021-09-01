
GR = "daphnis_and_chloe.txt"

EN = "en_daphnis_and_chloe_wiki_modified.txt"


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

eng_text = load_to_dict(EN)

gr_out = []

en_out = []

def format_section_2(address, text, cmarker = ''):
    return """\pstart
\eledchapter{""" + address + "}" + cmarker + """
\pend
\pstart
""" + text.strip() + """
\pend
"""


def format_section(address, text, cmarker = ''):
    return """\pstart
""" + address + '  ' + text.strip() + """
\pend
"""


EN_CMARKER = "\ledleftnote{s}"

for key, text in greek_text.items():
    gr_out.append(format_section(key, text))
    en_out.append(format_section(key, eng_text[key], EN_CMARKER))
    

HEADER = r"""\documentclass{book}
\usepackage[osf,p]{libertinus}
\usepackage{microtype}
\usepackage[pdfusetitle,hidelinks]{hyperref}
\usepackage[series={},nocritical,noend,nofamiliar,noledgroup]{reledmac}
\usepackage{reledpar}

\usepackage{geometry}
\geometry{
  paperheight=8.5in,
  paperwidth=5.5in,
  margin=0.5in,
  heightrounded,}


\usepackage{graphicx}
\usepackage{polyglossia}
\setmainlanguage{english}
\setotherlanguage{greek}

\usepackage{metalogo}

\linenumincrement*{1}
\firstlinenum*{1}
\setlength{\Lcolwidth}{0.45\textwidth}
\setlength{\Rcolwidth}{0.45\textwidth} 

\begin{document}

\title{Daphnis and Chloe}
\date{}

\maketitle



\begin{pairs}

\begin{Rightside} 

\begin{english}
\beginnumbering
"""

MID = r"""
\endnumbering
\end{english}

\end{Rightside}




\begin{Leftside} 
\begin{greek}
\beginnumbering
"""

FOOTER = r"""\endnumbering
\end{greek}
\end{Leftside}

\end{pairs}
\Columns
\end{document}
"""


with open("diglot.tex", 'w', encoding="UTF-8") as f:
    f.write(HEADER)
    f.write('\n\n'.join(en_out))
    f.write(MID)
    f.write('\n\n'.join(gr_out))
    
    f.write(FOOTER)

print("DONE")


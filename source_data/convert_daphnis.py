import lxml.etree as ET
import re
from greek_normalisation.utils import nfc
NS={'tei': "http:www.tei-c.org/ns/1.0"}

XMLFILE = 'tlg0561.tlg001.perseus-grc2.xml'






dom = ET.parse(XMLFILE)

parts = dom.getroot().findall(f".//div[@type='textpart']", NS)

JUST_TEXT = True

counter = 0

cur_book = 0

cur_chapter = 0



books = {}

chapters = {}



with open("daphnis_and_chloe.txt", 'w', encoding="UTF-8") as f:

    for p in parts:
        t_type = p.get('subtype')
        if JUST_TEXT:
            
            if t_type == 'section':
                for para in p.iter('p'):
                    if para.text:
                        text = re.sub('[·;“ʼ”,.)(!?]', '', para.text).strip()
                        text = [t for t in text.split(' ') if t.strip()]
                        for t in text:
                            counter += 1
                            form = re.sub('[· ;“ʼ”,.)(!?]', '', t)
                            print(str(counter) + "\t" + nfc(t) + "\t" + nfc(form).lower(), file=f)
            elif t_type == 'book':
                #print(f"# Βιλίον {p.get('n')}" + "\n", file=f)
                cur_book = p.get('n')
                
                books[cur_book] = int(counter) + 1
        
            elif t_type == 'chapter':
                #print(f"## Κεφάλαιον {p.get('n')}" + "\n", file=f)
                cur_chapter = p.get('n')
                chapters[f"{cur_book}.{cur_chapter}"] = int(counter) + 1
        else:
            if t_type == 'book':
                #print(f"# Βιλίον {p.get('n')}" + "\n", file=f)
                cur_book = p.get('n')
        
            if t_type == 'chapter':
                #print(f"## Κεφάλαιον {p.get('n')}" + "\n", file=f)
                cur_chapter = p.get('n')
                print('\n' + f"{cur_book}.{cur_chapter}", file=f, end='  ')
            if t_type == 'section':
                for para in p.iter('p'):
                #    print(para.attrib)
                #for para in p.findall('./p'):
                    if para.text:
                        print(para.text , file=f, end=' ')
        

def write_index(xs, fpath, last_token):

    last_item = ''     
    xs = list(xs.items())  
    # start is the first token of the book
    # I get the end by the next start -1
    out = {}

    (item_1_key, item_1_start) = xs[0]
    out[item_1_key] = [item_1_start]
    last_item = item_1_key
    
    for (key, start) in xs[1:]:
        out[last_item].append(int(start - 1))
        out[key] = [start]
        last_item = key
    out[last_item].append(last_token)
    
    with open(fpath, 'w', encoding="UTF-8") as f:
        for (key, xs) in out.items():
            print(key, xs)
            f.write(f"{key} {xs[0]} {xs[1]}" + "\n")

write_index(books, "daphnis_books.txt", counter)

write_index(chapters, "daphnis_chapters.txt", counter)
    

print(len(parts))


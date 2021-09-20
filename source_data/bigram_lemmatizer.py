# -*- coding: UTF-8 -*-
from collections import Counter
from greek_normalisation.utils import nfc,grave_to_acute
import re
import yaml


def clean(x):
    return grave_to_acute(re.sub('[·;“ʼ”,.)(!?]', '', x)).lower()


def make_bigrams(xs):
    lastx = xs[0]
    output = []
    #output = [('', lastx)]
    for x in xs[1:]:
        output.append((lastx, x))
        lastx = x
   # output.append((lastx, ''))
    return output
       

def try_bigrams(lemmatisation, lastlemmas, bmodel):
    bigrams = []
    for lemma in lastlemmas:
        bigrams.extend([(lemma, x.lower()) for x in lemmatisation])
    out = []
    for b in bigrams:
        if b in bmodel:
            out.append((b, bmodel[b]))
        else:
            out.append((b, 0))
    res = sorted(out, key=lambda x: x[1], reverse=True)
    if all([x[1] == 0 for x in res]):
        return None
    else: 
        return res[0][0]

def handle_lemma_override(norm, ref, lemma_overrides):
    lemma = None
    prefix = None
    lemma = lemma_overrides[norm].get("default")
    for k, v in lemma_overrides[norm].items():
        if not isinstance(k, str):
            print(f"*** {k} is not a string (under {norm})")
            break
        if k != "default" and ref.startswith(k):
            if prefix is None or len(k) > len(prefix):
                prefix = k
                lemma = v
    return lemma


def lemmatise_word_with_bigram(word, norm, ref,  lemmas, last_lemma, bmodel, overrides):
    if not norm.strip():
        return (word, ['?']), ['?']
    if norm in overrides:
        override = handle_lemma_override(norm, ref, overrides)
        return (word, [override]), [override]            
    if norm in lemmas:
        res = lemmas[norm]
        if len(res) > 1:
            # if we don't know the last lemma, don't use bigrams
            if last_lemma == ['?']:
                return (word, res), res
            else:
                x = try_bigrams(res, last_lemma, bmodel)
                if x:                    
                    try:
                        #print(x[1])
                        return (word , [x[1]+ "@*"]), [x[1]]
                    except:
                        print('failure')
                        print(x)
                        exit()
                else:
                    return (word, res), res
        else:
            return (word, [res[0]]), [res[0]]
    else:
        return (word, ['?']), ['?'] 


def lemmatise_with_bigrams(text, lemmas, bmodel, overrides):
    words = [x for x in nfc(text).strip().split(' ')]
    output = []
    last_lemma = ['?']
    for ref, word in enumerate(words):
        norm = clean(word)
        l, last = lemmatise_word_with_bigram(word, norm, str(ref), lemmas, last_lemma, bmodel, overrides)
        output.append(l)
        last_lemma = last
    return output
               
            
        
if __name__ == '__main__':
    from gnt_data import get_tokens, TokenType
    from morpheus_lemmatizer import load_lemmatiser_data
    lemma_data = load_lemmatiser_data()

    bigram_model = Counter(make_bigrams([x.lower() for x in get_tokens(TokenType.lemma)]))
    
    lemma_overrides = {}
    with open('lemma-overides.yaml', 'r', encoding="UTF-8") as f:
        lemma_overrides = yaml.safe_load(f)
    
    #TEST = 'Καὶ ἐλθὼν ὁ Ἰησοῦς εἰς τὴν οἰκίαν Πέτρου εἶδεν τὴν πενθερὰν αὐτοῦ βεβλημένην καὶ πυρέσσουσαν·'
    TEST = 'Ἐν Λέσβῳ θηρῶν ἐν ἄλσει Νυμφῶν θέαμα εἶδον κάλλιστον ὧν εἶδον· εἰκόνα, γραφήν, ἱστορίαν ἔρωτος. Καλὸν μὲν καὶ τὸ ἄλσος, πολύδενδρον, ἀνθηρόν, κατάρρυτον· μία πηγὴ πάντα ἔτρεφε, καὶ τὰ ἄνθη καὶ τὰ δένδρα· ἀλλ’ ἡ γραφὴ τερπνοτέρα καὶ τέχνην ἔχουσα περιττὴν καὶ τύχην ἐρωτικήν· ὥστε πολλοὶ καὶ τῶν ξένων κατὰ φήμην ᾔεσαν, τῶν μὲν Νυμφῶν ἱκέται, τῆς δὲ εἰκόνος θεαταί.  Γυναῖκες ἐπʼ αὐτῆς τίκτουσαι καὶ ἄλλαι σπαργάνοις κοσμοῦσαι· παιδία ἐκκείμενα, ποίμνια τρέφοντα· ποιμένες ἀναιρούμενοι, νέοι συντιθέμενοι· λῃστῶν καταδρομή, πολεμίων ἐμβολή. Πολλὰ ἄλλα καὶ πάντα ἐρωτικὰ ἰδόντα με καὶ θαυμάσαντα πόθος ἔσχεν ἀντιγράψαι τῇ γραφῇ·  καὶ ἀναζητησάμενος ἐξηγητὴν τῆς εἰκόνος τέτταρας βίβλους ἐξεπονησάμην, ἀνάθημα μὲν Ἔρωτι καὶ Νύμφαις καὶ Πανί, κτῆμα δὲ τερπνὸν πᾶσιν ἀνθρώποις, ὃ καὶ νοσοῦντα ἰάσεται, καὶ λυπούμενον παραμυθήσεται, τὸν ἐρασθέντα ἀναμνήσει,  τὸν οὐκ ἐρασθέντα προπαιδεύσει. Πάντως γὰρ οὐδεὶς ἔρωτα ἔφυγεν ἢ φεύξεται, μέχρι ἂν κάλλος ᾖ καὶ ὀφθαλμοὶ βλέπωσιν. Ἡμῖν δʼ ὁ θεὸς παράσχοι σωφρονοῦσι τὰ τῶν ἄλλων γράφειν.'
    print(TEST)
    resolved_counts = 0
    normal_count = 0
    res = lemmatise_with_bigrams(TEST, lemma_data, bigram_model, lemma_overrides)
    for (word, lemma) in res:
        print(word, lemma)
        if "@*" in lemma[0]:
            resolved_counts += 1
    print()
    for word in [x for x in nfc(TEST).strip().split(' ')]:
        if clean(word).lower() in lemma_data:
            ls  = lemma_data[clean(word).lower()]
    #        print(word, ls)
            if len(ls) > 1:
                normal_count += 1
        else:
            pass
     #       print(word, "?")
    print("ambigeous, resolved")
    print(normal_count, resolved_counts)
        

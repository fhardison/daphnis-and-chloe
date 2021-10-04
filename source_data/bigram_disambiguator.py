from collections import Counter
from greek_normalisation.utils import nfc,grave_to_acute
import re



# Since the bigram model is a Counter
# it would be possible to combine multiple copora, 
# but we might want one of them to count more highly than another
# in that case "weight" can be set slightly higher than 1.
def make_bigram_model(xs, weight=1):
    lastx = xs[0]
    output = Counter()
    for x in xs[1:]:
        output[(lastx, x)] += (1 * weight)
        lastx = x
    return output

# * bmodel (bigram model) is a Counter of bigrams, 
# * (Optional) smodel (unigram model) is a Counter of items in the corpus
# * Returns a list of the most likely lemmatisation based on 
# either bigram counts or unigram counts # if unigram model was given and bigrams 
# were unhelpful for some reason
# Returns [] if there was a problem
def disambiguate(lemmatisation, lastlemmas, bmodel, smodel=None):
    bigrams = []
    if lemmatisation == [] :
        return []
    # if last lemmatisation was empty
    # return current lemmatisaton
    if lastlemmas == []:
        return lemmatisation
    # build bigrams from current lemmatisation and last lemmatisation
    for lemma in lastlemmas:
        bigrams.extend([(lemma, x.lower()) for x in lemmatisation])
    # if we couldn't build any for some reason, 
    # fall back on lemmatisation possibilties
    if bigrams == []:
        print("bigrams were none")
        return lemmatisation
    out = []
    max_count = 0
    for b in bigrams:
        if b in bmodel:
            bcount = bmodel[b]
            if bcount > max_count:
                max_count = bcount
            out.append((b, bcount))
        else:
            out.append((b, 0))
    # if the bigrams were unhelpful
    # default to most common unigram in corpus if a unigram model was given
    if max_count == 0 and smodel:
        out = []
        for lemma in lemmatisation:
            if lemma in smodel:
                scount = smodel[lemma]
                if scount > max_count:
                    max_count = scount
                out.append((lemma, scount))
            else:
                out.append((lemma, 0))
        # return unigram results
        return [x[0] for x in out if x[1] == max_count]
    # return bigram results
    return [x[0][1] for x in out if x[1] == max_count]

# Utility function if you won't want to have to pass the models in each time       
def build_disambiguator(model, unigram_model=None):
    return lambda x, y: disambiguate_with_bigrams(x, y, model, unigram_model)

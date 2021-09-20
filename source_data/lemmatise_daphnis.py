from bigram_lemmatizer import lemmatise_word_with_bigram
from gnt_data import get_tokens, TokenType
from morpheus_lemmatizer import load_lemmatiser_data

IFILE = 'daphnis_merged.txt'
OFILE = 'daphnis_interlinear.txt'

with open(IFILE, 'r', encoding="UTF-8") as f, open(OFILE, 'w', encoding="UTF-8") as g:
    
    
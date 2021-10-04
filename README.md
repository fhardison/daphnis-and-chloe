# Daphnis and Chloe

STATUS: Ongoing lemmatization; diglot complete; reader's edition in progress.

LEMMATIZATION STATUS: 1.1 to 1.10 lemmatized.

This repo is a lemmatization project for _Daphnis and Chloe_ by Longus as well as an English-Greek diglot. It also contains a reader's edition based on forms occuring 10 times or less in the Greek New Testament (data taken from James Tauber's [vocabulary-tools](https://github.com/jtauber/vocabulary-tools)). 

The final format of the lemmatization will be the format used by James Tauber's [vocabulary-tools](https://github.com/jtauber/vocabulary-tools) so that it can be processed by the same toolset. `daphnis_books.txt` and `daphnis_chapters.txt` contain the book and chapter mappings for tokens in the `daphnis_and_chloe_tokens.txt`. 

The lemmatization is being done with a custom toolset based on the form-lemma mappings from [Eulexis](https://github.com/PhVerkerk/Eulexis_off_line), which is released under a [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html), and data from [Morpheus XML data] taken from Giuseppe G. A. Celano's [Lemmatized Ancient Greek Texts](https://github.com/gcelano/LemmatizedAncientGreekXML) which is released under a [Creative Commons Attribution-NonCommercial 4.0 International License](http://creativecommons.org/licenses/by-nc/4.0/). 

The file `daphnis_merged.txt` contains an alignment of the English and Greek texts. Each line has a key that includes its language. Spliting the file based on `\n\n` will give you a pair of Greek and its corresponding English.

## Sources and License

As such this repo work is also released under a CC-BY-SA 4.0 license with the exceptions that source data contained herein is still subject to the relevant licenses. 



The Greek text (found in `source_data/tlg0561.tlg001.perseus-grc2.xml`) is taken from [Perseus Digital Library](http://www.perseus.tufts.edu/hopper/text?doc=urn:cts:greekLit:tlg0561.tlg001.perseus-grc1) and the English translation (found in `source_data/en_daphnis_and_chloe_wiki.txt` and `source_data/en_daphnis_and_chloe_wiki_modified.txt`)is taken from [Wikisource.org](https://en.m.wikisource.org/wiki/Daphnis_and_Chloe_(The_1896_Athenian_Society_Translation)). Both of these are released under a [CC-BY-SA 3.0](http://creativecommons.org/licenses/by-sa/3.0/us/). 


The Morpheus data used for `reader.pdf`, `reader.tex`, `morpheus_glosser.py` and `morpheus_form_gloss.txt` and some of the lemmatization work is taken from Giuseppe G. A. Celano's [Lemmatized Ancient Greek Texts ](https://github.com/gcelano/LemmatizedAncientGreekXML) which is released under a [Creative Commons Attribution-NonCommercial 4.0 International License](http://creativecommons.org/licenses/by-nc/4.0/). As a result, the aforementioned files are also licensed under the same license.

The `greek_glosser.py` file uses Gloss data taken from https://github.com/helmadik/shortdefs (in `ShortdefsforOKLemma_perseus.txt`) which contains
 data taken from Perseus (perseus.uchicago.edu/greek.html)
 and Logeion (https://logeion.uchicago.edu/lexidium). 




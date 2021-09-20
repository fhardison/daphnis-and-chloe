#!/usr/bin/env python3

"""
converts the textpart-per-paragraph to textpart-per-sentence.
"""

from utils import print_interlinear

from greek_normalisation.normalise import Normaliser, Norm

config = (
    Norm.GRAVE
    | Norm.ELISION
    | Norm.MOVABLE
    | Norm.EXTRA
    | Norm.PROCLITIC
    | Norm.ENCLITIC
    | Norm.CAPITALISED
)

PROPER_NOUNS = {
    "Δάφνις",
    "χλόη"
}


def format_flags(flags):
    s = ""
    if flags & Norm.PROCLITIC:
        s += "p"
    if flags & Norm.ENCLITIC:
        s += "n"
    if flags & Norm.GRAVE:
        s += "g"
    if flags & Norm.EXTRA:
        s += "x"
    if flags & Norm.ELISION:
        s += "l"
    if flags & Norm.MOVABLE:
        s += "m"

    if s == "":
        s = "."

    return s


normalise = Normaliser(config, proper_nouns=PROPER_NOUNS).normalise

input_filename = f"daphnis_merged.txt"
output_filename = f"daphnis.sent.norm.txt"

with open(input_filename, encoding="UTF-8") as f, open(output_filename, "w", encoding="UTF-8") as g:
    for line in f:
        if not line.strip():
            continue
        if "@en" in line:
            continue
        line = line.strip()
        ref, *text = line.split()
        text_list = [f"{ref}.text", *text]
        norm = [f"{ref}.norm"]
        flags = [f"{ref}.flags"]
        for token in text:
            norm_token, norm_flags = normalise(token.strip(",.;·«»()!"))
            norm.append(norm_token)
            flags.append(format_flags(norm_flags))

        print_interlinear([text_list, flags, norm], g)

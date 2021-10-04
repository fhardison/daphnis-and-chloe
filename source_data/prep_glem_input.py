
input_filename = f"daphnis.sent.norm.txt"
output_filename = f"daphnis_glem_input.txt"

with open(input_filename, encoding="UTF-8") as f, open(output_filename, "w", encoding="UTF-8") as g:
    last_lemma = ['?']
    for line in f:
        # if ".text" in line:
            #text_list = line.strip().split()
       # if ".flags" in line:
            #flags_list = line.strip().split()
        if ".norm" in line:
            for p in line.strip().replace('  ', ' ').split(' '):
                print(p, file=g)
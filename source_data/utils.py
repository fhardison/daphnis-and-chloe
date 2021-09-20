from unicodedata import normalize, category


def real_len(s):
    l = 0    
    for ch in normalize("NFD", s):
        if category(ch)[0] != "M":
            l += 1
    return l
    

def real_just(t, l):
    return t + (" " * (l - real_len(t)))


def print_interlinear(token_lists, fout):
    print(token_lists)
    max_len = [max(map(real_len, x)) for x in zip(*token_lists)]
    print(file=fout)
    for token_list in token_lists:
        print(
            " ".join(
                real_just(t, l) for l, t in zip(max_len, token_list)
            ).strip(),
            file=fout
        )

def show_lemma_problem(line, norm, lemmas, refs, glosser=None):
    # display
    print(line.replace(f' {norm} ', f' *{norm}* '))
    print()
    print(norm)
    for i, lemma in enumerate(lemmas):
        if glosser:
            gloss = glosser.get(lemma)
            if gloss:
                print(f"{i}: {lemma} - {gloss}")
            else:
                print(f"{i}: {lemma}")
        else:
            print(f"{i}: {lemma}")
    ask = True
    while ask:
        choice = input("Enter lemma number: ").strip()
        print(choice)
        if choice.lower() == 'b':
            return "B", None
        elif choice.lower() == 'n':
            return 'N', None
        elif choice.lower() == 'q':
            return "Q", None
        else:
            try:
                if len(choice) > 1 and choice[0].lower()[0] == 'd':
                    num = int(choice[1])
                    return "OK", norm + ":\n  " + f"default: {lemmas[num]}"
                else:
                    num = int(choice)
                    out = norm + ":\n"
                    for ref in set(refs):
                        out += f'  "{ref}": {lemmas[num]}' + "\n" 
                    return "OK", out.strip()
            except:
                print("Not a valid choice")
    

def display_ambigeous_lemmas(line, problems, glosser=None):
    solutions = []
    
    norm_lemmas = list(problems.keys())
    if len(norm_lemmas) < 1:
        print("No problems found")
        return []
    keep_looping = True
    counter = 0
    #print(norm_lemmas)
    while keep_looping:  
        norm, lemmas = norm_lemmas[counter]
  
        status, res = show_lemma_problem(line, norm, lemmas.split("|"), problems[(norm, lemmas)], glosser)
        
        if status == "B":
            counter -= 1
        elif status == 'Q':
            return solutions
        elif status == 'N':
            counter += 1
        elif status == "OK":
            solutions.append(res)
            counter += 1
        if counter >= len(norm_lemmas):
            return solutions
            
    return solutions
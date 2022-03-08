from os import sep

def get_data(name):
    fname = sep.join(["..", "..", "data", name + ".txt"])
    try:
        with open(fname, "r") as fdesc:
            fdata = fdesc.read()
            return fdata.split()
    except IOError as e:
        print(e)
    return "error"

def check_guess(word, guess):
    retv = ''
    for indx, letter in enumerate(word):
        if guess[indx] == letter:
            retv += 'G'
        else:
            if guess[indx] in word:
                retv += 'Y'
            else:
                retv += '.'
    return retv

def gen_key(word, guesses):
    nkeys = []
    for guess in guesses:
        nkeys.append(check_guess(word, guess))
    return "|".join(nkeys)

def get_big_table(wlist):
    big_table = {}
    anlist = get_data("answers")
    for wrd in anlist:
        tindx = gen_key(wrd, wlist)
        if tindx not in big_table:
            big_table[tindx] = [wrd]
        else:
            big_table[tindx].append(wrd)
    return big_table

def do_scan(wlist):
    big_table = get_big_table(wlist)
    histogram = {}
    for entry in big_table:
        indx = len(big_table[entry])
        if indx in histogram:
            histogram[indx] += 1
        else:
            histogram[indx] = 1
    histogram['words'] = " ".join(wlist)
    return histogram

if __name__ == "__main__":
    with open("wlist20.txt", "r") as fdesc:
        info = fdesc.read()
    indata = info.split("\n")
    olist = []
    for record in indata:
        rlist = record.split(", ")
        data = do_scan(rlist)
        olist.append(data)
    newlist = sorted(olist, key=lambda d: d[1], reverse=True)
    print(newlist)

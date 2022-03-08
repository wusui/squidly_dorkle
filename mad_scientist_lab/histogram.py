import os
import sys
import codecs
import itertools

sys.stdout = codecs.getwriter('utf=8')(sys.stdout.buffer)
sys.stderr = codecs.getwriter('utf=8')(sys.stderr.buffer)

fname = os.sep.join(["D:", "Users", "Warren", "python3",
                     "squirrels_on_caffeine", "src", "sedecordle",
                     "answers.txt"])
with open(fname, "r", encoding="UTF-8") as rfile:
    glist = rfile.read()

def add_to(word, hist):
    for letter in word:
        if letter in hist:
            hist[letter] += 1
        else:
            hist[letter] = 1

histogram_full = {}
histogram_once = {}
for word in glist.split():
    f_word = sorted(word)
    o_word = list(set(f_word))
    add_to(f_word, histogram_full)
    add_to(o_word, histogram_once)
print(dict(sorted(histogram_full.items(), key=lambda item: item[1])))    
print(dict(sorted(histogram_once.items(), key=lambda item: item[1])))

def test_word(word, glist):
    sw1 = ''.join(sorted(word))
    for guess in glist.split():
        sw2 = ''.join(sorted(guess))
        if sw1 == sw2:
            print(guess)

ok_list = []
for word in glist.split():
    bad = False
    for tlet in 'jqvwxz':
        if tlet in word:
            bad = True
            break
    if bad:
        continue
    if len(list(set(word))) != 5:
        continue
    ok_list.append(word)

print(ok_list)
print(len(ok_list), len(glist))
        
def get_2x5_wlist(ok_list, lset, hbl):
    ret_list = []
    for word in ok_list:
        bad = False
        for tlet in word:
            if tlet not in lset:
                bad = True
                break
        if bad:
            continue
        #print(word)
        other = [hbl]
        for letr in lset:
            if letr not in word:
                other.append(letr)
        #print(other)
        for word2 in ok_list:
            bad2 = False
            for tlet2 in word2:
                if tlet2 not in other:
                    bad2 = True
                    break
            if bad2:
                continue
            ret_list.append([word, word2])
    return ret_list
        
OKLETS = 'bcdefghiklmnoprstuy'        
acombos = list(itertools.combinations(OKLETS, 9))
print(acombos[50000])
lset = list(acombos[50000])
# print(get_2x5_wlist(ok_list, lset, 'a'))
out_str = []
for entry in acombos:
    ret_list = get_2x5_wlist(ok_list, list(entry), 'a')
    if ret_list:
        nstr = ret_list[0][0] + ret_list[0][1]
        str2 = []
        for let2 in OKLETS:
            if let2 not in nstr:
                str2.append(let2)
        rlist2 = get_2x5_wlist(ok_list, str2[1:], str2[0])
        if rlist2:
            print(ret_list, " pairs with ", rlist2) 
            for p1 in ret_list:
                for p2 in rlist2:
                    out_str += [p1 + p2]
txtlist = []
for entry in out_str:
    s = ", ".join(sorted(entry))
    txtlist.append(s)
slist = list(set(sorted(txtlist)))
ostr = "\n".join(slist)
with open("wlist20.txt", "w") as wlist:
    wlist.write(ostr)


                           
                
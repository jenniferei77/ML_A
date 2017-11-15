#nb.py
#Jennifer Isaza

from sys import *
import csv
from math import *
import operator



def isNum(var):
    try:
        float(var)
        return True
    except ValueError:
        return False

def target_val(file):
    if file[:3] == "lib":
        target = 1
    else:
        target = 0
    return target

def open_each(file):
    #open file and read
    with open(file, 'rb') as examp:
        vj = target_val(file)
        examp = csv.reader(examp, delimiter='\n', quotechar='|')
        examps = []
        for row in examp:
            examps += row
        for i in range(len(examps)):
            examps[i] = examps[i].lower()

    return examps, vj

def calc_Pvj(group, trains):
    Pvj = float(len(group))/len(trains)
    return(Pvj)

def Textj(group):
    Textj = []
    for i in range(len(group)):
        Textj += group[i]
    return(Textj)

def distinct(Textj):
    unique = set(Textj)
    return(unique)

def diff_words(nk_l, nk_c):
    for key in nk_l:
        if key in nk_c:
            True
        else:
            nk_c[key] = 0
    for key in nk_c:
        if key in nk_l:
            True
        else:
            nk_l[key] = 0
    return(nk_l, nk_c)

def find_nk(Textj):
    word_freq = {}
    for i in range(len(Textj)):
        if Textj[i] in word_freq:
            word_freq[Textj[i]] += 1
        else:
            word_freq[Textj[i]] = 1

    return word_freq

def prop_wkvj(nk, n, vocab):
    Pwk_vj = {}
    for key in nk:
        Pwk_vj[key] = float(nk[key]+1)/(n+vocab)
    return Pwk_vj

def classify_naive(Pvj, Pwv):
    vals = []
    for i in range(len(Pwv)):
        vals += [log(Pwv[i])]
    #print vals
    vNB = log(Pvj) + sum(vals)
    return vNB

def main():
    split_train = argv[1]
    libs = []
    cons = []
    count = 0
    with open(split_train, 'rb') as training:
        training = csv.reader(training, delimiter='\n', quotechar='|')
        trains = []
        train_examps = []
        for row in training:
            trains += row
            examps, vj = open_each(row[0])
            train_examps += examps
            if vj == 1:
                libs += [examps]
            else:
                cons += [examps]

        #calculate required P(vj) and P(wk|vj)
        Pvj_l = calc_Pvj(libs, trains)
        Pvj_c = calc_Pvj(cons, trains)

        #form Textj, a single doc created by concatenating all members of docsj
        Textl = Textj(libs)
        Textc = Textj(cons)

        #form n, total number of distinct word positions in Textj
        nl = len(Textl)
        nc = len(Textc)

        distincts = set(train_examps)
        vocab = len(distincts)

        #Number of times word wk occurs in Textj
        nk_l = find_nk(Textl)
        nk_c = find_nk(Textc)
        nk_l, nk_c = diff_words(nk_l, nk_c)

        #Calculate P(wk|vj)
        PwvL = prop_wkvj(nk_l, nl, vocab)
        PwvC = prop_wkvj(nk_c, nc, vocab)

        #Log Odds
        oddsL = {}
        oddsC = {}
        for key in PwvL:
            oddsL[key] = log(PwvL[key]/PwvC[key])

        for key in PwvC:
            oddsC[key] = log(PwvC[key]/PwvL[key])

        #print PwvL.keys()
        PwvL_vals = sorted(oddsL.items(), key=lambda x:x[1], reverse=True)
        PwvC_vals = sorted(oddsC.items(), key=lambda x:x[1], reverse=True)

        #print PwvL_vals
        for i in range(20):
            pairL = PwvL_vals[i]
            print "%s %.4f" % (pairL[0], pairL[1])

        print ""
        for i in range(20):
            pairC = PwvC_vals[i]
            print "%s %.4f" % (pairC[0], pairC[1])

main()
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

def prop_wkvj(nk, n, vocab, q):
    Pwk_vj = {}
    for key in nk:
        Pwk_vj[key] = (nk[key]+q)/(n+q*float(vocab))
        if nk[key] <= 0:
            #print nk[key]
            Pwk_vj[key] = (0.0001 + q) / (n + q * float(vocab))
            #print Pwk_vj[key]
    return Pwk_vj

def classify_naive(Pvj, Pwv):
    vals = []
    #print Pwv
    #print Pwv['the']
    for i in range(len(Pwv)):
        #print Pwv[i]
        vals += [log(Pwv[i])]
    vNB = log(Pvj) + sum(vals)
    return vNB

def main():
    split_train = argv[1]
    split_test = argv[2]
    q = argv[3]
    q = float(q)
    libs = []
    cons = []
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
        PwvL = prop_wkvj(nk_l, nl, vocab, q)
        PwvC = prop_wkvj(nk_c, nc, vocab, q)



    with open(split_test, 'rb') as testing:
        testing = csv.reader(testing, delimiter='\n', quotechar='|')
        tests = []
        test_examps = []
        libs_test = []
        cons_test = []
        for row in testing:
            tests += row
            test_exs, vj = open_each(row[0])
            test_examps += [test_exs]
            if vj == 1:
                libs_test += [test_exs]
            else:
                cons_test += [test_exs]


        misclass = 0
        for i in range(len(test_examps)):
            vj = target_val(tests[i])
            test_file = test_examps[i]
            libs_prob = []
            cons_prob = []

            for k in range(len(test_file)):
                if test_file[k] in PwvL:
                    libs_prob += [PwvL[test_file[k]]]
                if test_file[k] in PwvC:
                    cons_prob += [PwvC[test_file[k]]]

            for i in libs_prob:
                if i <= 0:
                    #print i
                    True

            vNB_l = classify_naive(Pvj_l, libs_prob)
            vNB_c = classify_naive(Pvj_c, cons_prob)

            if vNB_l > vNB_c:
                print "L"
                if vj == 0:
                    misclass += 1
            else:
                print "C"
                if vj == 1:
                    misclass += 1

        accuracy = 1 - (float(misclass)/len(test_examps))
        print "Accuracy: %.4f" % accuracy



main()
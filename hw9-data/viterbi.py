#forward.py
#Jennifer Isaza

from sys import *
import csv
from math import *
from logsum import log_sum

def get_VPs_init(pi, b, lines):
    VPs_init = {}
    for sent in lines:
        VPs_init[sent[0]] = {}
        for key in pi:
            pi_key = key
            VPs_init[sent[0]][pi_key] = log(pi[pi_key])+log(b[pi_key][sent[0]])
    return VPs_init

def get_VPs(VPs_init, sentence, trans, b):
    word = len(sentence)
    state = len(trans.keys())
    VPs = [[0 for x in range(word)] for y in range(state)]
    Qs = [[0 for x in range(word)] for y in range(state)]
    P_back = []
    keys = trans.keys()
    for w in range(word):
        maxims_word = []
        for si in range(state):
            maxims = []
            for sj in range(state):
                if w == 0:
                    VPs[sj][w] = VPs_init[sentence[w]][keys[sj]]
                    maxims_word += [VPs[sj][w]]
                    Qs[sj][w] = sj

                else:
                    VPtj = VPs[sj][w-1]
                    aji = trans[keys[sj]][keys[si]]
                    maxims += [VPtj + log(aji)]


            if w > 0:
                maxim = max(maxims)
                print maxim
                maxim_state = maxims.index(maxim)
                VPs[si][w] = maxim + log(b[keys[si]][sentence[w]])
                maxims_word += [VPs[si][w]]
                Qs[si][w] = maxim_state
        #print "maxims_word", maxims_word
    max_VP = max(maxims_word)
    max_state = maxims_word.index(max_VP)
    q_path = []
    q_path += [max_state]
    #q_path += [Qs[q_path[0]][w]]
    for w in range(len(sentence)):
        q_path += [Qs[q_path[w]][len(sentence)-w-1]]
        P_back += [q_path[w]]
        key = keys[P_back[w]]
        sentence[len(sentence)-w-1] = [sentence[len(sentence)-w-1] + '_' + key]
    print sentence
    return sentence[w]

def main():
    dev_file = argv[1]        #possible symbols in vocabulary? (V = {o0,o1,...oM-1})
    hmm_trans_file = argv[2]  #state transition probabilities  (A = {aij})
    hmm_emit_file = argv[3]   #emission probabilities per word (B = {bi(ok)})
    hmm_prior_file = argv[4]  #initial state probabilities     (Pi = {pii})

    with open(dev_file, 'rb') as dev:
        dev = csv.reader(dev, delimiter='\n', quotechar='|')
        lines = []
        for row in dev:
            words = row[0].split(' ')
            lines += [words]

    with open(hmm_trans_file, 'rb') as state_probs:
        state_probs = csv.reader(state_probs, delimiter='\n', quotechar='|')
        state_trans = {}
        for row in state_probs:
            row = row[0].split(' ')
            del row[-1]
            full = []
            for trans in row:
                full += trans.split(':')
            probs = full[1:]
            state = full[0]
            state_trans[state] = {}
            for i in range(0, len(probs)-1, 2):
                state_trans[state][probs[i]] = float(probs[i+1])

    with open(hmm_emit_file, 'rb') as em_probs:
        em_probs = csv.reader(em_probs, delimiter='\n', quotechar='|')
        ems = {}
        for row in em_probs:
            row = row[0].split(' ')
            full = []
            for word in row:
                full += word.split(':')
            probs = full[1:]
            state = full[0]
            ems[state] = {}
            for i in range(0, len(probs)-1, 2):
                ems[state][probs[i]] = float(probs[i+1])

    with open(hmm_prior_file, 'rb') as init_probs:
        init_probs = csv.reader(init_probs, delimiter='\n', quotechar='|')
        inits = {}
        for row in init_probs:
            split = row[0].split(' ')
            inits[split[0]] = float(split[1])

    VPs_init = get_VPs_init(inits, ems, lines)
    for sentence in lines:
        prob_sum = get_VPs(VPs_init, sentence, state_trans, ems)


main()
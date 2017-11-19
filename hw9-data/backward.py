#forward.py
#Jennifer Isaza

from sys import *
import csv
from math import *
from logsum import log_sum

def get_betas_init(pi, b, lines):
    betas_init = {}
    for sent in lines:
        betas_init[sent[0]] = {}
        for key in pi:
            pi_key = key
            betas_init[sent[0]][pi_key] = log(pi[pi_key])+log(b[pi_key][sent[0]])
    return betas_init

def get_betas(pi, sentence, trans, b):
    word = len(sentence)
    state = len(trans.keys())
    betas = [[0 for x in range(word)] for y in range(state)]
    keys = trans.keys()

    for w in range(word-1, -1, -1):
        for si in range(state):
            sumj = 0
            aij_list = []
            bettj_list = []
            for sj in range(state):
                if w == word-1:
                    betas[sj][w] = 0
                else:
                    bettj = betas[sj][w+1]
                    aij = trans[keys[si]][keys[sj]]
                    aij_list += [aij]
                    bettj_list += [bettj]
                    #print log(aij), b[keys[sj]][sentence[w]]
                    if sumj == 0:
                        sumj = bettj + log(aij) + log(b[keys[sj]][sentence[w+1]])
                    else:
                        sumj = log_sum(sumj, bettj + log(aij) + log(b[keys[sj]][sentence[w+1]]))
                    # sumj += bettj*aij*b[keys[sj]][sentence[w]]

            if w < word-1:
                betas[si][w] = sumj
    prob_sum = 0
    w = 0
    for val in range(len(keys)):
        #print pi[keys[val]], b[keys[val]][sentence[w]], betas[val][w]
        if prob_sum == 0:
            prob_sum = log(pi[keys[val]])+log(b[keys[val]][sentence[w]])+betas[val][w]
        else:
            prob_sum = log_sum(prob_sum, log(pi[keys[val]])+log(b[keys[val]][sentence[w]])+betas[val][w])
        # prob_sum += prob_sum*pi[keys[val]]*betas[val][w]

    return prob_sum

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

    for sentence in lines:
        prob_sum = get_betas(inits, sentence, state_trans, ems)
        print prob_sum


main()
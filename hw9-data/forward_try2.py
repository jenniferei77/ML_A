#forward.py
#Jennifer Isaza

from sys import *
import csv
from math import *
from logsum import log_sum

def get_alphas_init(pi, b, lines):
    alphas_init = {}
    #alphas_init = []
    for sent in lines:
        alphas_init[sent[0]] = {}
        for key in pi:
            pi_key = key
            alphas_init[sent[0]][pi_key] = log(pi[pi_key])+log(b[pi_key][sent[0]])
    #print alphas_init
    return alphas_init

def get_alphas(alphas_init, sentence, trans, b):
    word = len(sentence)
    state = len(trans.keys())
    alphas = [[0 for x in range(word)] for y in range(state)]
    aji_list = []
    alphtj_list = []
    bs = []
    sums = []
    keys = trans.keys()
    for w in range(word):
        for si in range(state):
            sumj = 0
            for sj in range(state):
                if w == 0:
                    alphas[sj][w] = alphas_init[sentence[w]][keys[sj]]
                else:
                    #print alph_key, alphas[word_num][alph_key], b[alph_key][word[i-1]]
                    alphtj = alphas[sj][w-1]
                    alphtj_list += [alphtj]
                    aji = trans[keys[sj]][keys[si]]
                    aji_list += [aji]
                    if sumj == 0:
                        sumj = alphtj + log(aji)
                    else:
                        sumj = log_sum(sumj, alphtj + log(aji))
            if w > 0:
                #print keys[si], sentence[w], b[keys[si]][sentence[w]], alphtj, aji, sumj
                alphas[si][w] = log(b[keys[si]][sentence[w]])+ sumj
                bs += [b[keys[si]][sentence[w]]]


    #print alphas
    prob_sum = 0
    for val in range(len(keys)):
        if prob_sum == 0:
            prob_sum = alphas[val][w]
        else:
            prob_sum = log_sum(prob_sum, alphas[val][w])
    return alphas, prob_sum

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
        #print state_trans

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
        #print inits

    alphas_init = get_alphas_init(inits, ems, lines)
    for sentence in lines:
        alphas, prob_sum = get_alphas(alphas_init, sentence, state_trans, ems)

        print prob_sum


main()
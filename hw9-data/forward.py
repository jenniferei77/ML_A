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
        # for key, value in b.items():
        #     state_probs = value
        #     #print state_probs
        #     for key in state_probs:
        #         b_key = key
        #         #print pi[pi_key], b[pi_key][b_key]
        #         alphas_init[pi_key][b_key] = pi[pi_key] * b[pi_key][b_key]
        for key in pi:
            pi_key = key
            alphas_init[sent[0]][pi_key] = pi[pi_key]*b[pi_key][sent[0]]

        # for sent in lines:
        #     alpha_sent = []
        #     for word in sent:
        #         alpha_word = pi[pi_key]*b[pi_key][word]
        #         alpha_sent += [word, alpha_word]
        #     alpha_state += [alpha_sent]
        # alphas_init += [alpha_state]
    #print alphas_init
    return alphas_init

# def summation():
#      for


def get_alphas(alphas_init, sentence, trans, b):
    alphas = {}
    alphas[sentence[0]] = {}
    word = sentence
    keys = trans.keys()
    #print keys
    for i in range(len(sentence)):
        alphtj = []
        alphas[word[i]] = {}
        for alph_key in keys:
            if i == 0:
                alphas[word[i]][alph_key] = alphas_init[word[i]][alph_key]
            else:
                print word[i-1], alph_key, alphas[word[i-1]], b[alph_key][word[i-1]]
                alphtj += [alphas[word[i-1]][alph_key]]
                aji = []
                for trans_key in keys:
                    aji += [trans[alph_key][trans_key]]

        if i > 0:
            logs = []
            for j in range(len(alphtj)-1):
                #logs += [log_sum(alphtj[j], aji[j])]
                logs += [alphtj[j]*aji[j]]
            sumj = sum(logs)
            for key in trans:
                alph_key = key
                alphas[word[i]][alph_key] = b[alph_key][word[i]]*sumj

    prob_sum = 0
    for val in keys:
        prob_sum += alphas[word[i]][val]

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
            #del row[-1]
            full = []
            for word in row:
                full += word.split(':')

            probs = full[1:]
            state = full[0]
            ems[state] = {}
            for i in range(0, len(probs)-1, 2):
                ems[state][probs[i]] = float(probs[i+1])

        #print state
        #if state == 'OT':
            #print "hi"

        #print ems['PR']['it']


    with open(hmm_prior_file, 'rb') as init_probs:
        init_probs = csv.reader(init_probs, delimiter='\n', quotechar='|')
        inits = {}
        for row in init_probs:
            split = row[0].split(' ')
            inits[split[0]] = float(split[1])
        #print inits

    alphas_init = get_alphas_init(inits, ems, lines)
    #print alphas_init
    sentence = lines[0]
    for sentence in lines:
        alphas, prob_sum = get_alphas(alphas_init, sentence, state_trans, ems)
        print prob_sum







            
























main()
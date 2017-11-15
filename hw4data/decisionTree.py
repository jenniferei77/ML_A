# decisionTree.py
# Jennifer Isaza

from sys import *
import csv
from math import *
import copy

def get_entropy_error(root):
    bin1 = root[0]
    count2 = 0
    tot = len(root)
    for i in root:
        if i != bin1:
            bin2 = i
            count2 += 1
    count1 = tot - count2

    if tot == 0:
        prob1 = 0
        prob2 = 0
    else:
        prob1 = float(count1) / tot
        prob2 = float(count2) / tot

    if count1 == 0 and count2 > 0:
        entropy = prob2 * log(1 / prob2, 2)
    elif count2 == 0 and count1 > 0:
        entropy = prob1 * log(1 / prob1, 2)
    elif count2 == 0 and count1 == 0:
        entropy = 0
    else:
        entropy = prob1 * log((1 / prob1), 2) + prob2 * log((1 / prob2), 2)

    if count1 > count2:
        error = float(count2) / tot
    else:
        error = float(count1) / tot

    return entropy, error


def only_entrop(count1, count2):
    tot = count1 + count2
    if tot > 0:
        prob1 = float(count1) / tot
        #print "prob1: ", prob1
        prob2 = float(count2) / tot
        #print "prob2: ", prob2

    if count1 == 0 and count2 > 0:
        entropy = prob2 * log(1 / prob2, 2)
        #print "in here"
    elif count2 == 0 and count1 > 0:
        entropy = prob1 * log(1 / prob1, 2)
    elif count2 == 0 and count1 == 0:
        entropy = 0
    else:
        entropy = prob1 * log((1 / prob1), 2) + prob2 * log((1 / prob2), 2)

    return entropy


def get_gain_root(col1, col2):
    root_entrop, root_error = get_entropy_error(col1)
    #print root_entrop
    if col1 == [] or col2 == []:
        return 0.0, [], [], '0', []

    # calculate H(col1,col2)
    i = 0
    pos_pose = []
    neg_pose = []
    # list of positive and negative locations in the root
    while i < len(col2):
        if col2[i] == 1:
            pos_pose += [i]
        elif col2[i] == 0:
            neg_pose += [i]

        i += 1
    #print pos_pose
    #print neg_pose
    label_pose = [pos_pose, neg_pose]
    j = 0
    pos1 = 0
    pos1_pose = []
    pos2 = 0
    pos2_pose = []
    neg1 = 0
    neg1_pose = []
    neg2 = 0
    neg2_pose = []

    # count of positive and negatives in branches
    while j < len(pos_pose):
        if col1[pos_pose[j]] == 1:
            pos1 += 1
            pos1_pose += [pos_pose[j]]
        else:
            neg1 += 1
            neg1_pose += [pos_pose[j]]
        j += 1

    k = 0
    while k < len(neg_pose):
        if col1[neg_pose[k]] == 1:
            pos2 += 1
            pos2_pose += [neg_pose[k]]
        else:
            neg2 += 1
            neg2_pose += [neg_pose[k]]
        k += 1

    pos = len(pos_pose)
    neg = len(neg_pose)
    branch1_entrop = only_entrop(pos1, neg1)
    branch2_entrop = only_entrop(pos2, neg2)
    #calculate gain
    prop1 = float(pos1 + neg1) / (pos + neg)
    prop2 = float(pos2 + neg2) / (pos + neg)
    gain = root_entrop - prop1 * branch1_entrop - prop2 * branch2_entrop
    branch1 = [pos1_pose, neg1_pose]
    branch2 = [pos2_pose, neg2_pose]
    if pos > neg:
        target_label = '+'
    else:
        target_label = '-'

    return gain, branch1, branch2, target_label, label_pose


def get_gain(col1, col2, target_att):
    root_entrop, root_error = get_entropy_error(target_att)
    #print root_entrop
    #print "get gain 2"
    if col1 == [] or col2 == []:
        return 0.0, [], [], '0', []
    # calculate H(col1,col2)
    i = 0
    pos_pose = []
    neg_pose = []
    # list of positive and negative locations in the root
    while i < len(col2):
        if col2[i] == 1:
            pos_pose += [i]
        elif col2[i] == 0:
            neg_pose += [i]

        i += 1
    label_pose = [pos_pose, neg_pose]
    j = 0
    pos1 = 0
    pos1_pose = []
    pos2 = 0
    pos2_pose = []
    neg1 = 0
    neg1_pose = []
    neg2 = 0
    neg2_pose = []

    # count of positive and negatives in branches
    while j < len(pos_pose):
        if col1[pos_pose[j]] == 1:
            if target_att[pos_pose[j]] == 1:
                pos1 += 1
                pos1_pose += [pos_pose[j]]
            else:
                neg1 += 1
                neg1_pose += [pos_pose[j]]
        else:
            if target_att[pos_pose[j]] == 1:
                pos1 += 1
                pos1_pose += [pos_pose[j]]
            else:
                neg1 += 1
                neg1_pose += [pos_pose[j]]
        j += 1

    k = 0
    while k < len(neg_pose):
        if col1[neg_pose[k]] == 0:
            if target_att[neg_pose[k]] == 1:
                pos2 += 1
                pos2_pose += [neg_pose[k]]
            else:
                neg2 += 1
                neg2_pose += [neg_pose[k]]
        else:
            if target_att[neg_pose[k]] == 1:
                pos2 += 1
                pos2_pose += [neg_pose[k]]
            else:
                neg2 += 1
                neg2_pose += [neg_pose[k]]

        k += 1

    pos = len(pos_pose)
    neg = len(neg_pose)
    branch1_entrop = only_entrop(pos1, neg1)
    branch2_entrop = only_entrop(pos2, neg2)
    prop1 = float(pos1 + neg1) / (pos + neg)
    prop2 = float(pos2 + neg2) / (pos + neg)
    gain = root_entrop - prop1 * branch1_entrop - prop2 * branch2_entrop
    branch1 = [pos1_pose, neg1_pose]
    branch2 = [pos2_pose, neg2_pose]
    if pos > neg:
        target_label = '+'
    else:
        target_label = '-'

    return gain, branch1, branch2, target_label, label_pose


def choose_best(gains):
    i = 0
    largest = 0
    while i < len(gains):
        if gains[i] > largest:
            largest = gains[i]
            new_root = i

        i += 1

    return new_root


def get_attrib(col_num, attributes):
    i = 0
    col_val = []

    while i < len(attributes):
        row = attributes[i]
        col_val += [row[col_num]]
        i += 1

    col_val = transfer(attrib_pos, col_val)

    return col_val


def transfer(pos, col):
    i = 0
    while i < len(col):
        j = 0
        while j < len(attrib_pos):
            if col[i] == attrib_pos[j]:
                pos = attrib_pos[j]
                j = len(attrib_pos)
            j += 1
        i += 1

    i = 0
    while i < len(col):
        if col[i] != pos:
            neg = col[i]
        i += 1

    i = 0
    while i < len(col):
        if col[i] == pos:
            col[i] = 1
        elif col[i] == neg:
            col[i] = 0
        i += 1
    return col


def ID3_root(names, target_att, attributes):
    global root_num
    #print attributes
    target_att = transfer(label_posit, target_att)
    j = 0
    gains = []
    branches = []
    label_pos = 0
    label_neg = 0
    largest = 0
    root_num = 0
    label_pose = 0
    #print len(attributes[0])
    while j < len(attributes[0]):
        col2 = get_attrib(j, attributes)
        gain, branch1, branch2, target_label, label_pose = get_gain_root(target_att, col2)
        gains += [gain]
        branches += [branch1, branch2]
        if gain > largest:
            largest = gain
            root_num = j
            branches = [branch1, branch2]
            label_pose = label_pose

        j += 1
    #print gains
    root_branch_y = branches[0]
    root_branch_n = branches[1]
    pos_num1 = len(root_branch_y[0])
    neg_num1 = len(root_branch_y[1])
    pos_num2 = len(root_branch_n[0])
    neg_num2 = len(root_branch_n[1])

    #print names[root_num], " = y: [%d+/%d-]" % (pos_num2, neg_num2)
    #print names[root_num], " = n: [%d+/%d-]" % (pos_num1, neg_num1)

    root = get_attrib(root_num, attributes)
    root_gain = gains[root_num]
    root_branch_y = root_branch_y[0] + root_branch_y[1]
    root_branch_n = root_branch_n[0] + root_branch_n[1]
    root_branch_y.sort()
    root_branch_n.sort()
    i = 0

    while i < len(root):
        if root[j] == 1:
            label_pos += 1
        elif root[j] == 0:
            label_neg += 1
        i += 1
    #print label_pos, len(root)-1, label_neg, root, largest
    if label_pos == len(root) - 1:
        label = '+'
        return [], [], [], [], [], [], names, names[root_num], pos_num1, neg_num1, pos_num2, neg_num2
    elif label_neg == len(root) - 1:
        label = '-'
        return [], [], [], [], [], [], names, names[root_num], pos_num1, neg_num1, pos_num2, neg_num2
    elif root == []:
        label = target_label
        return [], [], [], [], [], [], names, names[root_num], pos_num1, neg_num1, pos_num2, neg_num2
    elif largest < 0.1:
        label = target_label
        return [], [], [], [], [], [], names, names[root_num], pos_num1, neg_num1, pos_num2, neg_num2

    attribs1 = []
    pos_part = root_branch_y
    neg_part = root_branch_n
    target_att_pos = []
    target_att_neg = []
    root_pos = []
    root_neg = []
    l = 0
    while l < len(root):
        att = attributes[l]
        del att[root_num]
        attributes[l] = att
        l += 1

    k = 0
    while k < len(pos_part):
        root_pos += [root[pos_part[k]]]
        target_att_pos += [target_att[pos_part[k]]]
        attribs1 += [attributes[pos_part[k]]]
        k += 1
    #print "attribs1: ", attribs1
    #print "root_pos: ", root_pos
    #print "target pos: ", target_att_pos
    h = 0
    attribs2 = []
    #print neg_part

    while h < len(neg_part):
        root_neg += [root[neg_part[h]]]
        target_att_neg += [target_att[neg_part[h]]]
        attribs2 += [attributes[neg_part[h]]]
        h += 1
    #print "attribs2: ", attribs2
    #print "root_neg: ", root_neg
    #print "target neg: ", target_att_neg


    return attribs1, root_pos, target_att_pos, attribs2, root_neg, target_att_neg, names, names[root_num], pos_num1, neg_num1, pos_num2, neg_num2


def ID3(names, target_att, attributes, root):
    #print target_att
    j = 0
    gains = []
    branches = []
    label_pos = 0
    label_neg = 0
    largest = 0
    label_pose = 0
    rootnum = 0

    while j < len(attributes[0]):
        col2 = get_attrib(j, attributes)
        gain, branch1, branch2, target_label, label_pose = get_gain(root, col2, target_att)
        gains += [gain]
        branches += [branch1, branch2]
        if gain > largest:
            largest = gain
            rootnum = j
            branches = [branch1, branch2]

        j += 1


    root_branch_y = branches[0]
    root_branch_n = branches[1]
    pos_num1 = len(root_branch_y[0])
    neg_num1 = len(root_branch_y[1])
    pos_num2 = len(root_branch_n[0])
    neg_num2 = len(root_branch_n[1])
    root_gain = gains[rootnum]

    return names[rootnum], pos_num2, neg_num2, pos_num1, neg_num1, root_gain
    i = 0
    while i < len(root):
        if root[j] == 1:
            label_pos += 1
            #print "label pos"
        elif root[j] == 0:
            label_neg += 1
            #print "label neg"
        i += 1
    if label_pos == len(root) - 1:
        label = '+'
        return root, label
    elif label_neg == len(root) - 1:
        label = '-'
        return root, label
    elif root == []:
        label = target_label
        return root, label
    elif largest < 0.1:
        label = target_label
        return root, label

def counts(col):

    i = 0
    pos = 0
    neg = 0
    while i < len(col):
        if col[i] == 1:
            pos += 1
        else:
            neg += 1

        i += 1

    return pos, neg

def comp_signs(col1, col2):

    i = 0
    pos_pose = []
    neg_pose = []
    while i < len(col2):
        if col2[i] == 1:
            pos_pose += [i]
        elif col2[i] == 0:
            neg_pose += [i]
        i += 1


    j = 0
    pos1 = 0
    neg1 = 0
    pos2 = 0
    neg2 = 0
    while j < len(pos_pose):
        if col1[pos_pose[j]] == 1:
            pos1 += 1
        elif col1[pos_pose[j]] == 0:
            neg1 += 1

        j += 1

    k = 0
    while k < len(neg_pose):
        if col1[neg_pose[k]] == 1:
            pos2 += 1
        elif col1[neg_pose[k]] == 0:
            neg2 += 1

        k += 1

    return pos1, neg1, pos2, neg2

def change_atts(attributes):
    i = 0
    j = 0
    while j < len(attributes[0]):
        col = get_attrib(j, attributes)
        i = 0
        while i < len(attributes):
            row = attributes[i]
            row[j] = col[i]
            i += 1
        j += 1

    return attributes


def tree_test(attributes, tree, pos_num1_r, neg_num1_r, pos_num2_r, neg_num2_r, pos_num1_n, neg_num1_n, pos_num2_n, neg_num2_n, pos_num1_y, neg_num1_y, pos_num2_y, neg_num2_y, type):

    attributes = change_atts(attributes)
    total = len(attributes)

    i = 0
    i = 0
    node1_att = False
    node2n_att = False
    node2y_att = False

    while i < len(tree):

        if tree[i+1] == 'node1':
            node1_att = tree[i+2]
        if tree[i+1] == 'node2n':
            node2n_att = tree[i+2]
        elif tree[i+1] == 'node2y':
            node2y_att = tree[i+2]
        i += 3

    k = 0
    error = 0
    if pos_num1_r > neg_num1_r:
        num1_r = 1
    else:
        num1_r = 0

    if pos_num2_r > neg_num2_r:
        num2_r = 1
    else:
        num2_r = 0

    if pos_num1_n > neg_num1_n:
        num1_n = 1
    else:
        num1_n = 0

    if pos_num2_n > neg_num2_n:
        num2_n = 1
    else:
        num2_n = 0

    if pos_num1_y > neg_num1_y:
        num1_y = 1
    else:
        num1_y = 0

    if pos_num2_y > neg_num2_y:
        num2_y = 1
    else:
        num2_y = 0

    while k < len(attributes):
        row = attributes[k]

        if row[node1_att] == 1:
            if node2n_att == True:
                if row[node2n_att] == 1:
                    if row[len(row) - 1] != num1_n:

                        error += 1


                else:
                    if row[len(row) - 1] != num2_n:

                        error += 1


            else:
                if row[len(row) - 1] != num1_r:

                    error += 1

        else:
            if node2y_att == True:
                if row[node2y_att] == 1:
                    if row[len(row) - 1] != num1_y:

                        error += 1


                else:
                    if row[len(row) - 1] != num2_y:

                        error += 1


            else:
                if row[len(row) - 1] != num2_r:

                    error += 1
        k += 1


    error = float(error)/total

    return error

def main():
    global tree
    tree = []
    trainFile = argv[1]
    with open(trainFile, 'rb') as Train_data:
        Train_data = csv.reader(Train_data, delimiter=',', quotechar='|')
        rows = 0
        attributes = []
        error_attribs = []
        global target
        global attrib_pos
        global label_posit
        target = []
        for row in Train_data:
            attribs = len(row) - 1
            target += [row[attribs]]
            rows += 1
            i = 0
            att_row = []
            while i < attribs:
                att_row += [row[i]]
                i += 1
            j = 0
            error_row = []

            while j < attribs+1:
                error_row += [row[j]]
                j += 1
            attributes += [att_row]
            error_attribs += [error_row]

        names = copy.deepcopy(attributes[0])
        names_err = copy.deepcopy(attributes[0])
        m = 0
        while m < len(names):
            if names[m].startswith(' '):
                name = names[m]
                names[m] = name[1:]
            if names_err[m].startswith(' '):
                name_err = names_err[m]
                names_err[m] = name_err[1:]
            m += 1

        del error_attribs[0]
        del attributes[0]
        del target[0]
        attrib_pos = ['y', 'A', 'democrat', 'yes', 'before 1950', 'morethan3min', 'fast', 'expensive', 'high', 'Two', 'large']


        if target[0] == 'democrat' or target[0] == 'republican':
            label_posit = 'democrat'
        elif target[0] == 'A' or target[0] == 'nonA':
            label_posit = 'A'
        else:
            label_posit = target[0]

        j = 0
        posit = 0
        negat = 0
        while j < len(target):
            if target[j] == label_posit:
                posit += 1
            else:
                negat += 1

            j += 1

        attribs1, root_pos, target_att_pos, attribs2, root_neg, target_att_neg, names, root_name, pos_num1_r, neg_num1_r, pos_num2_r, neg_num2_r = ID3_root(names, target, attributes)
        tree += [root_name, "node1", root_num]

        if names != []:
            del names[root_num]
            name_n, pos_num2_n, neg_num2_n, pos_num1_n, neg_num1_n, gain_n = ID3(names, target_att_pos, attribs1, root_pos)
            k = 0
            while k < len(names_err):
                if names_err[k] == name_n:
                    count = k
                k += 1
            if gain_n > 0.1:
                tree += [name_n, "node2n", count]
            name_y, pos_num2_y, neg_num2_y, pos_num1_y, neg_num1_y, gain_y = ID3(names, target_att_neg, attribs2, root_neg)
            k = 0
            while k < len(names_err):
                if names_err[k] == name_n:
                    count = k
                   
                k += 1
            if gain_y > 0.1:
                tree += [name_y, "node2y", count]
        else:
            gain_n = 0.0
            gain_y = 0.0
        print "[%d+/%d-]" % (posit, negat)
        print root_name, " = y: [%d+/%d-]" % (pos_num1_r, neg_num1_r)


        if gain_n > 0.1:

            print " | " + name_n, " = y: [%d+/%d-]" % (pos_num1_n, neg_num1_n)
            print " | " + name_n, " = n: [%d+/%d-]" % (pos_num2_n, neg_num2_n)

        print root_name, " = n: [%d+/%d-]" % (pos_num2_r, neg_num2_r)
        if gain_y > 0.1:

            print " | " + name_y, " = y: [%d+/%d-]" % (pos_num1_y, neg_num1_y)
            print " | " + name_y, " = n: [%d+/%d-]" % (pos_num2_y, neg_num2_y)

        error_train = tree_test(error_attribs, tree, pos_num1_r, neg_num1_r, pos_num2_r, neg_num2_r, pos_num1_n, neg_num1_n, pos_num2_n, neg_num2_n, pos_num1_y, neg_num1_y, pos_num2_y, neg_num2_y, 'train')

        print "error(train): ", error_train

        testFile = argv[2]
        with open(testFile, 'rb') as Test_data:
            Test_data = csv.reader(Test_data, delimiter=',', quotechar='|')
            rows = 0
            attrib_test = []
            target_test = []
            for row in Test_data:
                attribs = len(row)
                target_test += [row[attribs - 1]]
                rows += 1
                k = 0
                att_row = []
                while k < attribs:
                    att_row += [row[k]]
                    k += 1
                attrib_test += [att_row]
            del attrib_test[0]
            del target_test[0]

        error_test = tree_test(attrib_test, tree, pos_num1_r, neg_num1_r, pos_num2_r, neg_num2_r, pos_num1_n, neg_num1_n, pos_num2_n, neg_num2_n, pos_num1_y, neg_num1_y, pos_num2_y, neg_num2_y, 'test')
        print "error(test): ", error_test

main()

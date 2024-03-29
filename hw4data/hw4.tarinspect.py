decisionTree.py                                                                                     0000664 0001750 0001750 00000050234 13166517241 014221  0                                                                                                    ustar   jennifei                        jennifei                                                                                                                                                                                                               # decisionTree.py
# Jennifer Isaza

from sys import *
import csv
from math import *


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
        print "prob1: ", prob1
        prob2 = float(count2) / tot
        print "prob2: ", prob2

    if count1 == 0 and count2 > 0:
        entropy = prob2 * log(1 / prob2, 2)
        print "in count1 = 0"
    elif count2 == 0 and count1 > 0:
        entropy = prob1 * log(1 / prob1, 2)
        print "in count2 = 0"
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
    print tot
    print count1
    print count2
    if tot > 0:
        prob1 = float(count1) / tot
        print "prob1: ", prob1
        prob2 = float(count2) / tot
        print "prob2: ", prob2

    if count1 == 0 and count2 > 0:
        entropy = prob2 * log(1 / prob2, 2)
        print "in here"
    elif count2 == 0 and count1 > 0:
        entropy = prob1 * log(1 / prob1, 2)
    elif count2 == 0 and count1 == 0:
        entropy = 0
    else:
        entropy = prob1 * log((1 / prob1), 2) + prob2 * log((1 / prob2), 2)

    return entropy


def get_gain_root(col1, col2):
    root_entrop, root_error = get_entropy_error(col1)

    print "get gain"
    print col1
    print col2

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
    print pos_pose
    print neg_pose
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
    print len(pos_pose)
    while j < len(pos_pose):
        if col1[pos_pose[j]] == 1:
            pos1 += 1
            pos1_pose += [pos_pose[j]]
        else:
            neg1 += 1
            neg1_pose += [pos_pose[j]]
        j += 1

    k = 0
    print len(neg_pose)
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
    print "enter entrop"
    branch1_entrop = only_entrop(pos1, neg1)
    branch2_entrop = only_entrop(pos2, neg2)
    # calculate gain
    # print col2
    # print pos,neg
    # print pos1,neg1
    print "root_entrop: should be 0.9963 ", root_entrop
    print "entrop1: ", branch1_entrop
    # print pos2,neg2
    print "entrop2: ", branch2_entrop
    prop1 = float(pos1 + neg1) / (pos + neg)
    print "prop1: ", prop1
    prop2 = float(pos2 + neg2) / (pos + neg)
    print "prop2: ", prop2
    gain = root_entrop - prop1 * branch1_entrop - prop2 * branch2_entrop
    print gain
    branch1 = [pos1_pose, neg1_pose]
    branch2 = [pos2_pose, neg2_pose]
    # print branch1
    # print branch2
    if pos > neg:
        target_label = '+'
    else:
        target_label = '-'

    return gain, branch1, branch2, target_label, label_pose


def get_gain(col1, col2, target_att):
    print "root col: ", col1
    root_entrop, root_error = get_entropy_error(target_att)

    print "get gain 2"
    print col1
    print col2
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
    print pos_pose
    print neg_pose
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
    print len(pos_pose)
    print target_att
    print col1
    while j < len(pos_pose):
        if col1[pos_pose[j]] == 1:
            if target_att[pos_pose[j]] == 1:
                pos1 += 1
                pos1_pose += [pos_pose[j]]
            else:
                neg1 += 1
                neg1_pose += [pos_pose[j]]
                print "in here"
        else:
            if target_att[pos_pose[j]] == 1:
                pos1 += 1
                pos1_pose += [pos_pose[j]]
            else:
                neg1 += 1
                neg1_pose += [pos_pose[j]]
                print "in here"

        j += 1

    k = 0
    print len(neg_pose)
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
    print "enter entrop 2"
    branch1_entrop = only_entrop(pos1, neg1)
    branch2_entrop = only_entrop(pos2, neg2)
    # calculate gain
    # print col2
    # print pos,neg
    # print pos1,neg1
    print "root_entrop 2: ", root_entrop
    print "entrop1 2: ", branch1_entrop
    # print pos2,neg2
    print "entrop2 2: ", branch2_entrop
    prop1 = float(pos1 + neg1) / (pos + neg)
    print "prop1 2: ", prop1
    prop2 = float(pos2 + neg2) / (pos + neg)
    print "prop2 2: ", prop2
    gain = root_entrop - prop1 * branch1_entrop - prop2 * branch2_entrop
    print gain
    branch1 = [pos1_pose, neg1_pose]
    branch2 = [pos2_pose, neg2_pose]
    # print branch1
    # print branch2
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
        col_val += row[col_num]
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
    print col
    return col


def ID3_root(names, target_att, attributes):
    global root_num

    print target_att
    target_att = transfer(label_posit, target_att)
    j = 0
    gains = []
    branches = []
    label_pos = 0
    label_neg = 0
    largest = 0
    root_num = 0
    label_pose = 0
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

    # print root_num
    print gains
    print branches
    print label_pose

    # root_num = choose_best(gains)
    root_branch_y = branches[0]
    root_branch_n = branches[1]
    # print root_branch
    pos_num1 = len(root_branch_y[0])
    neg_num1 = len(root_branch_y[1])
    pos_num2 = len(root_branch_n[0])
    neg_num2 = len(root_branch_n[1])
    print root_branch_y
    print root_branch_n

    print names[root_num], " = y: [%d+/%d-]" % (pos_num2, neg_num2)
    print names[root_num], " = n: [%d+/%d-]" % (pos_num1, neg_num1)

    root = get_attrib(root_num, attributes)
    # root = transfer(label_posit, root)
    root_gain = gains[root_num]
    # print root_num
    root_branch_y = root_branch_y[0] + root_branch_y[1]
    root_branch_n = root_branch_n[0] + root_branch_n[1]
    root_branch_y.sort()
    root_branch_n.sort()
    print root_branch_y
    print root_branch_n
    i = 0
    print "print root: ", root
    while i < len(root):
        if root[j] == 1:
            label_pos += 1
            print "label pos"
        elif root[j] == 0:
            label_neg += 1
            print "label neg"
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
    elif gain < 0.1:
        label = target_label
        return root, label

    attribs1 = []
    pos_part = root_branch_y
    # print pos_part
    neg_part = root_branch_n
    # print neg_part
    # print attributes[pos_part[0]]
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

    print attributes
    k = 0
    print pos_part
    while k < len(pos_part):
        root_pos += [root[pos_part[k]]]
        target_att_pos += [target_att[pos_part[k]]]
        attribs1 += [attributes[pos_part[k]]]
        k += 1
    print "attribs1: ", attribs1
    print "root_pos: ", root_pos
    print "target pos: ", target_att_pos
    h = 0
    attribs2 = []
    print neg_part
    while h < len(neg_part):
        root_neg += [root[neg_part[h]]]
        target_att_neg += [target_att[neg_part[h]]]
        attribs2 += [attributes[neg_part[h]]]
        h += 1
    print "attribs2: ", attribs2
    print "root_neg: ", root_neg
    print "target neg: ", target_att_neg

    return attribs1, root_pos, target_att_pos, attribs2, root_neg, target_att_neg, names, names[
        root_num], pos_num1, neg_num1, pos_num2, neg_num2


def ID3(names, target_att, attributes, root):
    print target_att
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
            label_pose = label_pose

        j += 1

        # if gain == 0.0 and branch1 == [] and branch2 == [] and target_label == '0' and label_pose == []:
        #   return 'none', 0, 0, 0, 0, 0.0

    # print rootnum
    print gains
    print branches
    print label_pose

    # rootnum = choose_best(gains)
    root_branch_y = branches[0]
    root_branch_n = branches[1]
    # print root_branch
    pos_num1 = len(root_branch_y[0])
    neg_num1 = len(root_branch_y[1])
    pos_num2 = len(root_branch_n[0])
    neg_num2 = len(root_branch_n[1])
    # print names
    print "root num: ", rootnum
    root_gain = gains[rootnum]

    return names[rootnum], pos_num2, neg_num2, pos_num1, neg_num1, root_gain
    print names[rootnum], pos_num1, neg_num1
    print names[rootnum], pos_num2, neg_num2
    root = get_attrib(rootnum, attributes)
    # root = transfer(label_posit, root)
    # print rootnum
    i = 0
    print "print root: ", root
    while i < len(root):
        if root[j] == 1:
            label_pos += 1
            print "label pos"
        elif root[j] == 0:
            label_neg += 1
            print "label neg"
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
    elif gain < 0.1:
        label = target_label
        return root, label


        # if root_gain > 0.1:

        # leaf1, label1 = ID3(names, target_att_pos, attribs1, root_pos)
        #    leaf2, label2 = ID3(names, target_att_neg, attribs2)


def error(pos1, pos2, pos3, pos4, neg1, neg2, neg3, neg4):
    error = (pos1 + pos2 + pos3 + pos4) / (neg1 + neg2 + neg3 + neg4)

    return error

def change_atts(attributes):

    i = 0
    while i < len(attributes):
        j = 0
        while j < len(attributes[0]):
            row = attributes[i]
            k = 0
            while k < len(attrib_pos):
                if row[j] == attrib_pos[k]:
                    row[j] = 1
                    k = len(attrib_pos)
                else:
                    row[j] = 0
                k += 1
            attributes[i] = row
            j += 1
        i += 1
    return attributes

def tree_test(attributes, target, tree, names):

    attributes = change_atts(attributes)

    i = 0
    node1_att = 0
    node2n_att = 0
    node2y_att = 0
    while i < len(tree):
        j = 0
        while j < len(names):
            if tree[i] == names[j] and tree[i + 1] == 'node1':
                node1_att = j
            if tree[i] == names[j] and tree[i + 1] == 'node2n':
                node2n_att = j
                print node2n_att
            if tree[i] == names[j] and tree[i + 1] == 'node2y':
                node2y_att = j
            j += 1
        i += 1

    root = get_attrib(node1_att, attributes)
    target = transfer(target)
    target_pos, target_neg = counts(target)
    print "[%d+/%d-]" % (target_pos, target_neg)

    pos1r, neg1r, pos2r, neg2r = comp_signs(target, root)
    print names[node1_att], " = y: [%d+/%d-]" % (pos1r, neg1r)
    print names[node1_att], " = n: [%d+/%d-]" % (pos2r, neg2r)
    node_n = 0
    node_y = 0
    if tree[len(tree) - 1] == 'node2n' or tree[len(tree) - 3] == 'node2n':
        node2n = get_attrib(node2n_att, attributes)
        pos1n, neg1n, pos2n, neg2n = comp_signs(node2n, root)
        pos1n, neg1n, pos2n, neg2n = comp_signs(target, node2n)
        print " | " + names[node2n_att], " = y: [%d+/%d-]" % (pos1n, neg1n)
        print " | " + names[node2n_att], " = n: [%d+/%d-]" % (pos2n, neg2n)
        node_n = 1

    if tree[len(tree) - 1] == 'node2y' or tree[len(tree) - 3] == 'node2y':
        node2y = get_attrib(node2y_att, attributes)
        pos1y, neg1y, pos2y, neg2y = comp_signs(node2y, root)
        pos1y, neg1y, pos2y, neg2y = comp_signs(target, node2y)
        print " | " + names[node2y_att], " = y: [%d+/%d-]" % (pos1y, neg1y)
        print " | " + names[node2y_att], " = n: [%d+/%d-]" % (pos2y, neg2y)
        node_y = 1
        
    i = 0
    j = 0
    k = 0
    while k < len(target):
        row = attributes[k]
        if row[node1_att] == 1:
            if node_n == 1:
                if row[node2n_att] == 1:
                    if row[len(row) - 1] == label_posit:
                        pos_branch += 1
                    else:
                        error += 1
                else:
                    if row[len(row) - 1] == label_posit:
                        error += 1
                    else:
                        neg_branch += 1
            else:
                if row[len(row) - 1] == label_posit:
                    error += 1



        else:
            if node_y == 1:
                if row[node2y_att] == 1:
                    if row[len(row) - 1] == label_posit:
                        pos += 1
                    else:
                        error += 1
                else:
                    if row[len(row) - 1] == label_posit:
                        error += 1
                    else:
                        neg += 1
            else:
                if row[len(row) - 1] == label_posit:
                    error += 1

        k += 1



def main():
    global tree
    tree = []
    trainFile = argv[1]
    with open(trainFile, 'rb') as Train_data:
        Train_data = csv.reader(Train_data, delimiter=',', quotechar='|')
        rows = 0
        attributes = []
        global target
        global attrib_pos
        global label_posit
        target = []
        for row in Train_data:
            attribs = len(row) - 1
            target += [row[attribs]]
            rows += 1
            # print label
            i = 0
            att_row = []
            while i < attribs:
                att_row += [row[i]]
                i += 1
            attributes += [att_row]

        names = attributes[0]
        del attributes[0]
        # print attributes
        del target[0]
        # print label
        # print attributes
        attrib = attributes[0]
        attrib_pos = attrib_pos = ['y', 'A', 'democrat', 'yes', 'before 1950', 'morethan3min', 'fast', 'expensive', 'high', 'Two', 'large']

        if target[0] == 'democrat' or target[0] == 'republican':
            label_posit = 'democrat'
        elif target[0] == 'A' or target[0] == 'nonA':
            label_posit = 'A'
        else:
            label_posit = target[0]

        print "attrib pos: ", attrib_pos
        print "label posit: ", label_posit

        j = 0
        posit = 0
        negat = 0
        while j < len(target):
            if target[j] == label_posit:
                posit += 1
            else:
                negat += 1

            j += 1

        attribs1, root_pos, target_att_pos, attribs2, root_neg, target_att_neg, names, root_name, pos_num1_r, neg_num1_r, pos_num2_r, neg_num2_r = ID3_root(
            names, target, attributes)

        del names[root_num]

        name_n, pos_num2_n, neg_num2_n, pos_num1_n, neg_num1_n, gain_n = ID3(names, target_att_pos, attribs1, root_pos)
        name_y, pos_num2_y, neg_num2_y, pos_num1_y, neg_num1_y, gain_y = ID3(names, target_att_neg, attribs2, root_neg)

        print root_num
        print "[%d+/%d-]" % (posit, negat)
        print root_name, " = y: [%d+/%d-]" % (pos_num1_r, neg_num1_r)
        tree += [root_name, "node1"]

        # if name_n != 'none' and pos_num2_n != 0 and neg_num2_n != 0 and pos_num1_n != 0 and neg_num1_n != 0:
        if gain_n > 0.1:
            tree += [name_n, "node2n"]
            print " | " + name_n, " = y: [%d+/%d-]" % (pos_num1_n, neg_num1_n)
            print " | " + name_n, " = n: [%d+/%d-]" % (pos_num2_n, neg_num2_n)
        print root_name, " = n: [%d+/%d-]" % (pos_num2_r, neg_num2_r)
        # if name_y != 'none' and pos_num2_y != 0 and neg_num2_y != 0 and pos_num1_y != 0 and neg_num1_y != 0:
        if gain_y > 0.1:
            tree += [name_y, "node2y"]
            print " | " + name_y, " = y: [%d+/%d-]" % (pos_num1_y, neg_num1_y)
            print " | " + name_y, " = n: [%d+/%d-]" % (pos_num2_y, neg_num2_y)




        # node = get_attrib(root_num, attributes)
        # entropy_train, error_train = get_entropy_error(node)
        # print error_train

        # error_train = error(pos_num1_y, pos_num2_y, pos_num1_n, pos_num2_n, neg_num2_y, neg_num1_y, neg_num2_n, neg_num1_n)

        # print error_train
        print tree

        testFile = argv[2]
        with open(testFile, 'rb') as Test_data:
            Test_data = csv.reader(Test_data, delimiter=',', quotechar='|')
            rows = 0
            attributes = []
            target = []
            for row in Test_data:
                attribs = len(row)
                target += [row[attribs - 1]]
                rows += 1
                # print label
                k = 0
                att_row = []
                while k < attribs:
                    att_row += [row[k]]
                    k += 1
                attributes += [att_row]

            names = attributes[0]
            del attributes[0]
            # print attributes
            del target[0]
            # print label
            # print attributes

        tree_test(attributes, target, tree, names)












main()
                                                                                                                                                                                                                                                                                                                                                                    Q0.txt                                                                                              0000664 0001750 0001750 00000001572 13165476475 012270  0                                                                                                    ustar   jennifei                        jennifei                                                                                                                                                                                                               A decision tree would work for the political party information, because there are multiple attributes that are not known to affect the affiliation or not. Out of these multiple attributes, there are most likely only a few attributes that actually do accurately tell the user about any party outcome. Since there would only be a few useful attributes out of many unuseful ones, a decision tree would work.

However, a decision tree would not work well for the educational information, since there are so many known attributes that all contribute to the student grades. A collective view of all the attributes are needed in order to arrive at an average grade, so all of them are important and not a single one is probably a tell-tale sign as to if the student gets an A or not. Therefore, a decision tree would not be the best method to use in order to see what grade the student receives. 
                                                                                                                                      Q1_education.txt                                                                                    0000664 0001750 0001750 00000000476 13165501701 014303  0                                                                                                    ustar   jennifei                        jennifei                                                                                                                                                                                                               The valuable education variables are more difficult to predict, since they are very scattered in terms of nonA and A results. Based off of the data, the final is the most telling attribute for if the student receives an A. The other attribute that may be valuable is M4, since only eight nonA students received an A. 
                                                                                                                                                                                                  Q1_politicians.txt                                                                                  0000664 0001750 0001750 00000001031 13165501260 014632  0                                                                                                    ustar   jennifei                        jennifei                                                                                                                                                                                                               Q1

The most useful variables in the policial party data will be Export_south_africa in order to tell if the person is a democrat and Superfund_right_to_sue in order to tell if the person is a republican. The Export_south_africa issue only has one 'no' answer recorded by a democrat, and the Superfund_right_to_sue issue only has two 'no' answers recorded by republicans. Although the opposite cannot be said (all yes from republicans or all yes from democrats), these two variables will help predict results in a decision tree format. 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       Q2.txt                                                                                              0000664 0001750 0001750 00000000006 13166517651 012252  0                                                                                                    ustar   jennifei                        jennifei                                                                                                                                                                                                               1.000
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          Q3.txt                                                                                              0000664 0001750 0001750 00000000006 13166517676 012262  0                                                                                                    ustar   jennifei                        jennifei                                                                                                                                                                                                               0.918
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          Q4.txt                                                                                              0000664 0001750 0001750 00000000006 13166517715 012255  0                                                                                                    ustar   jennifei                        jennifei                                                                                                                                                                                                               0.541
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          Q5.txt                                                                                              0000664 0001750 0001750 00000000006 13166517732 012255  0                                                                                                    ustar   jennifei                        jennifei                                                                                                                                                                                                               1.000
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          Q6.txt                                                                                              0000664 0001750 0001750 00000000002 13166517743 012254  0                                                                                                    ustar   jennifei                        jennifei                                                                                                                                                                                                               B
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              Q7.txt                                                                                              0000664 0001750 0001750 00000000002 13166517755 012260  0                                                                                                    ustar   jennifei                        jennifei                                                                                                                                                                                                               X
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              Q8.txt                                                                                              0000664 0001750 0001750 00000000002 13166517764 012261  0                                                                                                    ustar   jennifei                        jennifei                                                                                                                                                                                                               3
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              Q9.txt                                                                                              0000664 0001750 0001750 00000000002 13166517773 012262  0                                                                                                    ustar   jennifei                        jennifei                                                                                                                                                                                                               2
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              Q10.txt                                                                                             0000664 0001750 0001750 00000000000 13166517534 012323  0                                                                                                    ustar   jennifei                        jennifei                                                                                                                                                                                                               collaboration.txt                                                                                   0000664 0001750 0001750 00000000000 13166520020 014572  0                                                                                                    ustar   jennifei                        jennifei                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
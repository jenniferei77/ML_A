# python hw4 inspect.py
# Jennifer Isaza
# calculate the label entropy at the root and the error rate of classifying using a majority vote 

from sys import *
import csv
from math import *



def get_entropy_error(root):
	
	del root[0]
	bin1 = root[0]
	count2 = 0
	tot = len(root)
	for i in root:
		if i != bin1:
			bin2 = i
			count2 += 1
	count1 = tot-count2
	entropy = float(count2)/tot *(log(float(tot)/count2,2)) + float(count1)/tot*(log(float(tot)/count1,2))
	if count1 > count2:
		error = float(count2)/tot
	else:
		error = float(count1)/tot
	return(entropy,error)
	


def main():
	infile = argv[1]
	root = []
	with open(infile, 'rb') as in_data:
		in_data = csv.reader(in_data, delimiter=',', quotechar='|')
		for row in in_data:
			attributes = len(row) - 1	
			root += [row[attributes]]
		
	entropy,error = get_entropy_error(root)
	print "entropy:", entropy
	print "error:", error


main()


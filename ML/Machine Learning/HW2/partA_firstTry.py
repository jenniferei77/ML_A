# python hw2 partA.py
# Jennifer Isaza

from __future__ import print_function
from sys import *


def size():
	#1
	size_inSpace = 2**9	
	print(size_inSpace)
	#2
	size_conSpace = 2**size_inSpace
	conspace = size_conSpace
	digits = 0
	while (conspace > 0):
		conspace = conspace/10
		digits += 1
	print(digits)
	#3
	hypSpace3 = 3**9+1
	print(hypSpace3)
	
	#4
	hypSpace4 = 3**10+1
	print(hypSpace4)

	#5
	hypSpace5 = 4*(3**8)+1
	print(hypSpace5)

def Find_S(infile,current_hyp,run):
	file_list = []
	outfile = open('partA6.txt','a')
	#Read file and make list
	#file_read = infile.readline()
	#file_list = file_list.append(file_read)
	#print(file_list)
	count = 0
	#current_hyp = ['null','null','null','null','null','null','null','null','null']
	first_low = 0
	for line in infile:
		file_list.append(line)
		line_count = file_list[count]
		line_count = line_count.replace(' ','\t')
		line_count = line_count.replace('\r\n','')
		#print(line_count)
		full_line = line_count.split('\t')
		#print(full_line)
		options = 1
		distinct_line = []
		while options < 20:
			distinct_line.append(full_line[options])
			#print(distinct_line)
			#print(options)
			options += 2
		#print(distinct_line)
		if distinct_line[9] =='high'and first_low == 1:
			for i in range(len(current_hyp)):
				if current_hyp[i] != distinct_line[i]:
					current_hyp[i] = '?'
					#print(current_hyp)
		if first_low == 0 and distinct_line[9] == 'high':
			first_low = 1
			#print(distinct_line)
			print(current_hyp)
			if current_hyp == ['null','null','null','null','null','null','null','null','null']:
				current_hyp = distinct_line
				current_hyp.remove('high')
			#print(current_hyp)
		#print("run = ",run)
		#if run == 0:
		#print(run)
		if count%30 == 0:
			#for i in range(len(current_hyp)):
				#out_line = str(current_hyp[i]+'\t')
			out_line = ('\t').join(current_hyp)
			#print(out_line)	
				#print(out_line)
			#outfile = open('partA6.txt','a')
			outfile.write(out_line)
			outfile.write('\n')

		count += 1
	run += 1
	return(current_hyp,run)
	

def main():
	#Print hardcoded answers 1-5
	size()
	
	#Run the Find-S algorithm on 9Cat-Train.labeled
	#Open input file to read
	run = 0
	CatTrained = argv[1]
	CatTrained = open(CatTrained,'r')
	current_hyp = ['null','null','null','null','null','null','null','null','null']
	[current_hyp,run] = Find_S(CatTrained,current_hyp,run)
	

	print('=====================================================================')

	#Apply final hyp to 9Cat-Dev.labeled
	#Open input file to read
	CatDev = open('9Cat-Dev.labeled','r')
	hyp1 = current_hyp
	print(hyp1)
	[current_hyp,run] = Find_S(CatDev,current_hyp,run)
	hyp2 = current_hyp
	print(hyp2)
	misclass_rate = 0
	for i in range(len(current_hyp)):
		if hyp1[i] == hyp2[i]:
			misclass_rate += (1.0/9)
	print(misclass_rate)
	
	CatDev.close()
	CatTrained.close()
	
	
		


	
		
main()


# python hw2 partB.py
# Jennifer Isaza

from binascii import *
from sys import *
def size():
	#size of input space	
	inSpace_size = 2**4
	print(inSpace_size)
	
	#size of concept space
	conSpace_size = 2**inSpace_size
	print(conSpace_size)

def List_Then_Elim(infile):
	file_list = []
	count = 0
	data = []
	list_of_lists = []
	for line in infile:
		file_list.append(line)
		line_count = file_list[count]
		line_count = line_count.replace(' ','\t')
		line_count = line_count.replace('\r\n','')
		full_line = line_count.split('\t')
		options = 1
		distinct_line = []
		while options < 10:
			distinct_line.append(full_line[options])
			options += 2
		if distinct_line[0] == 'Male':
			distinct_line[0] = 1
		else:
			distinct_line[0] = 0
		if distinct_line[1] == 'Young':
			distinct_line[1] = 1
		else:
			distinct_line[1] = 0
		if distinct_line[2] == 'Yes':
			distinct_line[2] = 1
		else:
			distinct_line[2] = 0
		if distinct_line[3] == 'Yes':
			distinct_line[3] = 1
		else:
			distinct_line[3] = 0
		if distinct_line[4] == 'low':
			distinct_line[4] = 1
		else:
			distinct_line[4] = 0
		
		data.append(distinct_line[4])
		list_of_lists.append(distinct_line)
		count += 1
	version_space = []
	for i in range(0,65536):
		binary = "{0:b}".format (i)
		if len(binary) < 16:
			zeros = 16 - len(binary)
			binary = "0"*zeros + binary
		hyps = []
		for a in range(16):
			hyps.append(int(binary[a]))
		match = 0
		for b in range(len(data)):
			if data[b] == hyps[b]:
				match += 1
		if match == len(data):
			version_space.append(hyps)
	return(version_space,list_of_lists)

def check_missing(indata):
	space = []
	missing = []
	for i in range(0,2**4):
		binary = "{0:b}".format (i)
		if len(binary) < 4:
			zeros = 4 - len(binary)
			binary = "0"*zeros + binary
		hyps = []
		for a in range(4):
			hyps.append(int(binary[a]))
		space.append(hyps)		
	full_space = space
	for i in range(0,2**4):
		for a in range(len(indata)-1):
			
			for b in range(len(space)-1):
				if indata[a] == space[b]:
					space.remove(indata[a])
	
	
	return(full_space)

def full_compare(version_space,full_space,test_case):
	del test_case[4]
	high = 0
	low = 0
	for i in range(len(version_space)):
		hyp = version_space[i]
		comp_space = full_space
		for j in range(len(version_space[i])):
			risk = hyp[j]
			if test_case == comp_space[j]:
				if risk == 1:
					high += 1
				else:
					low += 1	

	return(high,low)
				
def main():
	#sizes for partB 1-2
	size()
	CatTrained = open('4Cat-Train.labeled','r')
	[version_space1, indata1] = List_Then_Elim(CatTrained)

	#partB 3: size of final version space
	print(len(version_space1))
	infile = argv[1]
	infile = open(infile,'r')
	[version_space2,indata2] = List_Then_Elim(infile)

	#partB 4: voting results
	full_space = check_missing(indata2)
	for i in range(len(indata2)):
		[high,low]=full_compare(version_space1,full_space,indata2[i])
		print(str(high) + ' ' + str(low))
	
				

main()
	

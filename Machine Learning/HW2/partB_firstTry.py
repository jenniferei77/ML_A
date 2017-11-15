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


def main():
	#sizes for partB 1-2
	size()
	
	#read file
	CatTrained = argv[1]
	CatTrained = open(CatTrained,'r')
	infile = CatTrained
	file_list = []
	count = 0
	data = []
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
	#partB 3: size of final version space
	print(len(version_space))
	highs = 0
	lows = 0
	for i in range(len(data)):
		if data[i] == 0:
			highs += 1
		else:
			lows += 1
	#partB 4: print line of highs and lows per input set
	print(str(highs) + ' ' + str(lows))
				

main()
	

# python hw1b.py
# Jennifer Isaza
# program prints the lines of a file in reverse order to standard input.

import sys

def reverse():
    # Open input.txt for reading
    infile = sys.argv[1]
    infile = open(infile, 'r')
    file_list = []
    reverse_list = []
    # Read file and make list
    for line in infile:
        line = line.replace('\n','')
        file_list.append(line)
    # Reverse list and join 
    for i in range(len(file_list)):
    	reverse_list = [file_list[i]] + reverse_list
    rev = "\n".join(reverse_list)

    # Close file
    infile.close()
    return(rev)
    
    
    

def main():

    rev = reverse()
    print(rev)

main()
    

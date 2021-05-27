import argparse
import csv
import itertools
import random
import string
import os
import sys

#### ==== Arguments ==== ####

parser = argparse.ArgumentParser(description ='Generator of Random data.')
parser.add_argument('-k', default = 'keyFile.txt',
	help = 'File containing a space-separated list of key names and their data types that \
	could potentially be used for data generation. Defaults to "keyFile.txt".')
parser.add_argument('-n', type = int,
	help = 'Number of lines, i.e. number of separate instances of data, to be generated.')
parser.add_argument('-d', type = int,
	help = 'Maximum level of nesting, i.e. how many times in a line a value can have a set of ​key : values. \
	Zero means no nesting, i.e. there is only one set of key-values per line (in the value of the high level key.)')
parser.add_argument('-m', type = int,
	help = '​Maximum number of keys inside each value.')
parser.add_argument('-l', type = int, 
	help = '​Maximum length of a string value whenever a string value is generated. \
	Strings are comprised of letters (upper and lowercase) or numbers, not symbols. \
	E.g., setting "-l 4" means that we can generate strings of length up to 4 (e.g. “ab”, “abcd”, “a”), \
	but not an empty string.')

parser._parse_known_args(sys.argv[1:], argparse.Namespace())
args = parser.parse_args()

#### ==== Auxiliary Functions ==== ####

def populateKey(key, d, l, m):
    
    # Initialization of dictionary
    ins_dict = {}

    # Randomizing number of keys inside the value
    numValues = int(round(random.random()*m, 0))
    # Randomizing selection of keys
    combTmp = list(itertools.combinations(range(numKeys), numValues))
    keysTmpInd = random.randint(1, len(combTmp))
    keysTmp = combTmp[keysTmpInd-1]

    for i in range(numValues):

    	# Randomizing maximum nesting level per key
        nest_chance = int(round(random.random()*d, 0))

        key_tmp = lines[keysTmp[i]][0] # key "name", from keyFile.txt
        val_type_tmp = lines[keysTmp[i]][1] # key type, from keyFile.txt

        if nest_chance == 0:

        	# Assigning values to the keys - Random generation

            if val_type_tmp == "string":
                lenString = int(1+round(random.random()*(l-1), 0))
                val_tmp = ''.join(random.choice(alphabet) for i in range(lenString))

            # Different criteria were used for generating numeric values
            ## so that the values "make sense", e.g. not have a height of 354
            elif val_type_tmp == "int":
                if key_tmp == "age":
                    val_tmp = int(round(random.random()*120, 0))
                elif key_tmp == "postal_code":
                    val_tmp = int(round(random.random()*100000, 0))
                elif key_tmp == "address_no":
                    val_tmp = int(round(random.random()*200, 0))

            elif val_type_tmp == "float":
                if key_tmp == "height":
                    val_tmp = round(random.uniform(0.5,2), 2)
                elif key_tmp == "weight":
                    val_tmp = round(random.uniform(3,200), 2)
                else:
                    val_tmp = round(random.uniform(1,100), 2)
            
        # Recursively populating the dictionary if the nesting level is greater than 0
        elif nest_chance > 0:
            
            nest_ch_tmp = int(nest_chance-1)
            val_tmp = populateKey(key_tmp, nest_ch_tmp, l, m)
            
        ins_dict[key_tmp] = val_tmp

    return ins_dict


#### ==== Data Generation ==== ####

# Reading keyFile.txt
lines = []
with open(args.k, 'r') as f:
	lines = [[str(x) for x in line.split()] for line in f]
numKeys = len(lines)
# Sanity Check
if args.m > numKeys:
    print("Number of keys inside a value (argument m) exceeds number of possible key-values.")
    print("Duplications are not allowed.")
    sys.exit("Aborting Mission...")

# String "alphabet", containing upper- and lower-case letters, and numbers
alphabet = string.ascii_letters + string.digits

# Writing randomly generated data to file, dataToIndex.txt
fileName = 'dataToIndex.txt'
f = open(fileName, "w")
rand_dict = {}

for x in range(1, args.n+1):

    key_tmp = "key"+str(x) # setting high-level keys as key1, key2, etc.
    rand_dict[key_tmp] = populateKey(key_tmp, args.d, args.l, args.m)

    f.write("'key" + str(format(x)) + str("':")  + str(rand_dict[key_tmp]) + "\n")
    
f.close()






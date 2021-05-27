# simple-kv-database
The purpose of this project is to create a simple version of a distributed, fault-tolerant, Key-Value (KV) database (or store).

## 📗 Introduction

A Key-Value Database or Key-Value store is defined as a data storage paradigm designed for storing, retrieving, and managing associative arrays. In general, KV systems treat the data as a single opaque collection, which may have different fields for every record. These implementations often use less memory, and are used extensively in cloud computing. The most common data structure used in this frame include hash tables or dictionaries. The data stored inside the data structures, i.e. inside the dictionary, can be stored and retrieved using a key that uniquely identifies the record.

In the frame of this project, the Trie data structure will be used. A Trie is also known as a digital or prefix tree, which means that Tries are a type of search trees. Tree data structures are used for locating specific keys from within a set, and in such structures there exist links between nodes that are defined not by the entire key but by individual characters. To access a particular key, that is to recover its value, change it, or remove it, the trie is traversed depth-first by following the links between nodes.

## 🔑 Prerequisites

Please make sure that you have **Python 3.8.3** (or greater) installed on your computer. It possible that the implementation will run with other versions of Python.

Also, please make sure that the following libraries are installed and up-to-date:
* argparse
* socket
* sys
* os
* random
* itertools
* json
* csv
* string

## ⌨️ Data Creation

The KV Store to e created can index data of arbitrary length and arbitrary nesting of the form: `key:value`. In this case, key represents the key of the data that we care to store and value is the payload (or value) of the data that we want to store for that key. The value can also contain a set of `key:value` pairs. The maximum number of instances of the `key:value` -type of values inside a high-level (top) key is referred to as the nesting level; that is the maximum times a value can take the form of a `key:value` pair, e.g. in the form of nested dictionaries.

### Criteria for Data Generation

The following criteria and approaches are taken into account during the data creation step:
* The randomization in generating the data was the priority of this step. Combina- tions of key names were chosen at random, and the same applies for the number of values in each level, the nesting level of a specific value, the length of a string, and the integer and float values assigned to a certain key.
* Same-level keys should not contain have the same name.
  1. Each key, high-level or sub-key, can only be of type string.
  2. High-level keys are of the form ”key1”, ”key2”, etc., to enable easier debugging.
  3. High-level keys can either have an empty value, or a value with key:value pairs, up to the maximum level of nesting allowed.
* Individual values can be integers, floats, or strings, or an empty set of key:value pairs.
  1. String values can have up to a specific number of characters (user-defined parameter), but not be an empty string. String values include upper- and lower-case letters, as well as numbers.
  2. Integer and float values were ”tweaked” to make more sense, e.g. age or postal code, although in general the randomization of data was the foremost priority, and the majority of values will not make sense.

### The keyFile.txt auxiliary file

A two-column auxiliary file containing the plausible key names (1st column) along with their types (2nd column) is used in order to generate the random data. These key names refer only to low-level key names, not the high-level ones.
The keyFile.txt is supplied as argument in the python script to generate the random data. The program defaults to the keyFile.txt file already provided, but the user can potentially use their own file.

### 👟 Running

A python script was created for the data generation step. The following arguments need to be supplied in order for the script to run and output the desired results:

* **−k** : Defining the keyFile, the file containing the space-separated list of key names and their data types that could potentially be used for key generation (See section above). This argument defaults to the keyFile.txt already provided in the frame of this project.
* **−n** : Number of lines, i.e. number of separate instances of data, to be generated
* **−d** : Maximum level of nesting, i.e. how many times a value take the key:value form. Zero means no nesting, i.e. there is only one set of key-values for the high-level key.
* **−m** : Maximum number of keys inside each value. This may include a zero value, which leads to an empty set of key:value pairs.
* **−l** : Maximum length of a string value whenever a string value is generated. Strings are comprised of letters (upper and lowercase) or numbers, not symbols. Generation of an empty string is not permitted.

The arguments above are supplied by the user, while those having a default value could be omitted; the scripts parses the arguments so that they could be used downstream.

An auxiliary function, *populateKey*, was implemented for the generation of the random data. This function is used to create values and assign them to a specified key. This function takes into account all the factors for generating the data randomly:
* The number of values to be included per high-level key are selected at random, ranging from 0 (empty set) to m. This hold for all the sub-keys as well.
* The sub-key names and types are drawn from the keyFile.txt, chosen at random all the while not allowing for duplicated keys in the same level.
* The nesting level of each value is selected at random, ranging from 0 to d for the keys being assigned as values to the high-level key. For each subsequent level of keys, the potential maximum nesting level is decreased by one, and the process is repeated through recursion until all high-level and sub-keys are assigned values or sets of values.
* The maximum string length for values of type string is selected at random, ranging from 1 to l. The characters -letters or numbers- that will build the string are also chosen at random.
* The above processes are incorporated until all n keys have been populated.
The output of the script is written to the *dataToIndex.txt* file, to be used downstream by the KV System.

#### How to run:

```
python3 createData.py -k {keyFile.txt} 
					  -n {number of lines of data} 
					  -l {max string length} 
					  -m {max keys inside value} 
					  -d {max nesting level}
```

#### Example

```
python3 createData.py -n 1000 -l 5 -m 5 -d 3
```

#### Help

```
python3 createData.py --help
```

**Note**: The -k argument can be omitted. A *keyFile.txt* has been provided with the code, and it has been set to the default. However, if the user wishes to use their own *keyFile.txt* file, that is possible with the -k argument.

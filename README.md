# simple-kv-database
The purpose of this project is to create a simple version of a distributed, fault-tolerant, Key-Value (KV) database (or store).

![Tree](/aes/tree.jpeg){height=50%, width=50%}

## 📗 Introduction

A Key-Value Database or Key-Value store is defined as a data storage paradigm designed for storing, retrieving, and managing associative arrays. In general, KV systems treat the data as a single opaque collection, which may have different fields for every record. These implementations often use less memory, and are used extensively in cloud computing. The most common data structure used in this frame include hash tables or dictionaries. The data stored inside the data structures, i.e. inside the dictionary, can be stored and retrieved using a key that uniquely identifies the record.

In the frame of this project, the Trie data structure will be used. A Trie is also known as a digital or prefix tree, which means that Tries are a type of search trees. Tree data structures are used for locating specific keys from within a set, and in such structures there exist links between nodes that are defined not by the entire key but by individual characters. To access a particular key, that is to recover its value, change it, or remove it, the trie is traversed depth-first by following the links between nodes.

### 🔑 Prerequisites

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

## 🌃 Overview of Implementation

## ⌨️ Data Creation

The KV Store to be created can index data of arbitrary length and arbitrary nesting of the form: `key:value`. In this case, key represents the key of the data that we care to store and value is the payload (or value) of the data that we want to store for that key. The value can also contain a set of `key:value` pairs. The maximum number of instances of the `key:value` -type of values inside a high-level (top) key is referred to as the nesting level; that is the maximum times a value can take the form of a `key:value` pair, e.g. in the form of nested dictionaries.

### 🥅 Criteria for Data Generation

The following criteria and approaches are taken into account during the data creation step:
* The randomization in generating the data was the priority of this step. Combina- tions of key names were chosen at random, and the same applies for the number of values in each level, the nesting level of a specific value, the length of a string, and the integer and float values assigned to a certain key.
* Same-level keys should not contain have the same name.
  1. Each key, high-level or sub-key, can only be of type string.
  2. High-level keys are of the form ”key1”, ”key2”, etc., to enable easier debugging.
  3. High-level keys can either have an empty value, or a value with key:value pairs, up to the maximum level of nesting allowed.
* Individual values can be integers, floats, or strings, or an empty set of key:value pairs.
  1. String values can have up to a specific number of characters (user-defined parameter), but not be an empty string. String values include upper- and lower-case letters, as well as numbers.
  2. Integer and float values were ”tweaked” to make more sense, e.g. age or postal code, although in general the randomization of data was the foremost priority, and the majority of values will not make sense.

### 🗒️ The keyFile.txt auxiliary file

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
* The number of values to be included per high-level key are selected at random, ranging from 0 (empty set) to m. This holds for all the sub-keys as well.
* The sub-key names and types are drawn from the *keyFile.txt*, chosen at random all the while not allowing for duplicated keys in the same level.
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

## 🌴 Trie Implementation

For the implementation of the KV database, only one Trie structure was used for indexing, querying, and storing the data, for both high-level keys and their sub-keys, and the implementation of the Trie structures was done from scratch. Two different classes were introduced, the **Trie object**, and the auxiliary NewNode object, the latter being responsible for building and extending the Trie structure; therefore, the Trie object relies on the NewNode object. For traversing the Trie structure as well as for querying and modifying purposes, the following functions were defined for the Trie class:

1. `populate`: Function used for the creation of new keys -if they don’t already exist- inside the Trie structure, as well as for assigning them their value (payload).
2. `query`: Function used for traversing the Trie and returning the value assigned to a specific key, if the string provided is a key and/or a value has been assigned to it.
3. `delete node`: Function used for *pseudo-deleting* a specific key. Even if retrieving a certain entry goes beyond the scope of this project, it was considered a more viable and useful solution to pseudo-delete a particular key rather than trim it; that is, the delete node function ”decolorizes” the final nodes that are the ones ”marking” the presence or absence of a key, and also substitutes their value with an empty dictionary.
4. `delete`: A function that utilizes delete node but also deletes (”decolorizes”) all the children nodes of the final node of the specified key, when the relative argument is specified.

In order to incorporate the whole data into a single Trie structure, the sub-keys will be included as individual key instances, stored along with their own value. That is, the Trie does not only include the high level keys, but also the sub-keys as extensions of the high-level keys.

To achieve this, an auxiliary function was implemented, *ConcatenateKeys*, which adds a prefix to all sub-keys. This prefix consists of the high-level key as well as all keys at a level higher than the key at hand, separated by a dot. The use of this singular Trie structure in the way described above pushed for the implementation of the `delete` function that also deletes the "children" nodes, i.e. the sub-keys. It is only logical that when a high-level key is deleted -or pseudo-deleted in this case- all sub-keys are deleted as well.

All of the objects and functions described above are implemented inside the `ObjectTrie.py` script, which the user does not have to run since the script is automatically imported when needed.

## 📂 Key-Value (KV) Database

With the above implementations, one can now move to implementing the Key-Value store, that is to establish a connection between a server and a broker. The former accepts data, stores it and subsequently accepts queries and returns the findings, whereas the latter is responsible for sending the data and accepting queries from the user as well as returning the query results to the user.

### 💼 KV Broker

#### 👟 Running

A python script was created for the KV Broker. The following arguments need to be supplied in order for the script to run and output the desired results:
1. **−s** : Defining the serverFile, the file containing the space separated list of server IPs and their respective ports that will be listening for queries and indexing commands. This argument defaults to the serverFile.txt already provided in the frame of this project.
2. **−i** : Defining the *dataToIndex.txt*, the output of the Data Creation step. This argument defaults to the *dataToIndex.txt* already generated by the `createData.py` script and provided in the frame of this project.
3. **−k** : Replication factor, i.e. how many different servers will have the same replicated data.

The Python script starts with establishing a connection with the servers; **that is why the script that initiates the servers has to run before running the KV Broker script** (see section below on KV Server). It performs a check oh how many servers are up and running, and if the number of servers active are less than the replication factor specified, the operation is aborted: there are not enough active servers to which the data is sent. However, if enough servers are running, at least k, then the KV Broker sends a request to the servers of the form "PUT data".

The number of servers to which each line of data -from the input _dataToIndex.txt_ file- is also specified by k. The Broker then selects those k servers at random. If the servers selected are active, then the data will be sent to and stored by the servers; if, on the other hand, among the randomly selected servers one or more are down, the Broker will try to establish the connection yet it will most probably fail (unless the server(s) came back up in the meantime), thus the data will not be sent to and stored by the inactive server(s). This approach takes into account that the servers might come back up while the indexing takes place.

In parallel, while the indexing takes place, the Broker keeps checking how many servers are running. If more than k servers are inactive, i.e. if one or more servers shut down during the indexing so that no k servers are active, then the operation is aborted and the indexing step stops. On the contrary, if there are enough servers running during the indexing step, then the Indexing will be successfully completed.

Upon successful completion of the indexing step, the Broker awaits for instructions from the user. Those can have the following forms:

1. `GET`: A query request for high-level keys, e.g. GET key1.
2. `QUERY`: A query request for high-level keys or sub-keys, e.g. QUERY key2.name.age. 
3. `DELETE`: A delete request for high-level keys, e.g. DELETE key3
4. `EXIT`: An exit prompt; the program is terminated.

If the user provides any other invalid request, e.g. lower-case GET or a command with typos, the program returns a list of all the valid requests and the user is prompted to provide a valid request. If the user presses Enter before writing anything, the program prompts the user to insert their request anew.

For the whole duration of the user request input, the Broker keeps checking how many and which servers are running. If all servers are down, an error is printed. Furthermore, in the case of the GET request, if more than k servers are down, the Broker prints a warning that ”Correct output is not guaranteed”. Last but not least, in the case of the DELETE request, if even at least one server is down, the operation is aborted and the corresponding warning is printed.

Moreover, the following things are of importance and should be noted:
* If the user submits a PUT request, the following message is printed: ”PUT opera- tion is not supported for now.” Indeed, the PUT operation has not been implemented in the frame of this version, primarily due to possible complexity in checking that the data provided by the user is of correct format. Other than that, the implementation of a user PUT command if not difficult.
* In the case of a GET request, the first valid result is returned, i.e. a result that returns the value of the key from any of the servers that have stored the entry.

# simple-kv-database
The purpose of this project is to create a simple version of a distributed, fault-tolerant, Key-Value (KV) database (or store).

![Tree](/aes/tree.jpeg)

## 📗 Introduction

A Key-Value Database or Key-Value store is defined as a data storage paradigm designed for storing, retrieving, and managing associative arrays. In general, KV systems treat the data as a single opaque collection, which may have different fields for every record. These implementations often use less memory, and are used extensively in cloud computing. The most common data structure used in this frame include hash tables or dictionaries. The data stored inside the data structures, i.e. inside the dictionary, can be stored and retrieved using a key that uniquely identifies the record.

In the frame of this project, the Trie data structure will be used. A Trie is also known as a digital or prefix tree, which means that Tries are a type of search trees. Tree data structures are used for locating specific keys from within a set, and in such structures there exist links between nodes that are defined not by the entire key but by individual characters. To access a particular key, that is to recover its value, change it, or remove it, the trie is traversed depth-first by following the links between nodes.

## 🔑 Prerequisites

Please make sure that you have **Python 3.8.3** (or greater) installed on your computer. It possible that the implementation will run with other versions of Python.

Also, make sure that the following libraries are installed and up-to-date:
* argparse
* socket
* sys
* os
* random
* itertools
* json
* csv
* string

## 👟 Running

The KV Store to be created can index data of arbitrary length and arbitrary nesting of the form: `key:value`. In this case, key represents the key of the data that we care to store and value is the payload (or value) of the data that we want to store for that key. The value can also contain a set of `key:value` pairs. The maximum number of instances of the `key:value`-type of values inside a high-level (top) key is referred to as the nesting level; that is the maximum times a value can take the form of a `key:value` pair, e.g. in the form of nested dictionaries.

### ⌨️ Random Data Generation

For this implementation we generate random data.

#### Arguments

- **−k** : Defining the _keyFile_, the file containing the space-separated list of key names and their data types that could potentially be used for key generation (See section above). This argument defaults to the keyFile.txt already provided in the frame of this project.
- **−n** : Number of lines, i.e. number of separate instances of data, to be generated
- **−d** : Maximum level of nesting, i.e. how many times a value take the key:value form. Zero means no nesting, i.e. there is only one set of key-values for the high-level key.
- **−m** : Maximum number of keys inside each value. This may include a zero value, which leads to an empty set of key:value pairs.
- **−l** : Maximum length of a string value whenever a string value is generated. Strings are comprised of letters (upper and lowercase) or numbers, not symbols. Generation of an empty string is not permitted.

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

### 📂 Key-Value (KV) Database

After creating the random data to populate our KV Database, we can move on to implementing the Key-Value store, that is to establish a connection between a server and a broker. The former accepts data, stores it and subsequently accepts queries and returns the findings, whereas the latter is responsible for sending the data and accepting queries from the user as well as returning the query results to the user.

### 💻 KV Server

First, we need to start the servers. We will can run the following commands on localhost, from different terminals in order to set up multiple servers.

#### Arguments

* −a : The IP address to which the server should be started at.
* −p : The port to which the server should be started at.

#### How to Run

```
python3 kvServer.py -a {ip_address}
	            -p {port}

```

#### Example

```
python3 kvServer.py -a 127.0.0.1 -p 8000
python3 kvServer.py -a 127.0.0.1 -p 8001
python3 kvServer.py -a 127.0.0.1 -p 8002
python3 kvServer.py -a 127.0.0.1 -p 8003
python3 kvServer.py -a 127.0.0.1 -p 8004

```

#### Help

```
python3 kvServer.py --help

```

### 💼 KV Broker

Then we can move ahead with populating the database and performing queries.

#### Arguments

* **−s** : Defining the serverFile, the file containing the space separated list of server IPs and their respective ports that will be listening for queries and indexing commands. This argument defaults to the serverFile.txt already provided in the frame of this project.
* **−i** : Defining the *dataToIndex.txt*, the output of the Data Creation step. This argument defaults to the *dataToIndex.txt* already generated by the `createData.py` script and provided in the frame of this project.
* **−k** : Replication factor, i.e. how many different servers will have the same replicated data.

#### How to Run

```
python3 kvBroker.py -s {serverFile.txt}
	            -i {dataToIndex.txt}
		    -k {replication factor}
```

#### Example

```
python3 kvBroker.py -k 3
```

#### Example Query Commands

```
GET key1
GET "key1"
GET 'key1'
GET key2.name.age
QUERY key2.name.age
DELETE key3
GET key3
EXIT
```

#### Help

```
python3 kvBroker.py --help
```

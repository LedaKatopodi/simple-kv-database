# simple-kv-database
The purpose of this project is to create a simple version of a distributed, fault-tolerant, Key-Value (KV) database (or store).

## Introduction

A Key-Value Database or Key-Value store is defined as a data storage paradigm designed for storing, retrieving, and managing associative arrays. In general, KV systems treat the data as a single opaque collection, which may have different fields for every record. These implementations often use less memory, and are used extensively in cloud computing. The most common data structure used in this frame include hash tables or dictionaries. The data stored inside the data structures, i.e. inside the dictionary, can be stored and retrieved using a key that uniquely identifies the record.

In the frame of this project, the Trie data structure will be used. A Trie is also known as a digital or prefix tree, which means that Tries are a type of search trees. Tree data structures are used for locating specific keys from within a set, and in such structures there exist links between nodes that are defined not by the entire key but by individual characters. To access a particular key, that is to recover its value, change it, or remove it, the trie is traversed depth-first by following the links between nodes.

## Prerequisites

Please make sure that you have **Python 3.8.3** (or greater) installed on your computer.
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

## Data Creation

The KV Store created can index data of arbitrary length and arbitrary nesting of the form: key : value . In this case, key represents the key of the data that we care to store and value is the payload (or value) of the data that we want to store for that key. The value can also contain a set of key : value pairs. The maximum number of instances of the key : value -type of values inside a high-level (top) key is referred to as the nesting level; that is the maximum times a value can take the form of a key:value pair, e.g. in the form of nested dictionaries.

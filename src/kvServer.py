import argparse
import socket
import json
import ObjectTrie

#### ==== Arguments ==== ####

parser = argparse.ArgumentParser(description = 'Key-Value Server starts at a specific IP address and port. \
	It stores data and accepts query requests from the Key-Value Broker, returning the relevant results.')
parser.add_argument('-a', type = str, help = 'IP address.')
parser.add_argument('-p', type = int, help = 'Port.')

args = parser.parse_args()


# Initializing Trie Structure
server_trie = ObjectTrie.Trie()

#### ==== Start Server + Await for Connections ==== ####

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((args.a, args.p))
serversocket.listen(5) # maximum 5 connections

while True:

    connection, address = serversocket.accept()
    msg = connection.recv(8192)

    if len(msg) > 0:

        message = msg.decode()

        if message.split(None, 1)[0] == "PUT":

            dat = message.split(None, 1)[1]

            # Transforming to dictionary 
            dat_dict = str("{") + str(dat) + str("}")
            dat_dict = dat_dict.replace("'", "\"")
            dat_dict = json.loads(dat_dict)

            # Getting High-level key
            hl_key = list(dat_dict.keys())[0]

            # Handling Subkeys
            entry = ObjectTrie.ConcatenateKeys(dictionary = dat_dict)

            # Checking if high-level key exists
            #if server_trie.key_exists(hl_key):

                #message = "Key exists. Overwriting not permitted."
                #connection.send(message.encode())
                #continue

            #else:
                # Else, add entry
            for key, value in entry.items():
                server_trie.populate(key, value)
            message = "Connection with " + str(args.a) + ", port: " + str(args.p) + ". STATUS: OK. Entry Added."
            connection.send(message.encode())

        elif message.split(None, 1)[0] == "GET":
            
            key_search = message.split(None, 1)[1]
            # Low-level keys handling
            key_search = key_search.replace(".", "_")
            # Quote handling
            key_search = key_search.replace("\"", "")
            key_search = key_search.replace("\'", "")

            message = str(server_trie.query(key_search))
            connection.send(message.encode())

        elif message.split(None, 1)[0] == "QUERY":
            
            key_search = message.split(None, 1)[1]
            # Quote handling
            key_search = key_search.replace("\"", "")
            key_search = key_search.replace("\'", "")

            message = str(server_trie.query(key_search))
            connection.send(message.encode())

        elif message.split(None, 1)[0] == "DELETE":

            key_delete = message.split(None, 1)[1]
            # Low-level keys handling
            key_delete = key_delete.replace(".", "_")
            # Quote handling
            key_delete = key_delete.replace("\"", "")
            key_delete = key_delete.replace("\'", "")

            server_trie.delete(key_delete, del_children = True)
            message = "Key deleted."
            connection.send(message.encode())

    connection.close()




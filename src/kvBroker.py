import argparse
import socket
import sys
import os
import random
import itertools

#### ==== Arguments ==== ####

parser = argparse.ArgumentParser(description = 'Key-Value Broker establishes a connection with the servers.\
	It redirects requests in two forms: 1. PUT: Requesting from the server to store selected data, 2. QUERY: \
	Accepting user queries, redirecting the requests to the Key-Value Server, and collecting and presenting the results\
	to the user.')
parser.add_argument('-s', default = 'serverFile.txt',
	help = 'Space separated list of server IPs and their respective ports that will be \
	listening for queries and indexing commands. Defaults to "serverFile.txt".')
parser.add_argument('-i', default = 'dataToIndex.txt',
	help = 'Input file containing data. Defaults to the randomly generated data saved in the file "​dataToIndex.txt".')
parser.add_argument('-k', type = int,
	help = 'Replication factor, i.e. how many different servers will have the same replicated data.')

parser._parse_known_args(sys.argv[1:], argparse.Namespace())
args = parser.parse_args()

#### ==== Reading Input ==== ####

# Reading dataToIndex.txt
lines = []    
with open(args.i, 'r') as f:
        for line in f:
            lines.append(line.strip())
numData = len(lines)
lines = lines[0:numData] # final line in file is empty

# Reading serverFile.txt
servers = []
with open(args.s) as f:
    servers = [[str(x) for x in line.split()] for line in f]
numServers = len(servers)


#### ==== Establish Connection with Servers ==== ####

print("\nEstablishing Connection with Servers\n")
servers_running = numServers
ports_running = []

for i in range(numServers):

	clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	ip_tmp = str(servers[i][0])
	port_tmp = int(servers[i][1])

	try:
		clientsocket.connect((ip_tmp, port_tmp))
		ports_running.append(port_tmp)
		print("Connection established with " + str(ip_tmp) + ", port: " + str(port_tmp) + ". STATUS: Server Running")

	except:
		servers_running = servers_running - 1
		print("Connection not established with " + str(ip_tmp) + ", port: " + str(port_tmp) + ". STATUS: Server Down")

	clientsocket.close()

if servers_running < args.k:
	sys.exit("\n" + str(numServers - servers_running) + " server(s) are down. Operation aborted. \n")
else:
	print("\n" + str(servers_running) + " server(s) running. Resuming operation. \n")

print("\n## ==================== ##\n")


#### ==== Sending the Data ==== ####

for dat in lines:

	servers_running_init = servers_running

	# Randomly selecting the Servers to connect to
	combTmp = list(itertools.combinations(range(numServers), args.k))
	servTmpInd = random.randint(1, len(combTmp))
	servTmp = combTmp[servTmpInd-1]

	for i in range(args.k):

		clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		ip_tmp = str(servers[servTmp[i]][0])
		port_tmp = int(servers[servTmp[i]][1])

		try:
			clientsocket.connect((ip_tmp, port_tmp))
			#print("Connection with " + str(ip_tmp) + ", port: " + str(port_tmp) + ". STATUS: OK")
			
			if port_tmp not in ports_running:
				ports_running.append(port_tmp)
				servers_running += 1

			message = str("PUT ") + str(dat)
			clientsocket.send(message.encode())
			msg = clientsocket.recv(2048)
			print(msg.decode())
			
		except:
			print("Connection with " + str(ip_tmp) + ", port: " + str(port_tmp) + ". STATUS: FAILED")
			if port_tmp in ports_running:
				ports_running.remove(port_tmp)
				servers_running = servers_running - 1

		clientsocket.close()

	if servers_running < args.k:
		sys.exit("\n" + str(numServers - servers_running) + " server(s) are down. Operation aborted. \n")
	elif servers_running != servers_running_init:
		print(str(args.k) + " or more server(s) still running. Resuming operation. \n")

	print("## ==================== ##")


print("\nIndexing Completed\n")
print("## ==================== ##\n")


#### ==== Handling User Queries ==== ####

while True:

	user_input = input("Please enter your request:\n")

	# checking User Input
	if user_input == "":
		continue

	elif user_input.split(None, 1)[0] == "PUT":
		print("\nPUT operation is not supported for now.\n")

	elif user_input.split(None, 1)[0] == "EXIT":
		sys.exit("\nAborting Mission...\n\n")

	elif user_input.split(None, 1)[0] not in ["EXIT", "PUT", "GET", "QUERY", "DELETE"]:
		print("\nInvalid option. The possible options are:\n")
		print("-GET: to obtain the values of high-level keys. Example usage: 'GET key1'.")
		print("-QUERY: to obtain the values of all possible keys, including high-level and subkeys. Example usage: 'GET key1.name'.")
		print("-DELETE: to delete a high-level key. This subsequently deletes all subkeys. Example usage: 'DELETE key1'.")
		print("-EXIT: exit program.\n")


	# Checking Server Connectivity before attempting Queries
	for i in range(numServers):
		
		clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ip_tmp = str(servers[i][0])
		port_tmp = int(servers[i][1])

		try:
			clientsocket.connect((ip_tmp, port_tmp))
			if port_tmp not in ports_running:
				ports_running.append(port_tmp)
				servers_running += 1
			

		except:
			if port_tmp in ports_running:
				ports_running.remove(port_tmp)
				servers_running = servers_running - 1
			
		clientsocket.close()

	if servers_running == 0:
		print("WARNING: No servers currently running, queries will be affected. Please wait or try later.\n")

	# Query Handling
	for i in range(numServers):
		
		clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		ip_tmp = str(servers[i][0])
		port_tmp = int(servers[i][1])

		try:
			clientsocket.connect((ip_tmp, port_tmp))

			if port_tmp not in ports_running:
				ports_running.append(port_tmp)
				servers_running += 1

				#print("Connection with " + str(ip_tmp) + ", port: " + str(port_tmp) + ". STATUS: OK")

			if user_input.split(None, 1)[0] == "GET" or user_input.split(None, 1)[0] == "QUERY" :

				if servers_running < args.k:
					print("\n" + str(numServers - servers_running) + " server(s) are down. Correct output is not guaranteed.\n")

				message = user_input
				clientsocket.send(message.encode())
				msg = clientsocket.recv(8192)
				message = msg.decode()

				print("Server: " + str(ip_tmp) + ", port: " + str(port_tmp) + ": " + str(message))
	
			elif user_input.split(None, 1)[0] == "DELETE":

				if servers_running < numServers:
					print("Only " + str(servers_running) + " servers running. DELETE operation cannot be carried out.")
				else:
					message = user_input
					clientsocket.send(message.encode())
					msg = clientsocket.recv(2048)
					print(msg.decode())	
		
		except Exception as e: 
			#print("Connection with " + str(ip_tmp) + ", port: " + str(port_tmp) + ". STATUS: FAILED")
			if e == "[Errno 61] Connection refused":
				if port_tmp in ports_running:
					ports_running.remove(port_tmp)
					servers_running = servers_running - 1

		clientsocket.close()

	print("\n## ==================== ##\n")	
		


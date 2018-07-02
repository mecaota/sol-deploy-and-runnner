# coding: utf-8

import binascii
import sys
import json
import subprocess
from collections import OrderedDict
from functools import partial
from solc import compile_source
from web3 import Web3,IPCProvider, HTTPProvider

def argv_parser():
	results = {}
	args = sys.argv[1:]
	for arg in args:
		name_arg = arg.split("=", 1)
		try:
			results[name_arg[0]] = name_arg[1]
		except ValueError:
			print("Missed Input. Try again...")
	return results

args = argv_parser()

### eth chain connection

if "http" in args:
	web3 = web3(HTTPProvider(args["http"]))
elif "ipc" in args:
	web3 = Web3(IPCProvider(args["ipc"]))
else:
	web3 = Web3(IPCProvider('../geth.ipc'))


### compiled data load OR compile

if ("bin" in args) and ("abi" in args):
	bin = args["bin"]
	#abi = json.loads(args["abi"], object_pairs_hook=OrderedDict )
	abi = args["abi"]
else:
	bin = ""
	abi = {}
	#solc_codes = ["solc", "--abi", "--bin", args[0]]
	#with open(args[0]) as source:
	#	compiled_sol = compile_source(source)
	#	print(compiled_sol)
	res = subprocess.run(solc_codes, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
	print("output result")
	for output in res.stdout.splitlines():
		print(output)
	#print(res.splitlines)

print("---------- input data ----------")
print("----- bin -----")
print(bin)
print("----- abi -----")
print (abi)

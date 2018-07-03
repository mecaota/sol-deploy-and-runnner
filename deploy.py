# coding: utf-8

import sys
import json
from getpass import getpass

# web3.py & solc
from solc import compile_source
from web3 import Web3,IPCProvider, HTTPProvider
from web3.contract import ConciseContract

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

if "coinbase" in args:
	web3.eth.defaultAccount = args["coinbase"]
else:
	web3.eth.defaultAccount = web3.eth.accounts[0]


### compiled data load, or compile

if ("bin" in args) and ("abi" in args):
	bin = args["bin"]
	abi = args["abi"]
else:
	bin = ""
	abi = {}

print("---------- input data ----------")
print("----- bin -----")
print(bin)
print("----- abi -----")
print (abi)
print("--------------------------------")

## coinbase account password input form
coinbase_pwd = getpass(prompt = "Please input coinbase account password: ")
while not web3.personal.unlockAccount(web3.eth.coinbase, coinbase_pwd):
	coinbase_pwd = getpass(prompt = "Missed password. Please retype coinbase account password: ")

## contract deploy
print("Now deploying, please wait...")
contract_obj = web3.eth.contract(abi=abi, bytecode=bin)
tx_address = web3.eth.waitForTransactionReceipt(contract_obj.constructor().transact()).contractAddress
web3.personal.lockAccount(web3.eth.coinbase)
print("Contract address published!: " + str(tx_address))

## abi & tx_address save to file
with open("contracts.tsv", "a") as file:
	file.write(str(tx_address) + "\t" + str(abi) + "\t" + str(bin) + "\n")
	print("Contract Address & ABI & BIN was written in contracts.tsv")

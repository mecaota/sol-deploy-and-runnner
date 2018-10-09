# coding: utf-8

import sys
import ast
import code
import pandas
from jsonpath_rw import parse
from getpass import getpass

# web3.py
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

def open_contract(source, contract_name):
	tsv = pandas.read_csv(source, sep="\t", header=None)
	tsv.columns = ["name", "tx_address", "abi", "bin"]
	tsv =  tsv[tsv["name"] == contract_name]
	tsv = tsv.to_dict(orient="list")
	print("----------loaded contract data----------")
	print("-----abi-----")
	print(tsv["abi"][0])
	print("-----tx_address-----")
	print(tsv["tx_address"][0])
	return web3.eth.contract(abi=ast.literal_eval(tsv["abi"][0]), address=tsv["tx_address"][0])

def open_prompt():
	#func = contract.functions
	print()
	start_disp = "----------Contract functions----------\n"
	for value in contract.all_functions():
		start_disp += str(value) + "\n"
	start_disp += "\n----------Already main defined variable and functions----------\n"
	start_disp += "func = contract.functions\n"
	start_disp += "contract = Contract Object\n"
	start_disp += "web3 = web3 Object\n"
	start_disp += "unlock_account(account)\n"
	start_disp += "\n----------------------------------------\n"
	#code.InteractiveConsole(locals()).interact(banner=start_disp)
	code.InteractiveConsole(globals()).interact(banner=start_disp)

def unlock_account(account):
	## coinbase account password input form
	coinbase_pwd = getpass(prompt = "Please input coinbase account password: ")
	while not web3.personal.unlockAccount(account, coinbase_pwd):
		coinbase_pwd = getpass(prompt = "Missed password. Please retype coinbase account password: ")
	return web3

args = argv_parser()

### eth chain connection

if "http" in args:
	web3 = web3(HTTPProvider(args["http"]))
elif "ipc" in args:
	web3 = Web3(IPCProvider(args["ipc"]))
else:
	web3 = Web3(IPCProvider('../geth.ipc'))

## select coinbase account
if "coinbase" in args:
	web3.eth.defaultAccount = args["coinbase"]
else:
	web3.eth.defaultAccount = web3.eth.accounts[0]


### contract load
contract = open_contract(args["source"], args["contract_name"])
print("-----contract loaded-----")

## functions for prompt
func = contract.functions
coinbase = web3.eth.coinbase

## coinbase account password input form
web3 = unlock_account(coinbase)

## contract runner
open_prompt()

## exit process
web3.personal.lockAccount(web3.eth.coinbase)
print("Process closing...")

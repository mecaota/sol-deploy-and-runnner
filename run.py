# coding: utf-8

import sys
import json
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

def yes_no_input(message):
        while True:
                choice = input(message + " 'yes' or 'no' [Y/n]: ").lower()
                if choice in ['y', 'ye', 'yes', '']:
                        return True
                elif choice in ['n', 'no']:
                        return False

def open_contract(source, contract_name):
        tsv = pandas.read_csv(source, sep="\t", header=None)
        tsv.columns = ["name", "tx_address", "abi", "bin"]
        tsv =  tsv[tsv["name"] == contract_name]
        return tsv.to_dict(orient="list")

def contract_run(contract):
        method = ""
        result = []
        while method != "exit":
                print(json.loads(contract.abi))
                method = input("Please type contract functions method: ")
                runner = contract.functions[method]
                result.push(runner(1).call())
        return result

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


### contract load
data = open_contract(args["source"], args["contract"])
contract = web3.eth.contract(abi=data["abi"], address=data["txaddress"])

## coinbase account password input form
coinbase_pwd = getpass(prompt = "Please input coinbase account password: ")
while not web3.personal.unlockAccount(web3.eth.coinbase, coinbase_pwd):
        coinbase_pwd = getpass(prompt = "Missed password. Please retype coinbase account password: ")

## contract runner
print(contract_run(contract))

## exit process
web3.personal.lockAccount(web3.eth.coinbase)
print("Process closing...")
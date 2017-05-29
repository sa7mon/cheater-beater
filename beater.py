#!/usr/local/Cellar/python/2.7.12/bin/python2.7

import json
import hashlib
import psutil
import argparse


workingDirectory = "./good-game/"

def enforceFileRule(fileName, fileHash):
	fileName = workingDirectory + fileName
	print("	File name: " + str(fileName) + " File hash: " 
			+ str(fileHash))

	# Open file and calculate MD5 hash
	with open(fileName) as file_to_check:
	    md5_returned = hashlib.md5(file_to_check.read()).hexdigest()

	if md5_returned == fileHash:
		print("	Good file!")
	else:
		print("	Bad file!")


def enforceProcessNameRule(procName):
	# print("	Enforced process rule for process: " + procName)
	foundBadProc = False

	for proc in psutil.process_iter():
	    try:
	        pinfo = proc.as_dict(attrs=['pid', 'name'])
	    except psutil.NoSuchProcess:
	        pass
	    else:
	        # print(pinfo)
	        if pinfo.get("name") == "procName":
			foundBadProc = True

	print("Bad proccess running!")


def enforceMemoryStringRule(memString):
	print("	Enforced memory rule for string: " + memString)


# Instantiate the parser
parser = argparse.ArgumentParser(description='Fight those cheaters!')

# Add directory arg
parser.add_argument('gameDirectory', help='Directory where game is stored')

# Parse the args
args = parser.parse_args()

workingDirectory = args.gameDirectory


with open('config.json') as f:
    # for line in f:
    data = json.load(f)

for rule in data.get("rules"):
	ruleType = rule.get("rule-type")

	if ruleType == "file-hash":
		print("Processing file hash rule...")
		enforceFileRule(rule.get("file-name"), rule.get("hash"))

	elif ruleType == "running-process":
		print("Processing running process rule...")
		enforceProcessNameRule(rule.get("process-name"))

	elif ruleType == "memory-string":
		print("Processing memory string rule...")
		enforceMemoryStringRule(rule.get("string"))
	else:
		"Error: Unknown rule type"
#!/usr/local/Cellar/python/2.7.12/bin/python2.7


########################################################
# cheater-beater - beater.py
# 	An optimistic cheat detection script
#
# Author: Dan Salmon (@sa7mon)
# Written: May 29, 2017
# Location: HAN University, Arnhem, Netherlands
#
########################################################


import json
import hashlib
import psutil
import argparse
import os.path


def enforceFileRule(fileName, fileHash):
	fileName = workingDirectory + fileName

	# Open file and calculate MD5 hash
	with open(fileName) as file_to_check:
	    md5_returned = hashlib.md5(file_to_check.read()).hexdigest()

	if md5_returned == fileHash:
		return True
	else:
		return False


def enforceProcessNameRule(procName):
	allProcsGood = True

	for proc in psutil.process_iter():
	    try:
	        pinfo = proc.as_dict(attrs=['pid', 'name'])
	    except psutil.NoSuchProcess:
	        pass
	    else:
	        if pinfo.get("name") == procName:
	       		allProcsGood = False
	return allProcsGood

def enforceBadFileRule(fileName):
	return not os.path.isfile(workingDirectory + fileName) 

# Instantiate the parser
parser = argparse.ArgumentParser(description='Fight those cheaters!')

# Add directory arg
parser.add_argument('gameDirectory', help='Directory where game is stored')

# Parse the args
args = parser.parse_args()

workingDirectory = args.gameDirectory

with open('config.json') as f:
	
	# Load in JSON file
    data = json.load(f)

ruleCount = len(data.get("rules"))
allRulesPass = True

# Verify each rule
for rule in data.get("rules"):
	ruleType = rule.get("rule-type")

	if ruleType == "file-hash":
		print("Processing file hash rule...")
		if enforceFileRule(rule.get("file-name"), rule.get("hash")) == False:
			allRulesPass = False

	elif ruleType == "running-process":
		print("Processing running process rule...")
		if enforceProcessNameRule(rule.get("process-name")) == False:
			allRulesPass = False
	elif ruleType == "bad-file":
		print("Processing bad file rule")
		if enforceBadFileRule(rule.get("file-name")) == False:
			allRulesPass = False
	else:
		"Error: Unknown rule type"

# Make a ruling
if allRulesPass == True:
	print("\n \033[1;32mReport: All good! \033[1;m\n")
else: 
	print("\n \033[1;31mReport: CHEATER\033[1;m\n")

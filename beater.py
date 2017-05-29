#!/usr/local/Cellar/python/2.7.12/bin/python2.7

import json


def enforceFileRule(fileName, fileHash):
	print("	File name: " + str(fileName) + " File hash: " 
			+ str(fileHash))


def enforceProcessNameRule(procName):
	print("	Enforced process rule for process: " + procName)


def enforceMemoryStringRule(memString):
	print("	Enforced memory rule for string: " + memString)


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
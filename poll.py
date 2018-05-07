# Log Polling
import requests
import importlib
import time
import petlog

entryLogURI = "https://pets.ewi.utwente.nl/log/16-aPvLeykys0oiQd8uJ6F+G5Oakhp/PoupGtcQERJlqow=/entry.csv"
exitLogURI =  "https://pets.ewi.utwente.nl/log/16-aPvLeykys0oiQd8uJ6F+G5Oakhp/PoupGtcQERJlqow=/exit.csv"
debugLogURI = "https://pets.ewi.utwente.nl/log/error.txt"

l1 = 0
l2 = 0
l3 = 0

def extractRemainder(uri, start) :
	"Return the text (per line) from a uri, starting at an index and its full length"
	full = petlog.getLog(uri).strip()
	l = len(full)
	return l, full[start:].split("\n")

def getDateCol(line):
	return line[1][:32]

while(True):

	l1, entries = extractRemainder(entryLogURI, l1)
	l2, exits = extractRemainder(exitLogURI, l2)
	# l3, debug = extractRemainder(debugLogURI, l3)

	comb = [("- entr", e) for e in entries if len(e) > 0] + [("| exit", e) for e in exits if len(e) > 0]
	sorted(comb, key=getDateCol)

	for line in comb:
		print(line[0], line[1])

	time.sleep(1)

	

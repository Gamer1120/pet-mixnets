# Extract Log Files
import requests

def getLog (uri) :
	"Return the contents of a url in UTF-8 encoding"
	r = requests.get(uri)
	return r.content.decode("utf-8")	

def csvLogToArray(csvLog) :
	"Returns 2-dimensional array from log"
	return [row.split(",") for row in csvLog.strip().split("\n")]

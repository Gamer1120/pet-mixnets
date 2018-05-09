# Extract Log Files
import petlog

entryLogURI = "https://pets.ewi.utwente.nl/log/16-aPvLeykys0oiQd8uJ6F+G5Oakhp/PoupGtcQERJlqow=/entry.csv"
entries = petlog.csvLogToArray(petlog.getLog(entryLogURI))

exitLogURI =  "https://pets.ewi.utwente.nl/log/16-aPvLeykys0oiQd8uJ6F+G5Oakhp/PoupGtcQERJlqow=/exit.csv"
exits = petlog.csvLogToArray(petlog.getLog(exitLogURI))


# Count the number of entries before the first exit
i = 0 

while i < len(entries) and entries[i] <= exits[0]:
	print(entries[i])
	i = i + 1

print("Number entries before first exit:", i)
import dummy

# Options for t1, t2, t3
t1s = range(1,15)
t2s = range(1,15)
t3s = range(1,15)

# Total padding messages
padding = 5

# Actual Observed Output Sequence
actual = [0,0,0,0,0,0,0,0,12,0,0,0,0,0,0,0,0,0,0,0,12,0,0,0,0,0,0,0,0,0,0,0,0,0,15];
steps = len(actual)
 
def evaluateMixAsSolution(m):
	"Run a mixnet to verify it gives the same output sequence"

	out, m2 = dummy.sendNMessages(m, steps)

	for i in range(0, steps):
		if out[i] != actual[i]:
			return False

	return True
 
def evaluateStateReachable(ts, states, maxruns=1000):
	"Run a mixnet for a long time to see if a buffer-state is possible"

	# Create the mixnet
	m = (len(ts), ts, [0]*len(ts))
	c = 0
	for i in range(0, maxruns):
		out, m = dummy.sendMessage(m)	
		c += 1
		if m[2] == states:
			return True, c
	return False

def brute():

	# Try all threshold combinations
	for t1 in t1s:
		for t2 in t2s:
			for t3 in t3s:

				# Try all valid padding combinations
				for r1 in range(0, padding + 1):
					for r2 in range(0, padding + 1 - r1):
						for r3 in range(0, padding + 1 - r1 - r2):

							validR = r1 < t1 and r2 < t2 and r3 < t3
							enoughPadd = r1+r2+r3 == 5

							if validR and enoughPadd:
								# Create the mixnet
								m = (3, [t1,t2,t3], [r1,r2,r3])

								# Compare against solution
								if evaluateMixAsSolution(m):
									# Check if the original state can be reached
									if evaluateStateReachable(m[1], [r1,r2,r3]):
										print ("\nFound solution: ", m)

# m = (3,[3,11,4],[0,2,3])

# i = 0
# out = -1
# while i != out:
# 	i += 1
# 	out, m = dummy.sendMessage(m)
# print ("Returns to 0 state after ",i)
# n = 135
# outs, m = dummy.sendNMessages(m, n)
# # acc = 0
# for i in range(1,n):
# 	if(outs[i] > 0):
# 		print (i+1, outs[i])
# 	acc += outs[i-1]
	# print(outs[i-1], acc, i)
# 	if outs[i-1] > 0 and i == acc:
# 		print ("Returns to 0 state after", i)

brute() # (3,[3,11,4],[0,2,3])
# print (evaluateStateReachable([3,11,4],[0,0,0]))
# for i in range(0,1000):
# 	m = dummy.randomMixnet(3)
# 	if evaluateStateReachable(m[1], [0]*3) == False:
# 		print ("Zero-state not reachable for ", m)
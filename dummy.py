# Dummy Mixnet
# ============
# Represent a mixnet state as a 3-tuple (n, [t0, t1, ..., tn], [r0, r1, ..., rn])
# with n mixes having thresholds ti and number of initial messages ri

import random
import math
import copy

def validateMixnet(mixnet):
	assert mixnet[0] == len(mixnet[1]) and mixnet[0] == len(mixnet[2]), "Size does not match t or r length"

# Input (i, [t0, t1, ..., ti], [r0, r1, ..., ri])
# Output out, (i, [t0, t1, ..., t1], [r0_1, r1_1, ..., ri_1])
#   where out is the number of messages leaving the mix
def sendMessage(mixnet) :
	"Given a mixnet config, add a message and calculate the next state and output"
	size, t, r = copy.deepcopy(mixnet)
	out = 0

	validateMixnet(mixnet)

	# Add the message to the first mix
	r[0] += 1

	for i in range(0, size):
		if r[i] >= t[i]:
			s = r[i] % t[i] # calc remainder (staying)
			e = (r[i] - s) # calc exiting messages
			r[i] = s # store remainder
			if i == (size - 1) :
				out = e
			else :
				r[i+1] += e # add to next mix			

	return out, (size, t, r)

def sendNMessages(mixnet, n): 
	"Given a mixnet config, add n messages and calculate the next state and output"
	out = []
	for i in range(0, n):
		o, mixnet = sendMessage(mixnet)
		out.append(o)
	return out, mixnet

# Usage example:
def testSendMessage():
	"Run a simple test on sendMessage"
	m = (3, [2, 3, 2], [0,0,0])
	# Expected output [r0, r1, r2, out]
	s = [
		[1,0,0,0], # first message enters
		[0,2,0,0], # flush mix 0
		[1,2,0,0],  
		[0,1,1,2], # flush mix 0, 1 and 2
		[1,1,1,0],
		[0,0,0,4], # flush mix 0, 1 and 2
		# Cycle repeats after this
	]

	for i in range(0, len(s)):
		out, m = sendMessage(m)
		a = (m[2] + [out])
		assert (a == s[i]), "Step " + str(i) + ": Expected " + str(s[i]) + " but received " + str(a)
	print("Test Send Message successful")

def getNFlushes(m, n):
	"Return the first n pairs (e_i, o_i) where e_i is the number of messages entered until flush i, and o the number of messages exiting at flush i."
	i = 0
	flushes = []
	while len(flushes) < n:
		out, m = sendMessage(m)
		i += 1
		if out > 0:
			flushes.append((i, out))
	return flushes

def randomMixnet(size, tmin=2, tmax=12, rmin=0, rmax=0):
	"Create a random mixnet with a given size and threshold range"
	return (
		size, 
		[random.randint(tmin, tmax) for i in range(0, size)],
		[random.randint(rmin, rmax) for i in range(0, size)]
		)

def printStepsOfMixnet(m, steps=100):
	out = 0
	for i in range(0, steps):
		if out > 0:
			print(i, m, "->", out)
		else:
			print(i, m)	
		out, m = sendMessage(m)

# m = (3, [3,7,5],[0,0,0])

# printStepsOfMixnet(m)

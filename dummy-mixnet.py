#  Dummy Mixnet

# Mixnet datastructure: (size, [t0, t1, t2], [r0, r1, r2])
def sendMessage(mixnet) :
	"Given a mixnet config, add a message and calculate the next state and output"
	size, t, r = mixnet
	out = 0

	# Add the message to the first mix
	r[0] += 1

	for i in range(0, size):
		# print("mix",i)
		if r[i] >= t[i]:
			# print("exceeds",  r[i], t[i])
			s = r[i] % t[i] # calc remainder (staying)
			# print("staying", s)
			e = (r[i] - s) # calc exiting messages
			# print("exiting", e)
			r[i] = s # store remainder
			if i == (size - 1) :
				out = e
			else :
				r[i+1] += e # add to next mix			

	return out, (size, t, r)

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

testSendMessage()
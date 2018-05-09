import dummy

def guessT0(m, attempts=100):
	"Guess t0 of a given mixnet"
	g = -1
	i0 = 0
	for i in range(1, attempts):
		out, m = dummy.sendMessage(m)
		if out > 0 :
			print("Output on", i,":", out)
			if (g < 0 or (i - i0) < g):
				g = (i - i0)
				print("New guess:", g)
				i0 = i
		

	if(g >= 0):
		print("My guess is " + str(g) + " is (divisible by) t0")
	else :
		print("I have no guess for t0")

# Final mix t2:
# when t2 flushes, then t1 and t0 also flushed
# t2 <= t1: when t1 flushes, t2 flushes
# t2 > t1: then 
	# t2 > t1 * n for some n >= 1

def guessTn(m, attempts=100):
	"Guess tn of a given mixnet"
	g = -1
	for i in range(1, attempts):
		out, m = dummy.sendMessage(m)
		if out > 0 :
			# print("Output on", i,":", out)
			if (g < 0 or out < g):
				g = out
				# print("New guess:", out)
		
	if(g >= 0):
		print("My guess is " + str(g) + " is (divisible by) tn")
	else :
		print("I have no guess for t0")

	return g

def guessLCM(m, attempts=100):
	"Guess lcm of a given mixnet"
	g = -1
	for i in range(1, attempts):
		out, m = dummy.sendMessage(m)
		if out > 0 :
			# print("Output on", i,":", out)
			if (g < 0 or out < g):
				g = out
				# print("New guess:", out)
		
	if(g >= 0):
		print("My guess is " + str(g) + " is (divisible by) tn")
	else :
		print("I have no guess for t0")

	return g

guessTn( (3, [4, 6, 7], [0,0,0]), 10000)

def lcmn(l):
	a = lcm(l[0], l[1])
	for i in range(2, len(l)):
		a = lcm(a , l[i])
	return a

def gcd(a, b):
    """Calculate the Greatest Common Divisor of a and b.

    Unless b==0, the result will have the same sign as b (so that when
    b is divided by it, the result comes out positive).
    """
    while b:
        a, b = b, a%b
    return a

def lcm(x, y):
   if x > y:
       z = x
   else:
       z = y

   while(True):
       if((z % x == 0) and (z % y == 0)):
           lcm = z
           break
       z += 1

   return lcm
def getInEqOutFlush(m):
	i = 0
	flushes = []
	while i < 10000:
		out, m = dummy.sendMessage(m)
		i += 1
		if out == i:
			return i

	print("Cant find in=out for " + str(m))
	return 1


def testGuessTn(attempts=10000):
	for i in range(100):
		m = dummy.randomMixnet(3)
		g = guessTn(m)
		assert g == m[1][2], "Guess tn does not work for " + str(m) + ", gives " + str(g)

def lcmOfInOut(m):
	f = dummy.getNFlushes(m,1)[0]
	return lcm(f[0], f[1])

m = (3, [4, 6, 7], [0,0,0])
print( lcmOfInOut(m) )
print( lcmn(m[1]))

def testLcmOfInOut(attempts=10000):
	for i in range(100):
		m = dummy.randomMixnet(3)
		g = lcmOfInOut(m)
		e = lcmn(m[1])
		e2 = e % g
		assert e2 == 0 or (g % e == 0), "Guess lcm does not work for " + str(m) + ", gives " + str(g) + ", expected " + str(e)

def guessLargestWithTwoFlushes(attempts=10000):
	for i in range(attempts):
		m = dummy.randomMixnet(3)
		f = dummy.getNFlushes(m, 2)
		l = lcmn(m[1])
		g = gcd(f[0][0], f[1][0])
		ok = f[0][1] in m[1] or l in m[1]
		assert g in m[1] or ok, "Guessed wrong, m: " + str(m) + ", guessed " + str(g) + ", expected x in " + str(m[1]) + " | " + str(f) + " | " + str(l)

def findInEqualsOut(attempts=10000):
	for i in range(attempts):
		m = dummy.randomMixnet(3)
		f = getInEqOutFlush(m)
		assert f > 0, "Naha"

def floorAss(attempts=10000):
	for i in range(attempts):
		m = dummy.randomMixnet(3)
		f = dummy.getNFlushes(m, 10)
		t123 = m[1][0] * m[1][1] * m[1][2]
		for j in f:
			x0 = j[0]
			x3 = j[1]
			g = math.floor(x0/t123) * t123
			assert g == x3, "Guessed wrong, m: " + str(m) + ", guessed " + str(g) + ", expected " + str(x3) 

# testGuessTn()

m1 = (3, [32,13,5], [0,0,0])
print( dummy.getNFlushes(m1, 3))

class Kupify:
	def next(self, previous_pattern):
		if(previous_pattern == 'z'):
			return 'aa'
		if(previous_pattern == ''):
			return 'a'			
		if(previous_pattern.endswith("z")):
			return self.next(previous_pattern[0:-1]) + 'a'
		else:
			return previous_pattern[0:-1] + chr(ord(previous_pattern[-1]) + 1)


def test():
	k = Kupify()
	return k.next("c")

print test()
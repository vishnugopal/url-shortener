class Kupify:
  def kupify_next(previous_pattern):
    if(previous_pattern.endswith("z"))
		  return kupify_next(previous_pattern[1:-1]) + 'a'
		else
      return previous_pattern[1:-1] + chr(ord(previous_pattern[-1]) + 1)
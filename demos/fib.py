
def fib(i):
  count = 0
  x = 0
  y = 1
  while count < i:
    count = count + 1
    x, y = y, x+y
  return y

  
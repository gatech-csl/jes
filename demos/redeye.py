
def decreaseRed(picture):
  for p in getPixels(picture):
    setRed(p, getRed(p) * 0.5)
  return picture

def decrease2(picture, x1, y1, x2, y2):
  for x in range(x1, x2):
    for y in range(y1, y2):
      p = getPixel(picture, x, y)
      setRed(p, getRed(p) * 0.5)
  return picture


orig = makePicture('/home/timmy/img/redeye.jpg')
fix = decrease2(duplicatePicture(orig), 135, 132, 145, 145)
fix2 = decreaseRed(duplicatePicture(orig))

show(fix)
show(fix2)

p = makePicture(pickAFile())
explore(p)
pixels = getPixels(p)
show(makePicture(pixels))

p = makePicture(pickAFile())
explore(makePicture([px for px in getPixels(p) if getRed(px) < 120]))
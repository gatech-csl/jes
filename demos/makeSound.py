s = makeSound(pickAFile())
s.play()
samples = getSamples(s)
makeSound(samples).explore()

s = makeSound(pickAFile())
explore(makeSound([smpl for smpl in getSamples(s) if getIndex(smpl)%5==0]))

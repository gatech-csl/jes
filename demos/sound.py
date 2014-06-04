def backwards(filename):
  source = makeSound(filename)
  target = makeSound(filename)

  sourceIndex = getLength(source)
  for targetIndex in range(1, getLength(target)+1):
    sourceValue = getSampleValueAt(source, sourceIndex)
    setSampleValueAt(target, targetIndex, sourceValue)
    sourceIndex = sourceIndex - 1

  return target


file = '/usr/lib/openoffice/share/gallery/sounds/train.wav'
s = makeSound(file)
s2 = backwards(file)


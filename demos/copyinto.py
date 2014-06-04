
a = makePicture('/home/timmy/tmp/f430-1.jpg')
b = makePicture('/home/timmy/tmp/f430-2.jpg')

bg = makeEmptyPicture(getWidth(a) + getWidth(b), getHeight(a) + getHeight(b))

copyInto(a, bg, 1,1)
copyInto(b, bg, getWidth(a),getHeight(a))

addText(bg, getWidth(a)+20, int(getHeight(a)/2), 'Side View of F430')
addText(bg, getWidth(a)-150, int(getHeight(a)/2)*3, 'Back View of F430')

show(bg)



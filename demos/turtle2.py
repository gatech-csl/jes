w = makeEmptyPicture(500, 500)
t = makeTurtle(w)
penUp(t)
moveTo(t, int(500/3), 250)
penDown(t)
movie = makeMovie()
for i in range(0, 20):
    turn(t, 3)
    forward(t, 3)
    addFrameToMovie(w, movie)


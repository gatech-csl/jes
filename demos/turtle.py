w = makeWorld(500, 500)
t = makeTurtle(w)
penUp(t)
moveTo(t, int(500/3), 250)
penDown(t)
for i in range(0, 360):
    turn(t, 1)
    forward(t, 3)


from orbit import Orbit

o = Orbit(100, 4, 1)
for i in range(10):
    o.advance(1)
    print(o.curr)

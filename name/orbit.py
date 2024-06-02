from math import pi, sin, cos, atan2

def next_point(r, w, point, delta):
    t = atan2(point[1], point[0])
    print(t)
    tp = t + w * delta
    print(tp/(2*pi))
    x = r * cos(tp)
    y = r * sin(tp)
    return (x,y)

class Orbit:
    def __init__(self, radius, period, tail_len):
        self.curr = (radius, 0)
        self.prev = []
        self.radius = radius
        # period is 2pi per time
        # omega is rad per second
        self.omega = (2 * pi) / period
        self.tail_len = tail_len

    def advance(self, delta):
        self.prev.append(self.curr)
        self.prev = self.prev[max(0, len(self.prev) - self.tail_len):]
        self.curr = next_point(self.radius, self.omega, self.curr, delta)

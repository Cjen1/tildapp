import app

from events.input import Buttons, BUTTON_TYPES

from math import pi, sin, cos, atan2

# Orbit : F x F -> Screen : P x P -> lines between

class Path:
    def __init__(self):
        self.data = []

    def add(self, point):
        self.data += point

    def filter(self):
        self.data = self.data[-retain:]

class PathTime:
    def __init__(self, retain):
        self.data = []
        self.retain = retain

    def add(self, time, point):
        matching = None
        for i, (t1, p1) in enumerate(self.data):
            if p1 = point and time > t1:
                matching = i
                continue
        if matching is None:
            self.data.append((time, point))
        else:
            assert self.data[i][0] = point
            self.data[i] = (time, point)

        sort(self.data, key=lambda (t,p): t)

    def filter(self, time):
        self.data = [(t,p) for (t,p) in self.data if t > time - self.retain]

class Orbit:
    def __init__(self, radius, period):
        self.radius = radius
        self.period = period

    def pos(self, t):
        theta = (2 * pi) * ( float(t % period) / period )
        y = self.radius * sin(theta)
        x = self.radius * cos(theta)

        return (x,y)

class Scene:
    def __init__(self):
        self.retain = 10
        self.vp = PathTime(retain)
        self.vo = Orbit()
        t = 0
        #self.ep = PathTime(retain)
        #self.eo = Orbit()
        #self.mp = PathTime(retain)
        #self.mo = Orbit()

    def update(self, dt):
        self.t += dt
        self.vp.add(self.vo.pos(self.t))

    def _draw_multiseg(self, ctx, pts):
        ctx.save()

        ctx.gray(0.5).begin_path()
        ctx.move_to(pts[0][0], pts[0][1])
        
        for pt in pts[1:]:
            ctx.line_to(pt[0], pt[1])

        ctx.stroke()

        ctx.restore()

    def draw(self, ctx):
        #clear
        ctx.rgb(0,0,0).rectangle(-120, -120, 240, 240).fill()

        #orbit: Venus
        if (self.vp.data):
            # Orbit path
            self.draw_multiseg(ctx, self.vp.data)
            # Object
            ctx.gray(1).arc(
                    self.vp.data[-1][0], #x
                    self.vp.data[-1][1], #y
                    4, # radius
                    0, 2*pi, # range
                    True # direction
                    ).fill()

def dist_to_circle(r, x, y):
    s = (x * x + y * y - r * r)
    return s * s

def next_point_int(r, point, prev):
    x,y = point
    dxs = [ 1,1,1,  0,  0, -1,-1,-1]
    dys = [-1,0,1, -1,  1, -1, 0, 1]

    min_dist = 1e100
    min_point = (x + dxs[0], y + dys[0])

    for i, _ in enumerate(dxs):
        dx = dxs[i]
        dy = dys[i]

        new_point = (int(x+dx), int(y+dy))

        dist = dist_to_circle(r, new_point[0], new_point[1])
        if dist < min_dist and new_point not in prev:
            min_point = (x+dx, y + dy)
            min_dist = dist

    return min_point

def next_point(r, w, point, delta):
    t = atan2(point[1], point[0])
    tp = t + w * delta
    x = r * cos(tp)
    y = r * sin(tp)
    return (x,y)

class Orbit:
    def __init__(self, radius, period, tail_len):
        self.curr = (radius, 0)
        self.ct = 0
        self.prev = []
        self.radius = radius
        # period is 2pi per time
        # omega is rad per second
        self.omega = (2 * pi) / period
        self.tail_len = tail_len

    def advance(self, delta):
        self.prev.append((self.ct, self.curr))
        self.prev = [(t,p) for t, p in self.prev if t > self.ct + delta - self.tail_len]
        self.ct += delta
        self.curr = next_point(self.radius, self.omega, self.curr, delta)

class MainClass(app.App):
    person_name = ["Chris Jensen"]
    mastodon = ["@cjen1","@discuss.", "\tsystems"]

    def __init__(self):
        self.button_states = Buttons(self)
        self.state = "person_name"
        self.orbit = Orbit(100, 10, 1)

    def update(self, delta):
        if self.button_states.get(BUTTON_TYPES['CANCEL']):
            self.minimise()
        elif self.button_states.get(BUTTON_TYPES['UP']):
            self.state = "person_name"
        elif self.button_states.get(BUTTON_TYPES['DOWN']):
            self.state = "mastodon"
        self.button_states.clear()

        self.orbit.advance(delta/1000)

    def draw_centered_text(self, ctx, text, rgbargs=(1,1,1), y=0):
        width = ctx.text_width(text)
        ctx.rgb(*rgbargs).move_to(-width/2, y).text(text)

    def draw_multiline_centered_text(self, ctx, textbuf, **kwargs):
        height = 25
        total_height = len(textbuf) * height
        start_height = - total_height / 2 + 10
        for yi, txt in enumerate(textbuf):
            y = int(yi * height + start_height)
            self.draw_centered_text(ctx, txt, y=y, **kwargs)

    def draw_multiseg(self, ctx, pts):
        ctx.save()

        ctx.gray(0.5).begin_path()
        ctx.move_to(pts[0][0], pts[0][1])
        
        for pt in pts[1:]:
            ctx.line_to(pt[0], pt[1])

        ctx.stroke()

        ctx.restore()

    def draw_orbit(self, ctx):
        pts = [p for _,p in self.orbit.prev] + [self.orbit.curr]

        self.draw_multiseg(ctx, pts)

        curr = self.orbit.curr
        ctx.gray(1).arc(curr[0], curr[1], 4, 0, 2 * pi, True).fill()

    def draw(self, ctx):
        #clear
        ctx.rgb(0,0,0).rectangle(-120, -120, 240, 240).fill()

        #orbit
        self.draw_orbit(ctx)

        #text
        if self.state == "person_name":
            self.draw_multiline_centered_text(ctx, self.person_name)
        elif self.state == "mastodon":
            self.draw_multiline_centered_text(ctx, self.mastodon)

__app_export__ = MainClass

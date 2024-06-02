import app

from events.input import Buttons, BUTTON_TYPES

from math import pi, sin, cos, atan2

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
    mastodon = ["@cjen1","@discuss.systems"]

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

import app

from events.input import Buttons, BUTTON_TYPES

from math import pi, sin, cos, atan2

# Orbit : F x F -> Screen : P x P -> lines between

class Path:
    def __init__(self, retain):
        self.data = []
        self.retain = retain

    def add(self, point):
        self.data.append(point)

    def filter(self):
        self.data = self.data[-self.retain:]

class PathTime:
    def __init__(self, retain):
        self.data = []
        self.retain = retain

    def add(self, time, point):
        matching = None
        for i, (t1, p1) in enumerate(self.data):
            if p1 == point and time > t1:
                matching = i
        if matching is None:
            self.data.append((time, point))
        else:
            assert self.data[matching][1] == point
            self.data[matching] = (time, point)

        self.data.sort(key=lambda item: item[0])

    def filter(self, time):
        self.data = [(t,p) for (t,p) in self.data if t > time - self.retain]

class Orbit:
    def __init__(self, radius, period):
        self.radius = radius
        self.period = period

    def pos(self, t):
        theta = (2 * pi) * (float(t % self.period) / self.period)
        y = self.radius * sin(theta)
        x = self.radius * cos(theta)

        return (x,y)


def draw_multiseg(ctx, pts):
    ctx.save()

    ctx.gray(0.5).begin_path()
    ctx.move_to(pts[0][0], pts[0][1])
    
    for pt in pts[1:]:
        ctx.line_to(pt[0], pt[1])

    ctx.stroke()

    ctx.restore()

class Scene:
    def __init__(self):
        self.t = 0
        self.vp = PathTime(2)
        self.vo = Orbit(50, 6)
        self.ep = PathTime(2)
        self.eo = Orbit(90, 11)
        self.mp = PathTime(3)
        self.mo = Orbit(20, 2)

    def update(self, dt):
        self.t += dt / 1000

        vp = self.vo.pos(self.t)
        self.vp.add(self.t, (int(vp[0]), int(vp[1])))
        self.vp.filter(self.t)

        ep = self.eo.pos(self.t)
        self.ep.add(self.t, (int(ep[0]), int(ep[1])))
        self.ep.filter(self.t)

        mp = self.mo.pos(self.t)
        self.mp.add(self.t, (int(ep[0] + mp[0]), int(ep[1] + mp[1])))
        self.mp.filter(self.t)

    def draw(self, ctx):
        #clear
        ctx.rgb(0,0,0).rectangle(-120, -120, 240, 240).fill()

        #orbit: Venus
        if (self.vp.data):
            # Orbit path
            draw_multiseg(ctx, [point for _, point in self.vp.data])
            # Object
            _, (x, y) = self.vp.data[-1]
            ctx.gray(1).arc(
                    x, #x
                    y, #y
                    4, # radius
                    0, 2*pi, # range
                    True # direction
                    ).fill()

        if (self.ep.data):
            draw_multiseg(ctx, [point for _, point in self.ep.data])
            _, (x,y) = self.ep.data[-1]
            ctx.gray(1).arc(
                    x,
                    y,
                    4,
                    0, 2*pi,
                    True
                    ).fill()

        if (self.mp.data):
            draw_multiseg(ctx, [point for _, point in self.mp.data])
            _, (x,y) = self.mp.data[-1]
            ctx.gray(1).arc(
                    x,
                    y,
                    2,
                    0, 2*pi,
                    True,
                    ).fill()

class MainClass(app.App):
    person_name = ["Chris Jensen"]
    mastodon = ["@cjen1","@discuss.", "\tsystems"]

    def __init__(self):
        self.button_states = Buttons(self)
        self.state = "person_name"
        self.scene = Scene()

    def update(self, delta):
        if self.button_states.get(BUTTON_TYPES['CANCEL']):
            self.minimise()
        elif self.button_states.get(BUTTON_TYPES['UP']):
            self.state = "person_name"
        elif self.button_states.get(BUTTON_TYPES['DOWN']):
            self.state = "mastodon"
        self.button_states.clear()

        self.scene.update(delta)

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

    def draw(self, ctx):
        # clear
        ctx.rgb(0,0,0).rectangle(-120, -120, 240, 240).fill()

        # orbit
        self.scene.draw(ctx)

        # text
        if self.state == "person_name":
            self.draw_multiline_centered_text(ctx, self.person_name)
        elif self.state == "mastodon":
            self.draw_multiline_centered_text(ctx, self.mastodon)

__app_export__ = MainClass

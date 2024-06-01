import app

from events.input import Buttons, BUTTON_TYPES

class MainClass(app.App):
    person_name = ["Chris Jensen"]
    mastodon = ["@cjen1","@discuss.systems"]

    def __init__(self):
        self.button_states = Buttons(self)
        self.state = "person_name"

    def update(self, delta):
        if self.button_states.get(BUTTON_TYPES['CANCEL']):
            self.minimise()
        elif self.button_states.get(BUTTON_TYPES['UP']):
            self.state = "person_name"
            print(self.state)
        elif self.button_states.get(BUTTON_TYPES['DOWN']):
            self.state = "mastodon"
            print(self.state)
        elif self.button_states.get(BUTTON_TYPES['LEFT']):
            self.state = "error";
            print(self.state)
        self.button_states.clear()

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
        ctx.rgb(0,0,0).rectangle(-120, -120, 240, 240).fill()
        if self.state == "person_name":
            self.draw_multiline_centered_text(ctx, self.person_name)
        elif self.state == "mastodon":
            self.draw_multiline_centered_text(ctx, self.mastodon)

__app_export__ = MainClass

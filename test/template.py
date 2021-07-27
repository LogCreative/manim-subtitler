from manimlib import *

class SubLine:
    def __init__(self, caption, fadeIn, duration, fadeOut):
        self.caption = caption
        self.fadeIn = fadeIn
        self.duration = duration
        self.fadeOut = fadeOut

    # Overlapping is not allowed.

subLines = [
    "Hello, world!",
    "LogCreative"
]

class DisplayLines(Scene):
    def construct(self):
        for subLine in subLines:
            line = Text(subLine)
            self.play(FadeIn(line), run_time=1)
            self.wait(5)
            self.play(FadeOut(line), run_time=1)

if __name__=="__main__":
    DisplayLines()
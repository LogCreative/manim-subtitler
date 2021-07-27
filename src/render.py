import re
from manimlib import *
from numpy import empty

class SubLine:
    def __init__(self, caption, fadeIn, duration, fadeOut, space):
        self.caption = caption
        self.fadeIn = fadeIn
        self.duration = duration
        self.fadeOut = fadeOut
        self.space = space

    # Overlapping is not allowed.

subLines = [
    SubLine("Hello, world!",1,1,1,1),
    SubLine("LogCreative",1,1,1,1),
    SubLine("2021 $A$ \(A\)",1,1,1,1)
]

class DisplayLines(Scene):
    def construct(self):
        # Read line from csv
        # If it is an online version,
        # use JSON for transmission.
        for subLine in subLines:
            # Read the text
            # TODO: next_to(Mobject)
            # TODO: wait
            
            # TODO: replace \(.+\) to $.+$ using re
            subLine.caption = subLine.caption.replace("\\(","$").replace("\\)","$")
            
            captionList = []
            stack_str = ""
            in_equation = False
            prev = ""
            for c in subLine.caption:
                if c=='$':
                    if not in_equation:
                        cur = Text(stack_str)
                    else:
                        cur = Tex(stack_str)                        
                    if not prev=="":
                        cur.next_to(prev)
                    captionList.append(cur)
                    prev = cur
                    in_equation != in_equation
                else:
                    stack_str += c
            if stack_str != "":
                cur = Text(stack_str)
                if not prev=="":
                    cur.next_to(prev)
                captionList.append(cur)
            
            # Fade In animation
            for el in captionList:
                self.play(FadeIn(el), run_time=subLine.fadeIn)
            # Hold for some while
            self.wait(subLine.duration)
            # Fade Out animation
            for el in captionList:
                self.play(FadeOut(el), run_time=subLine.fadeOut)
            # Space after this line
            self.wait(subLine.space)

if __name__=="__main__":
    DisplayLines()
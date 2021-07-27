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
    SubLine("2021 $A$  \(A\)",1,1,1,1)
]

class DisplayLines(Scene):
    def construct(self):
        # Read line from csv
        # If it is an online version,
        # use JSON for transmission.
        for subLine in subLines:
            # Read the text

            subLine.caption = subLine.caption.replace("\\(","$").replace("\\)","$")
            # avoid bug: space between TexObject
            subLine.caption = re.sub("\$\s+\$","$$",subLine.caption)
            # compose Text and Tex
            captionList = []
            stack_str = ""
            in_equation = False
            for c in subLine.caption:
                if c=='$':
                    if not in_equation:
                        captionList.append(Text(stack_str))
                    else:
                        captionList.append(Tex(stack_str))
                    stack_str = ""
                    in_equation = not in_equation
                else:
                    stack_str += c
            if stack_str != "":
                captionList.append(Text(stack_str))

            line = VGroup(*captionList)
            line.arrange()
            
            # Fade In animation
            self.play(FadeIn(line), run_time=subLine.fadeIn)
            # Hold for some while
            self.wait(subLine.duration)
            # Fade Out animation
            self.play(FadeOut(line), run_time=subLine.fadeOut)
            # Space after this line
            self.wait(subLine.space)

if __name__=="__main__":
    DisplayLines()
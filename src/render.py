FONT_SIZE = 30

import re
import csv
from manimlib import *

class SubLine:
    def __init__(self, caption, space, fadeIn, duration, fadeOut):
        self.caption = caption
        self.space = space
        self.fadeIn = fadeIn
        self.duration = duration
        self.fadeOut = fadeOut

    # Overlapping is not allowed.

class DisplayLines(Scene):
    def construct(self):
        # Read line from csv
        # TODO: If it is an online version,
        # use JSON for transmission.
        with open("subtitle.csv","r",encoding="UTF-8") as f:
            reader = csv.reader(f)
            for row in reader:
                # Read the text
                subLine = SubLine(row[0], float(row[1]), float(row[2]), float(row[3]), float(row[4]))

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
                            captionList.append(Text(stack_str, font_size = FONT_SIZE, font="Simhei"))
                        else:
                            # TODO: tempory fix on \text
                            stack_str = re.sub("\\text\{(.+)\}","{\\rm $1}",stack_str)
                            captionList.append(Tex(stack_str))
                        stack_str = ""
                        in_equation = not in_equation
                    else:
                        stack_str += c
                if stack_str != "":
                    captionList.append(Text(stack_str, font_size=FONT_SIZE, font="Simhei"))

                line = VGroup(*captionList)
                line.arrange()
                
                # Space before this line
                self.wait(subLine.space)
                # Fade In animation
                self.play(FadeIn(line), run_time=subLine.fadeIn)
                # Hold for some while
                self.wait(subLine.duration)
                # Fade Out animation
                self.play(FadeOut(line), run_time=subLine.fadeOut)

if __name__=="__main__":
    DisplayLines()
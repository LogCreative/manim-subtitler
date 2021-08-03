# MIT License
# 
# Copyright (c) 2021 LogCreative

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
            subLines = []
            for row in reader:
                # Read the text
                subLine = SubLine(row[0], float(row[1]), float(row[2]), float(row[3]), float(row[4]))

                subLine.caption = subLine.caption.replace("\\(","$").replace("\\)","$")
                # avoid bug: space between TexMObject or linebreak
                subLine.caption = re.sub("\$\s+\$","$$",subLine.caption)
                subLine.caption = re.sub("\$\s+\n","$\n",subLine.caption)

                # break block by lines
                lineList = []
                lines = subLine.caption.split("\n")
                for line in lines:
                    # compose Text and Tex
                    captionList = []
                    stack_str = ""
                    in_equation = False
                    for c in line:
                        if c=='$':
                            if not in_equation:
                                captionList.append(Text(stack_str,  font="Simhei"))
                            else:
                                captionList.append(Tex(stack_str))
                            stack_str = ""
                            in_equation = not in_equation
                        else:
                            stack_str += c
                    if stack_str != "":
                        captionList.append(Text(stack_str,  font="Simhei"))
                    lineGroup = VGroup(*captionList)
                    lineGroup.arrange()
                    lineList.append(lineGroup)
                blockGroup = VGroup(*lineList)
                blockGroup.arrange(direction=DOWN)
                subLines.append([subLine, blockGroup])

            for i,line in enumerate(subLines):
                subLine = line[0]
                blockGroup = line[1]
                
                # If the space is smaller than 0
                # the line has been fadeIn already
                if subLine.space>=0:
                    # Space before this line
                    self.wait(subLine.space)
                    # Fade In animation
                    # TODO: You can change to other effects 
                    self.play(DrawBorderThenFill(blockGroup), run_time=subLine.fadeIn)
                
                # Hold for some while
                self.wait(subLine.duration)

                if i+1<len(subLines) and subLines[i+1][0].space < 0:
                    # load the next line
                    nextBlockGroup = subLines[i+1][1]
                    # play the transformation animation between two lines
                    self.play(ReplacementTransform(blockGroup, nextBlockGroup), run_time=subLine.fadeOut)
                else:
                    # Fade Out animation
                    # TODO: You can change to other effects
                    self.play(Uncreate(blockGroup), run_time=subLine.fadeOut)

if __name__=="__main__":
    DisplayLines()
# MIT License
# 
# Copyright (c) 2021 LogCreative

import re
import datetime
import sys

# ---|----     ---|---

FADEIN = 0.5
FADEOUT = 0.5

class SrtLine:
    def __init__(self, caption, start, end):
        self.caption = caption
        self.start = start
        self.end = end

class Parser:
    def __init__(self, filePath):
        self.filePath = filePath

    def split_block(self):
        self.stack_blocks = []

        def append_block(stack_block):
            if not stack_block=="\n":
                self.stack_blocks.append(stack_block)

        with open(self.filePath, 'r', encoding='UTF-8') as f:
            stack_block = ""
            for line in f:
                if line=="\n":
                    append_block(stack_block)
                    stack_block = ""
                else:
                    stack_block += line
            if stack_block != "":
                append_block(stack_block)

    def parse_block(self):
        self.srtLines = []
        for block in self.stack_blocks:
            block_info = re.search(r"(?P<id>\d+)\n(?P<sh>\d\d):(?P<sm>\d\d):(?P<ss>\d\d),(?P<sms>\d\d\d) --> (?P<eh>\d\d):(?P<em>\d\d):(?P<es>\d\d),(?P<ems>\d\d\d)", block, re.M)
            block_caption = block[block_info.end():].strip("\n")
            self.srtLines.append(SrtLine(block_caption, 
                datetime.time(int(block_info['sh']), int(block_info['sm']), int(block_info['ss']), int(block_info['sms'])),
                datetime.time(int(block_info['eh']), int(block_info['em']), int(block_info['es']), int(block_info['ems']))    
            ))

    def calcu_block(self, fileOut):
        def second_time(second):
            return datetime.time(second=int(second),microsecond=int((second - int(second))*1000))

        def get_second(t):
            return t.hour * 3600 + t.minute * 60 + t.second + t.microsecond / 1000

        def diff_second(f, e):
            fs = get_second(f)
            es = get_second(e)
            return fs - es

        def add_second(t, s):
            ts = get_second(t)
            ts += s
            tsn = int(ts)
            tsm = int((ts - tsn) * 1000)
            return datetime.time(int(tsn / 3600), int(tsn / 60), tsn % 60, tsm)

        with open(fileOut, 'w', encoding='UTF-8') as f:
            prev = datetime.time(0,0,0,0)
            for i,srtLine in enumerate(self.srtLines):
                fadeIn = FADEIN
                space = diff_second(srtLine.start, prev) - FADEIN / 2.0
                if space<0:
                    fadeIn += space
                    duration = diff_second(srtLine.end, prev)
                    if fadeIn<0:
                        fadeIn = 0
                        duration -= FADEOUT / 2.0
                    else:
                        duration -= FADEOUT / 2.0 + fadeIn
                    if i>0 and self.srtLines[i-1].end == srtLine.start:
                        # When the beginning of the this line
                        # is the same as the end of prev line
                        # then the special effect of
                        # ReplacementTransform
                        # will be applied between the two lines
                        #
                        # ---|---                ---|---
                        #  --|--  (FADEIN)  =>   ---|--- (FADEOUT)
                        space = - FADEOUT
                        duration = diff_second(srtLine.end, self.srtLines[i-1].end) - FADEOUT
                    else:
                        space = 0
                else:
                    duration = diff_second(srtLine.end, srtLine.start) - FADEOUT / 2.0 - FADEIN / 2.0
                prev = add_second(srtLine.end, FADEOUT / 2.0)
                f.write("\"" + srtLine.caption.replace("\n"," ") + "\"," + str(space) + "," + str(fadeIn) + "," + str(duration) + "," + str(FADEOUT) + "\n")

    def output(self, fileOut):
        self.split_block()
        self.parse_block()
        self.calcu_block(fileOut)
        

if __name__=="__main__":
    if len(sys.argv) < 2:
        filePath = input("Input the subtitle file path (.srt): ")
    else:
        filePath = sys.argv[1]
    p = Parser(filePath)
    p.output("subtitle.csv")
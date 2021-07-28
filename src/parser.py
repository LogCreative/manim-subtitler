import re

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

    def output(self):
        self.split_block()
        
        for block in self.stack_blocks:
            block_info = re.search(r"(?P<id>\d+)\n(?P<sh>\d\d):(?P<sm>\d\d):(?P<ss>\d\d),(?P<sms>\d\d\d) --> (?P<eh>\d\d):(?P<em>\d\d):(?P<es>\d\d),(?P<ems>\d\d\d)", block, re.M)
            block_caption = block[block_info.end():].strip("\n")
            print(block_caption)

if __name__=="__main__":
    filePath = input("Input the subtitle file path (.srt): ")
    p = Parser(filePath)
    p.output()
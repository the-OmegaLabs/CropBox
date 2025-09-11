# OmegaOS CropBox - cat
# Author: Stevesuk0 (stevesukawa@outlook.com)
# Modification: bzym2 (yakamoawa@outlook.com)
# Modification: Google Gemini 2.5 Pro (aistudio.google.com)
#
# Description:
#     OmegaOS CropBox version of the 'cat' command.
#     Maybe compatible with POSIX 'cat' behavior, with minor adjustments.
#
# Usage:
#     cat [OPTIONS]... [FILE]...
#
# Function:
#     Reads each FILE in sequence and writes its contents to standard output.
#     If no FILE is provided or FILE is '-', reads from standard input.
#
# Options:
#     -    Argument head.
#     n    Number all output lines.
#     b    Number only non-empty output lines.
#     s    Squeeze multiple consecutive blank lines into one.
#     E    Display '$' at the end of each line.
#     T    Display TAB characters as '^I'.
#
# Examples:
#     cat file.txt
#         Print the contents of file.txt to standard output.
#
#     cat
#         Read from standard input until EOF (Ctrl+D).

import os
import sys
import string

from cropbox.commandBase import CommandBase


class Cat(CommandBase):
    def __init__(self, args):
        super().__init__(args)
        self.count_line = False
        self.count_line_skip_empty = False
        self.end_sign = False
        self.show_tabs = False
        self.show_nonprint = False

        self.options = []
        self.files = []

    def parse_args(self):
        for arg in self.args:
            if arg.startswith('-') and arg != '-':
                # 这样可以支持像 -nE 这样的组合 很爽
                for char in arg[1:]:
                    if char == 'n':
                        self.count_line = True
                    elif char == 'b':
                        self.count_line = True
                        self.count_line_skip_empty = True
                    elif char == 'E':
                        self.end_sign = True
                    elif char == 'T':
                        self.show_tabs = True
                    elif char == 'v':
                        self.show_nonprint = True
                    elif char == 'A':
                        self.end_sign = True
                        self.show_tabs = True
                        self.show_nonprint = True
                    elif char == 'u':
                        # POSIX -u 选项是禁用输出缓冲，Python的 print 默认就是行缓冲
                        pass
                    else:
                        self.error(f"invalid option -- '{char}'")
            else:
                # 那这就是一个文件名或 stdin ('-')
                self.files.append(arg)

    def run(self):
        self.parse_args()

        if not self.files:
            # 没有文件就直接从stdin里读
            self.process_stdin()
        else:
            for file_path in self.files:
                if file_path == '-':
                    self.process_stdin()
                elif os.path.exists(file_path):
                    if os.path.isdir(file_path):
                        self.error(f"{file_path}: Is a directory")
                    else:
                        self.process_file(file_path)
                else:
                    self.error(f"{file_path}: No such file or directory")

    def make_visible(self, text):
        res = ''
        for c in text:
            if c == '\t' and self.show_tabs:
                res += '^I'
            elif (ord(c) < 32 or ord(c) > 126) and c not in ('\t', '\n') and self.show_nonprint:
                # M-x (Meta-x) for characters > 127
                if ord(c) > 127:
                    res += 'M-^' + chr((ord(c) - 128) ^ 0x40)
                # ^x for control characters
                else:
                    res += '^' + chr(ord(c) ^ 0x40)
            else:
                res += c
        return res

    def process_stream(self, stream):
        cnt = 0
        for line in stream:
            line_content = line.rstrip('\n')

            # 处理 -b 选项（只计数非空行）
            if self.count_line:
                is_empty = not line_content.strip()
                if self.count_line_skip_empty and is_empty:
                    sys.stdout.write('\n')
                    continue
                cnt += 1
                sys.stdout.write(f"{cnt:6}\t")

            line_content = self.make_visible(line_content)
            sys.stdout.write(line_content)

            if self.end_sign:
                sys.stdout.write('$')

            sys.stdout.write('\n')
        sys.stdout.flush()

    def process_file(self, path):
        with open(path, 'r', errors='replace') as f:
            self.process_stream(f)

    def process_stdin(self):
        self.process_stream(sys.stdin)


# 先这么干 做假入口
# 因为主文件还没写 写了再弄
if __name__ == "__main__":
    Cat.main()
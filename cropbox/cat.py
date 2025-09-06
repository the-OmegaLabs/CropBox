# OmegaOS CropBox - cat
# Author: Stevesuk0 (stevesukawa@outlook.com)
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
#     -n    Number all output lines.
#     -b    Number only non-empty output lines.
#     -s    Squeeze multiple consecutive blank lines into one.
#     -E    Display '$' at the end of each line.
#     -T    Display TAB characters as '^I'.
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

class Main:
    def __init__(self, args):
        self.count_line = False
        self.count_line_skip_empty = False
        self.end_sign = False
        self.show_tabs = False
        self.show_nonprint = False
        self.flush_immediately = False

        if len(args) == 0:
            self.cat_stdin()
        else:
            for i in args:
                if i == '-':
                    self.cat_stdin()
                elif i == '-n':
                    self.count_line = True
                elif i == '-b':
                    self.count_line = True
                    self.count_line_skip_empty = True
                elif i == '-E':
                    self.end_sign = True
                elif i == '-T':
                    self.show_tabs = True
                elif i == '-v':
                    self.show_nonprint = True
                elif i == '-A':  # show-all
                    self.end_sign = True
                    self.show_tabs = True
                    self.show_nonprint = True
                elif i == '-u':
                    self.flush_immediately = True
                elif os.path.exists(i):
                    self.cat_file(i)
                else:
                    print(f"cat: {i}: No such file or directory", file=sys.stderr)
                    sys.exit(1)

    def make_visible(self, text):
        res = ''
        for c in text:
            if c == '\t' and self.show_tabs:
                res += '^I'
            elif c not in string.printable and self.show_nonprint:
                res += '^' + chr(ord(c) ^ 0x40)
            else:
                res += c
        return res

    def cat_file(self, path):
        with open(path, 'r', errors='replace') as f:
            cnt = 0
            for i in f:
                line = i.rstrip('\n')
                if self.count_line:
                    if self.count_line_skip_empty and not line.strip():
                        sys.stdout.write('\n')
                        continue
                    cnt += 1
                    sys.stdout.write(f'{cnt}  ')
                line = self.make_visible(line)
                sys.stdout.write(line)
                if self.end_sign:
                    sys.stdout.write('$')
                sys.stdout.write('\n')
                if self.flush_immediately:
                    sys.stdout.flush()

    def cat_stdin(self):
        while True:
            content = input()

            raw_content = str(content.encode())[2:-1]

            if raw_content == '\\x04':
                break
            else:
                raw_content = self.make_visible(raw_content)
                sys.stdout.write(raw_content)
                if self.end_sign:
                    sys.stdout.write('$')
                sys.stdout.write('\n')
                if self.flush_immediately:
                    sys.stdout.flush()
            


try:
    args = sys.argv
    args.pop(0) # clear module path

    Main(args)
except KeyboardInterrupt:
    pass

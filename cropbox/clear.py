# OmegaOS CropBox - clear
# Author: bzym2 (yakamoawa@outlook.com)
#
# Description:
#     OmegaOS CropBox version of the 'clear' command.
#
# Usage:
#     clear
#
# Function:
#     Clear things on your terminal.
#

import os
import sys

from cropbox.commandBase import CommandBase


class Main(CommandBase):
    def __init__(self, args):
        super().__init__(args)

    def parse_args(self):
        if self.args:
            self.error("clear: takes no arguments")

    def run(self):
        self.parse_args()
        if os.name == 'nt':
            os.system('cls')
        else:
            # 在 POSIX 系统 (Linux, macOS) 上，我们发送 ANSI 转义码。
            # '\033[2J'：清空整个屏幕。
            # '\033[H'：将光标移动到主屏幕的左上角 (第一行，第一列)。
            sys.stdout.write('\033[2J\033[H')
            sys.stdout.flush()

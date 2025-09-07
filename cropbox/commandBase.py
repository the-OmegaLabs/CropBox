# OmegaOS CropBox - commandBase
# Author: Google Gemini 2.5 Pro (aistudio.google.com)
# Modification: bzym2 (yakamoawa@outlook.com)
#
# Description:
#     Parent class for all commands.
#

import sys
import os


class CommandBase:
    def __init__(self, args):
        self.args = args
        self.command_name = os.path.basename(sys.argv[0]).replace('.py', '')

    def parse_args(self):
        raise NotImplementedError("子类必须实现 parse_args()")

    def run(self):
        raise NotImplementedError("子类必须实现 run()")

    def error(self, message, exit_code=1):
        print(f"{self.command_name}: {message}", file=sys.stderr)
        sys.exit(exit_code)

    @classmethod
    def main(cls):
        try:
            # cls(sys.argv[1:]) 会创建子类的一个实例
            instance = cls(sys.argv[1:])
            instance.run()
        except KeyboardInterrupt:
            # 打印一个换行符以避免终端提示符出现在中断的行上
            print()
            sys.exit(130)
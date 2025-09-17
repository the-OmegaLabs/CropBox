# 这个文件用来作为cropbox主入口
# 因为我们后面要改env管理器 所以把每个py文件全部都独立编译一遍是比较狗屎的
# 我想的是在env里把crop的命令单独映射到cropbox <命令名>
# 首先这样只要一次编译
# 其次就是有个父类可以很好的模块化与统一管理
# 就不像这个windows拉了一大坨屎 不方便维护 你还不敢动
# 如果你觉得这个设计不行的话
# 你直接把他revert就行了

from cropbox import cat, clear

modules = {
    "cat" : cat,
    "clear" : clear
}

def call_module(arg_tuple):
    name, *params = arg_tuple
    if name not in modules:
        raise ValueError(f"模块 {name} 不存在")
    cmd = modules[name].Main(params)
    return cmd.run()


if __name__ == "__main__":
    call_module(("cat", "LICENSE"))
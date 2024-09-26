import os,sys
Version="2.0"
def GetPath():
    if getattr(sys, 'frozen', False):
        # 如果程序是通过 PyInstaller 打包的
        return os.path.dirname(sys.executable)
    else:
        # 如果在开发环境中运行
        return os.path.dirname(os.path.abspath(__file__))
def GetIconpath():
    return os.path.join(GetPath(),"NcuNetLimiter.ico")
def GetConfigspath():
    return os.path.join(GetPath(),"Configs.txt")
def GetExeclsivepath():
    return os.path.join(GetPath(),"NcuNetLimiter.exe")
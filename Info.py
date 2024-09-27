import os,sys
Version="2.0"
LastDetectedTraffic='尚未開始偵測'
def GetPath():
    if getattr(sys, 'frozen', False):
        # 如果程序是通过 PyInstaller 打包的
        return os.path.dirname(sys.executable)
    else:
        # 如果在开发环境中运行
        return os.path.dirname(os.path.abspath(__file__))
def GetInternalPath():
    if getattr(sys, 'frozen', False):
        # 如果程序是通过 PyInstaller 打包的
        return os.path.join(os.path.dirname(sys.executable),"_internal")
    else:
        # 如果在开发环境中运行
        return os.path.dirname(os.path.abspath(__file__))
def GetIconpath():
    return os.path.join(GetInternalPath(),"NcuNetLimiter.ico")
def GetConfigspath():
    return os.path.join(GetInternalPath(),"Configs.txt")
def GetExeclsivepath():
    return os.path.join(GetPath(),"NcuNetLimiter.exe")
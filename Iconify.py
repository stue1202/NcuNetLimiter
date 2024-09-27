import tkinter as tk
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
import threading
import sys
import Info,Crwal

# 显示窗口
def show_window():
    print("P")
    global ico,win
    ico.stop()  # 停止托盘图标
    win.deiconify()
    print("i")# 恢复Tkinter窗口

# 最小化到托盘
def minimize_to_tray(window,SaveQuit):
    print("p")
    global win
    win=window
    win.withdraw()  # 隐藏窗口
    #Notify.notify("通知","正在後台運作")
    threading.Thread(target=show_tray_icon).start()
    
# 显示托盘图标
def show_tray_icon():
    global win,ico
    icon = Icon("test_icon", Image.open(Info.GetIconpath()), f"當前上傳量:%s"%Crwal.GetLastDetectedTraffic(),menu=Menu(
    MenuItem(text="show window",action=show_window,default=True)
))
    ico=icon
    icon.run()

# 退出程序
def quit_app(icon=None, item=None):
    if icon:
        icon.stop()  # 停止托盘图标
    # 停止Tkinter主循环
    sys.exit()


import tkinter as tk
from tkinter import messagebox
import Crwal
import webbrowser
import re
import AutoStart
import os,sys

def get_executable_directory():
    if getattr(sys, 'frozen', False):
        # 如果程序是通过 PyInstaller 打包的
        return os.path.dirname(sys.executable)
    else:
        # 如果在开发环境中运行
        return os.path.dirname(os.path.abspath(__file__))
current_directory = get_executable_directory()
# 打印当前程序所在目录
print(get_executable_directory())
def UpdateConfig():
    Configs=open(os.path.join(current_directory,'configs.txt'),"w")
    Configs.write(YourIp.get().strip()+'\n'+str(IsAutoStart.get())+'\n'+TrafficMaxValue.get().strip())
    Configs.close()
def StopScanning():
    Crwal.StopScanning()
    StopScanButton['state']=tk.DISABLED
    ScanButton['state']=tk.ACTIVE
def CheckState():
    if not re.match(r'\d+',TrafficMaxValue.get().strip()) :
        messagebox.showerror("錯誤","請輸入數字")
    elif not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',YourIp.get().strip()):
        messagebox.showerror("錯誤","請輸入正確IP位置格式")
    else:
        UpdateConfig()
        StopScanButton['state']=tk.ACTIVE
        ScanButton['state']=tk.DISABLED
        Crwal.StartDetect(Log.insert,'1.0',YourIp.get(),TrafficMaxValue.get())
def AutoStartCheck():
    UpdateConfig()
    if IsAutoStart.get():
        AutoStart.add_startup_item(os.path.join(current_directory,"NcuNetLimiter.exe") )
    else:
        AutoStart.remove_startup_item("NcuNetLimiter.exe")
window = tk.Tk()
window.title('NcuNetLimiter')
window.iconbitmap(os.path.join(current_directory,'NcuNetLimiter.ico'))
window.geometry('380x400')

menubar = tk.Menu()
#edit = tk.Menu(menubar, tearoff=0)
#menubar.add_cascade(label='Settings', menu=edit)
#edit.add_command(label='設定報警筏值', command=None)
#edit.add_separator()
#edit.add_command(label='設定開機自起動', command=None)
help_ = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=help_)
help_.add_command(label='關於此程式', command=lambda:webbrowser.open("https://github.com/stue1202/NcuNetLimiter"))
window.config(menu=menubar)

label = tk.Label(window, text="輸入你的IP")
YourIp = tk.Entry(window)
Log = tk.Text(window, height=10, width=30)
ScanButton = tk.Button(window, text="開始偵測", command=CheckState)
StopScanButton=tk.Button(window, text="停止偵測", command=StopScanning)
Setting = tk.LabelFrame(window,text='設定')
label2=tk.Label(Setting,text="報警閥值(GB)")
IsAutoStart=tk.BooleanVar(value=False)
AutoStartCheckButton=tk.Checkbutton(Setting,text='開機自啟動',command=AutoStartCheck,variable=IsAutoStart,onvalue=True,offvalue=False)
TrafficMaxValue=tk.Entry(Setting)

StopScanButton['state']=tk.DISABLED
ScanButton['state']=tk.ACTIVE
if os.path.exists(os.path.join(current_directory,'configs.txt')):
    with open(os.path.join(current_directory,'configs.txt'), 'r') as file:
        content = file.read().split()
        Ip=content[0]
        IsAutoStart.set(bool(content[1]))
        Limit=content[2]
else:
    with open(os.path.join(current_directory,'configs.txt'), 'w') as file:
        file.write("111.111.111.111"+'\n'+"False"+'\n'+"2.5")
        Ip="111.111.111.111"
        IsAutoStart.set(False)
        Limit="2.5"
YourIp.insert(0,Ip)
TrafficMaxValue.insert(0,Limit)

label.pack(pady=5)
YourIp.pack(pady=5)
ScanButton.pack(pady=5)
StopScanButton.pack(pady=5)
Log.pack(pady=5)
Setting.pack(pady=5)
AutoStartCheckButton.pack(pady=3,padx=3)
label2.pack()
TrafficMaxValue.pack(pady=3,padx=3)
window.resizable(False, False)
window.mainloop()

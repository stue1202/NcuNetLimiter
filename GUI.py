import tkinter as tk
from tkinter import messagebox
import Crwal
import webbrowser
import re
import AutoStart
import os,sys
import Iconify,Info,Notify

Scanning=False

def SaveQuit():
    UpdateConfig()
    window.destroy()
    
def SettingsValueCheck():
    if not re.match(r'\d+',TrafficMaxValue.get().strip()) :
        messagebox.showerror("錯誤","請輸入數字")
        return False
    elif not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',YourIp.get().strip()):
        messagebox.showerror("錯誤","請輸入正確IP位置格式")
        return False
    return True
    
def UpdateConfig():
    Configs=open(Info.GetConfigspath(),"w")
    Configs.write(YourIp.get().strip()+'\n'+str(IsAutoStart.get())+'\n'+str(MinimizeWhenScanning.get())+'\n'+TrafficMaxValue.get().strip())
    Configs.close()
    
def StopScanning():
    global Scanning
    Scanning=False
    Crwal.StopScanning()
    StopScanButton['state']=tk.DISABLED
    ScanButton['state']=tk.ACTIVE
    YourIp['state']=tk.NORMAL
    TrafficMaxValue['state']=tk.NORMAL
    
def StartScanning():
    global Scanning
    if SettingsValueCheck():
        Scanning=True
        if MinimizeWhenScanning.get():
            Iconify.minimize_to_tray(window,SaveQuit)
            Notify.notify("NcuNetLimiter","正在背景掃描")
        UpdateConfig()
        YourIp['state']=tk.DISABLED
        TrafficMaxValue['state']=tk.DISABLED
        StopScanButton['state']=tk.ACTIVE
        ScanButton['state']=tk.DISABLED
        Crwal.StartDetect(Log.insert,'1.0',YourIp.get(),TrafficMaxValue.get(),window.wm_state)
    else:
        Scanning=False
        window.deiconify()
        messagebox.showerror("無法啟動自動掃描","設定參數有誤")

debug=0
def IconifyCallBack(event):
    print(MinimizeWhenScanning.get() , Scanning,window.wm_state())
    global debug
    if MinimizeWhenScanning.get() and Scanning and window.state()=='iconic':
        Iconify.minimize_to_tray(window,SaveQuit)
        debug=1
def DeIconifyCallBack(event):
    global debug
    debug=0

def AutoStartCheck():
    UpdateConfig()
    if IsAutoStart.get():
        AutoStart.add_startup_item(Info.GetExeclsivepath())
    else:
        AutoStart.remove_startup_item("NcuNetLimiter.exe")

def ReadConfigs():
    try:
        with open(Info.GetConfigspath(), 'r') as file:
            content = file.read().split()
            print(content)
            Ip=content[0]
            print(IsAutoStart.get(),MinimizeWhenScanning.get())

            IsAutoStart.set(content[1])
            MinimizeWhenScanning.set(content[2])
            Limit=content[3]
            print(IsAutoStart.get(),MinimizeWhenScanning.get())
            return Ip,Limit
    except:
        with open(Info.GetConfigspath(), 'w') as file:
            file.write("111.111.111.111"+'\n'+"0"+'\n'+"0"+'\n'+"2.5")
            Ip="111.111.111.111"
            IsAutoStart.set(0)
            MinimizeWhenScanning.set(0)
            Limit="2.5"
            return Ip,Limit

window = tk.Tk()
window.title('NcuNetLimiter')
window.iconbitmap(Info.GetIconpath())
window.geometry('455x260')
menubar = tk.Menu()
#edit = tk.Menu(menubar, tearoff=0)
#menubar.add_cascade(label='Settings', menu=edit)
#edit.add_command(label='設定報警筏值', command=Settings.__init__)
#edit.add_command(label='設定開機自起動', command=None)
help_ = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=help_)
help_.add_command(label='關於此程式', command=lambda:webbrowser.open("https://github.com/stue1202/NcuNetLimiter"))
help_.add_separator()
help_.add_command(label='版本號:%s'%Info.Version)
window.config(menu=menubar)
Setting = tk.LabelFrame(window,text='設定')
label = tk.Label(Setting, text="輸入你的IP")
YourIp = tk.Entry(Setting,width=15)
Log = tk.Text(window, height=15, width=30)
ScanButton = tk.Button(window, text="開始偵測", command=StartScanning)
StopScanButton=tk.Button(window, text="停止偵測", command=StopScanning)
label2=tk.Label(Setting,text="報警閥值(GB)")
IsAutoStart=tk.IntVar()
MinimizeWhenScanning=tk.IntVar()
Ip,Limit=ReadConfigs()

AutoStartScanButton=tk.Checkbutton(Setting,text='開機自動掃描',command=AutoStartCheck,variable=IsAutoStart)
MinimizeWhenScanningButton=tk.Checkbutton(Setting,text='掃描時最小化到托盤',command=UpdateConfig,variable=MinimizeWhenScanning)
TrafficMaxValue=tk.Entry(Setting,width=15)
StopScanButton['state']=tk.DISABLED
ScanButton['state']=tk.ACTIVE


YourIp.insert(0,Ip)
TrafficMaxValue.insert(0,Limit)

Log.grid(column=0,row=0,columnspan=2, rowspan=2,padx=10,pady=10)
Setting.grid(column=2,row=0)
label.grid(column=0,row=0,pady=10,padx=5)
YourIp.grid(column=1,row=0,pady=10,padx=5)
label2.grid(column=0,row=1,pady=10,padx=5)
TrafficMaxValue.grid(column=1,row=1,pady=10,padx=5)
AutoStartScanButton.grid(column=0,row=2,pady=5,columnspan=2)
MinimizeWhenScanningButton.grid(column=0,row=4,pady=5,columnspan=2)
ScanButton.grid(column=1,row=2)
StopScanButton.grid(column=0,row=2)


if IsAutoStart.get():
    StartScanning()
window.bind("<Unmap>", IconifyCallBack)
window.bind("<Map>", DeIconifyCallBack)
#window.protocol("WM_DELETE_WINDOW", Qt)
window.resizable(False, False)
window.mainloop()

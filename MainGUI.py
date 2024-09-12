import tkinter as tk
from tkinter.ttk import * 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import schedule
import time
from selenium import webdriver
from tkinter import messagebox
import threading
from datetime import datetime

import BackGround
# 初始状态
state = "開始偵測"
Detecting=False
YourIP=''

window = tk.Tk()
window.title('UploadMonitorForNcu')
window.geometry('380x400')


text_widget = tk.Text(window, height=10, width=30)

# 菜单
menubar = tk.Menu()
edit = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Settings', menu=edit)
edit.add_command(label='設定報警筏值', command=None)
edit.add_separator()
edit.add_command(label='監測間隔', command=None)
help_ = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=help_)
help_.add_command(label='檢查新版本', command=None)
help_.add_separator()
help_.add_command(label='關於此程式', command=None)
window.config(menu=menubar)

# 标签和输入框
label = tk.Label(window, text="輸入你的IP")
label.pack()

entry = tk.Entry(window)
entry.pack()

button = tk.Button(window, text="開始偵測", command=BackGround.StartDetect(entry.text))
button.pack()

text_widget.pack()

window.resizable(False, False)
window.mainloop()

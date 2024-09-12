import tkinter as tk
from tkinter.ttk import * 
from BackGround import *
from selenium.webdriver.chrome.options import Options
import schedule
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from tkinter import messagebox
import threading

state="開始偵測"

window = tk.Tk()
window.title('UploadMonitorForNcu')
window.geometry('380x400')
text_widget = tk.Text(window, height=10, width=30)

chrome_options = Options()
chrome_options.add_argument("--headless=new")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://latias.cc.ncu.edu.tw/dormnet/index.php?section=netflow")
def RunCrawl(YourIP):
    # headless mode
    FillIp=driver.find_element(By.XPATH,"/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/form/table/tbody/tr/td/table/tbody/tr[3]/td/input[1]")
    FillIp.send_keys(YourIP)
    SendIp=driver.find_element(By.XPATH,"/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/form/table/tbody/tr/td/table/tbody/tr[3]/td/input[2]")
    SendIp.click()
    TotoalUpload=driver.find_element(By.XPATH,"/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/form/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[3]/td[2]")
    text_widget.insert(tk.END, TotoalUpload.text)
    text_widget.see(tk.END)


scheduler = schedule.Scheduler()
scheduler.every(0.1).minutes.do(RunCrawl,"140.115.205.118")
    
def run_scheduler():
    while True:
        scheduler.run_pending()
        time.sleep(1)  # Sleep briefly to prevent 100% CPU usage
thread = threading.Thread(target=run_scheduler, daemon=True)

def StartDetect():
    if thread.is_alive():
        state="停止偵測"
        thread.join()
    else:
        state="開始偵測"
        thread.start()

#menu
menubar = tk.Menu() 
# Adding Edit Menu and commands 
edit = tk.Menu(menubar, tearoff = 0) 
menubar.add_cascade(label ='Settings', menu = edit) 
edit.add_command(label ='設定報警筏值', command = None) 
edit.add_separator() 
edit.add_command(label ='監測間隔', command = None) 
# Adding Help Menu 
help_ = tk.Menu(menubar, tearoff = 0) 
menubar.add_cascade(label ='Help', menu = help_) 
help_.add_command(label ='檢查新版本', command = None) 
help_.add_separator() 
help_.add_command(label ='關於此程式', command = None) 
window.config(menu=menubar)


label = tk.Label(window, text="輸入你的IP")
label.pack()

entry = tk.Entry(window)
entry.pack()

button = tk.Button(window, text=state,command=StartDetect)
button.pack()

text_widget.pack()

window.resizable(False, False)
window.mainloop()

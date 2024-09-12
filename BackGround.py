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
import MainGUI
chrome_options = Options()
chrome_options.add_argument("--headless=new")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://latias.cc.ncu.edu.tw/dormnet/index.php?section=netflow")



def RunCrawl():
    print()
    if Detecting:
        try:
            # 等待 IP 输入框元素加载完成
            FillIp = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/form/table/tbody/tr/td/table/tbody/tr[3]/td/input[1]"))
            )
            FillIp.clear()
            FillIp.send_keys(YourIP)
            
            # 提交 IP
            SendIp = driver.find_element(By.XPATH, "/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/form/table/tbody/tr/td/table/tbody/tr[3]/td/input[2]")
            SendIp.click()

            # 获取上传总量
            TotoalUpload = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/form/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[3]/td[2]"))
            )
            text_widget = tk.Text(MainGUI.window, height=10, width=30)
            text_widget.see(tk.END)  # 自动滚动到最新内容
        except Exception as e:
            text_widget.insert(tk.END, "出錯: " + str(e) + "\n")
            text_widget.see(tk.END)

scheduler = schedule.Scheduler()
scheduler.every(0.1).minutes.do(RunCrawl)

def run_scheduler():
    while True:
        scheduler.run_pending()
        time.sleep(1)  # 避免占用过多 CPU
# 初始化线程
thread = threading.Thread(target=run_scheduler, daemon=True)

def StartDetect():
    global Detecting, thread, YourIP,state
    if not Detecting:
        # 启动线程
        Detecting=True
        YourIP=MainGUI.entry.get()
        print(MainGUI.entry.get())
        if not thread.is_alive():
            MainGUI.text_widget.insert(tk.END, "開始偵測\n")
            thread = threading.Thread(target=run_scheduler, daemon=True)
            thread.start()
        MainGUI.button.config(text="停止偵測")
    else:
        # 停止线程
        Detecting=False
        MainGUI.text_widget.insert(tk.END, "停止偵測\n")
        MainGUI.button.config(text="開始偵測")
        # 不直接停止线程，依赖 `schedule` 自然停止




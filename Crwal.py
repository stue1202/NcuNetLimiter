import threading
import schedule
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from tkinter import messagebox
import Info
import tkinter as TK
# 全局變數
YourIP = ''
stop_scanning = False
def GetLastDetectedTraffic():
    return Traffic
def GetTime():
    formatted_time = time.strftime("%H:%M:%S", time.localtime())
    return formatted_time
def GetTraffic():
    driver.get("https://latias.cc.ncu.edu.tw/dormnet/index.php?section=netflow")
    print("a")
    FillIp = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/form/table/tbody/tr/td/table/tbody/tr[3]/td/input[1]"))
    )
    FillIp.clear()
    FillIp.send_keys(YourIP)
    # 提交 IP
    SendIp = driver.find_element(By.XPATH, "/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/form/table/tbody/tr/td/table/tbody/tr[3]/td/input[2]")
    SendIp.click()
    print("b")
    # 获取上传总量
    TotoalUpload = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/form/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[3]/td[2]"))
    )
    print("c")
    #print(TotoalUpload.text)
    Traffic = re.findall(r'\d\.\d{1,2}', TotoalUpload.text)[0]
    #print(Traffic)
    return Traffic

def RunCrawl():
    global driver
    chrome_options = Options()
    chrome_options.add_argument("--headless=old")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=chrome_options)
    try:
        # 等待 IP 输入框元素加载完成
        global Traffic
        Traffic=GetTraffic()
        Ins(End, f'上傳流量共%sGB   %s\n'%(Traffic,GetTime()))
        if float(Traffic)>=float(Max):
            #if window !="normal":
            #    Notify.notify(f"超出設定上傳流量%s"%Max, f'上傳流量共%sGB   %s'%(Traffic,GetTime()))
            #else:
            messagebox.showerror(f"超出設定上傳流量%sGB"%Max, f'上傳流量共%sGB   %s'%(Traffic,GetTime()))
            Traffic=Traffic+'GB'
        driver.quit()
    except Exception as e:
        messagebox.showerror("警告", str(e))
        StopScanning()

def run_scheduler():
    scheduler = schedule.Scheduler()
    scheduler.every(10).minutes.do(RunCrawl)
    RunCrawl()
    while not stop_scanning:
        scheduler.run_pending()
        time.sleep(30)  # 避免占用过多 CPU

def StartDetect(TextBoxInsert, TextBoxEnd, MyIp, MaxTrafficValue,WindowState):
    global thread, YourIP, Ins, End, Max,stop_scanning,window,driver,Traffic
    Traffic='尚未開始偵測'
    Ins = TextBoxInsert
    End = TextBoxEnd
    Max = MaxTrafficValue
    YourIP = MyIp
    window=WindowState
    Ins(End, "開始偵測 " + YourIP + "\n")
    stop_scanning = False  # 重置停止標誌
    thread = threading.Thread(target=run_scheduler, daemon=True)
    thread.start()

def StopScanning():
    global stop_scanning
    stop_scanning = True  # 設置停止標誌
    thread.join()  # 等待線程結束
    Ins(End, "停止偵測\n")  # 顯示停止訊息

    
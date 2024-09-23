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

# 全局變數
YourIP = ''
TotoalUpload = 'init'
stop_scanning = False  # 停止標誌

chrome_options = Options()
chrome_options.add_argument("--headless=new")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://latias.cc.ncu.edu.tw/dormnet/index.php?section=netflow")

def StrModify(Origin):
    formatted_time = time.strftime("%H:%M:%S", time.localtime())
    Traffic = re.findall(r'\d\.\d{1,2}', Origin)[0]
    if float(Traffic) >= float(Max):
        messagebox.showwarning("警告", "上傳超過設定上限")
    return Traffic + ' GB ' + formatted_time + '\n'

def RunCrawl():
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
        Ins(End, StrModify(TotoalUpload.text))
    except Exception as e:
        Ins(End, str(e) + '\n')

scheduler = schedule.Scheduler()
scheduler.every(10).minutes.do(RunCrawl)

def run_scheduler():
    while not stop_scanning:
        scheduler.run_pending()
        time.sleep(1)  # 避免占用过多 CPU

def StartDetect(TextBoxInsert, TextBoxEnd, MyIp, MaxTrafficValue):
    global thread, YourIP, Ins, End, Max,stop_scanning
    Ins = TextBoxInsert
    End = TextBoxEnd
    Max = MaxTrafficValue
    YourIP = MyIp
    Ins(End, "開始偵測 " + YourIP + "\n")
    stop_scanning = False  # 重置停止標誌
    thread = threading.Thread(target=run_scheduler, daemon=True)
    thread.start()

def StopScanning():
    global stop_scanning
    stop_scanning = True  # 設置停止標誌
    thread.join()  # 等待線程結束
    Ins(End, "停止偵測\n")  # 顯示停止訊息

    
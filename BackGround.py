from selenium.webdriver.chrome.options import Options
import schedule
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

def probe(YourIP):
    # headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://latias.cc.ncu.edu.tw/dormnet/index.php?section=netflow")
    FillIp=driver.find_element(By.XPATH,"/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/form/table/tbody/tr/td/table/tbody/tr[3]/td/input[1]")
    FillIp.send_keys(YourIP)
    SendIp=driver.find_element(By.XPATH,"/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/form/table/tbody/tr/td/table/tbody/tr[3]/td/input[2]")
    SendIp.click()
    TotoalUpload=driver.find_element(By.XPATH,"/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/form/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[3]/td[2]")
    na=TotoalUpload.text


def MainProcess(Mytime,YourIP):
    schedule.every(Mytime).minutes.do(probe,YourIP)
    while True:
        schedule.run_pending()
        time.sleep(1)





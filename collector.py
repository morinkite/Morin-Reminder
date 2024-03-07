from selenium import webdriver
from selenium.webdriver.common.by import By
import time
url = 'https://www.time.ir/'

xp = '//*[@id="ctl00_cphTop_Sampa_Web_View_EventUI_EventCalendarSimple30cphTop_3732_ecEventCalendar_pnlPrevious"]'
browser = webdriver.Chrome()
browser.get(url)
for i in range(6):
    print(i)
    browser.find_element(By.XPATH,xp).click()
time.sleep(100)
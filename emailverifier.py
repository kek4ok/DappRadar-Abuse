import json
import time

from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("user-agent=")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(executable_path=r"C:\Windows\chromedriver.exe", options=options)

with open("base.json", 'r+') as f:
    data = json.load(f)
    f.close()

driver.get("https://google.com")
for i in data:
    if data[i].get("email_confirmed") == False:
        link =  data[i]["verif_link"]
        driver.get(link)
        time.sleep(5)
        print(i)
        print(link)



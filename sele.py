from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import seleFunc
import apiOuv

PATH = "C:\Program Files (x86)\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument('headless') #Not open browser
service = ChromeService(executable_path=PATH)
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://form.gov.sg/#!/60d5793adfd78e0012932b98")

def search(xpath):
    try:
        main = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,xpath))
        )
        return main
    except:
        print(f'{xpath} not found')
        driver.quit()

depot = '93FMD'
workcentre = ' Sembawang FMW'
name = ' Wong Weng Hong'
nric = '433H'

actions = ActionChains(driver)
def tab():
    time.sleep(.6)
    actions.send_keys(Keys.TAB)
    actions.perform()

def sendName(name):
    actions.send_keys(' ' + name)
    actions.perform()
    tab()

#Date
search('//*[@id="60d6a4ad3ed9d20011477b9e"]').click()
search('/html/body/section/section/div/submit-form-directive/div[1]/div/div/form/div[1]/field-directive/div/date-field-component/div/div[1]/div/div/ul/li[2]/button').click()

#Depot
search('/html/body/section/section/div/submit-form-directive/div[1]/div/div/form/div[2]/field-directive/div/dropdown-field-component/div/div[1]/div/div/div[1]/input').send_keys(depot)
tab()

#Work Centre
search('/html/body/section/section/div/submit-form-directive/div[1]/div/div/form/div[3]/field-directive/div/dropdown-field-component/div/div[1]/div/div/div[1]/input').send_keys(workcentre)
tab()

#Name
search('/html/body/section/section/div/submit-form-directive/div[1]/div/div/form/div[4]/field-directive/div/dropdown-field-component/div/div[1]/div/div/div[1]/input').send_keys(name)
tab()

#NRIC
search('//*[@id="60d57fcc71256d0011a7025c"]').send_keys(nric)

#Contacts
contacts = seleFunc.main()
if contacts:
    print(contacts)
    search('//*[@id="614c28b150247100126751b5"]').click()
    for i in contacts:
        tab()
        if 'Bryan' in i:
            i = 'Lum Chao Hui, Bryan'
        sendName(i)

#Declare
search('/html/body/section/section/div/submit-form-directive/div[1]/div/div/form/div[20]/field-directive/div/radio-button-field-component/div/div[1]/div/div/div/label/span[2]').click()

#Submit
search('/html/body/section/section/div/submit-form-directive/div[1]/div/div/div/div/button').click()

print('DONE AMB!')
time.sleep(2)
driver.quit()

apiOuv.main()
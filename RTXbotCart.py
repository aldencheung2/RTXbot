#automatically check out item in cart when it restocks

#update account details
accountEmail = "___@gmail.com"
accountPassword = "password"
cvv = "000"

#update webdriver path
driverPath = "C:/WebDriver/bin/MicrosoftWebDriver.exe"

from selenium import webdriver
from selenium.webdriver import Edge
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
import time
import win10toast

#create an object for the notification
from win10toast import ToastNotifier
notification = ToastNotifier()

driver2 = webdriver.Edge(executable_path=driverPath)

##########################################
executor_url = driver2.command_executor._url
session_id = driver2.session_id
driver2.get("https://www.bestbuy.ca")

element = WebDriverWait(driver2,1000).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,"Account")))

driver2.find_elements_by_partial_link_text("Account")[0].click()

element = WebDriverWait(driver2,1000).until(EC.presence_of_element_located((By.NAME,"username")))

elem = driver2.find_element_by_name("username")
print("Found Username")
elem.clear()
elem.send_keys(accountEmail)
elem = driver2.find_element_by_name("password")
elem.send_keys(accountPassword)
elem.send_keys(Keys.RETURN)
print("Autofilled")

#waits for user to clear captcha
while True:
    userInput = input("Type 'ok' to continue: ")
    if userInput == "ok":
        break


print(session_id)
print(executor_url)

##########################


driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
driver.session_id = session_id
print(driver.current_url)

while True:
    try:
        driver.get("https://www.bestbuy.ca/en-ca/basket")
        WebDriverWait(driver,60).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,"NVIDIA GeForce RTX 3060 Ti 8GB GDDR6 Video Card")))
        driver.find_element_by_css_selector('[class="globalMessageContainer_1ib8T"]')
    except NoSuchElementException:
        break
    except Exception as e:
        notification.show_toast("Error1!", "RTXbotCart.py")
        notification.show_toast("Error1!", str(e))

try:
    element = WebDriverWait(driver,1000).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,"Continue to Checkout")))

    #driver.find_element_by_css_selector('[class="button_2Xgu4 primary_oeAKs continueToCheckout_9H2aB regular_cDhX6"]').click()
    driver.find_elements_by_partial_link_text("Continue to Checkout")[0].click()

    notification.show_toast("RTX 3060 Ti IN STOCK","CHECKING OUT", threaded=True)

    element = WebDriverWait(driver,1000).until(EC.presence_of_element_located((By.NAME,"cvv")))

    elem = driver.find_element_by_name("cvv")
    elem.clear()
    elem.send_keys(cvv)
    elem.send_keys(Keys.RETURN)

    notification.show_toast("RTX 3060 Ti PURCHASED","")

    #driver.close()
except Exception as e:
    notification.show_toast("Error2!", "RTXbotCart.py")
    notification.show_toast("Error2!", str(e))
#automatically checks out item from product page when in stock
#update cvv
cvv="000"
#update Edge webdriver path
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

start = time.time()
while (time.time()-start)<120:
    print(time.time()-start)
    time.sleep(5)

print(session_id)
print(executor_url)


driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
driver.session_id = session_id
print(driver.current_url)

#######################

driver.get("https://www.bestbuy.ca/en-ca/product/nvidia-geforce-rtx-3060-ti-8gb-gddr6-video-card/15166285")

while True:
    try:
        form = driver.find_element_by_css_selector('[class="button_2Xgu4 primary_oeAKs addToCartButton_1DQ8z addToCartButton regular_cDhX6"]')
        break
    except NoSuchElementException:
        continue


#works:
driver.find_element_by_css_selector('[class="button_2Xgu4 primary_oeAKs addToCartButton_1DQ8z addToCartButton regular_cDhX6"]').click()


# wait = WebDriverWait(driver, 20)
# element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'basketIcon_30LAG')))
# print("found")

# driver.find_element_by_class_name('basketIcon_30LAG').click()

element = WebDriverWait(driver,1000).until(EC.presence_of_element_located((By.CSS_SELECTOR,"[class='button_2Xgu4 primary_oeAKs goToCartButton_2hUsP regular_cDhX6']")))



print("found")

#driver.find_element_by_class_name('basketIcon_30LAG').click()
driver.get("https://www.bestbuy.ca/en-ca/basket")

element = WebDriverWait(driver,1000).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,"Continue to Checkout")))

#driver.find_element_by_css_selector('[class="button_2Xgu4 primary_oeAKs continueToCheckout_9H2aB regular_cDhX6"]').click()
driver.find_elements_by_partial_link_text("Continue to Checkout")[0].click()

element = WebDriverWait(driver,1000).until(EC.presence_of_element_located((By.NAME,"cvv")))

elem = driver.find_element_by_name("cvv")
elem.clear()
elem.send_keys(cvv)
elem.send_keys(Keys.RETURN)

notification.show_toast("RTX 3060 Ti PURCHASED","")

#driver.close()
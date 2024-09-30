from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = 'http://127.0.0.1:5500/'
USERNAME = 'test@kea.dk'
PASSWORD = 'Test'

driver = webdriver.Firefox()
driver.get(BASE_URL)

#
# Sign up
#
driver.find_element(By.CSS_SELECTOR, '#optSignup > a').click()
driver.find_element('id', 'txtEmail').send_keys(USERNAME)
driver.find_element('id', 'txtPassword').send_keys(PASSWORD)
driver.find_element('id', 'txtRepeatPassword').send_keys(PASSWORD)
driver.find_element(By.CSS_SELECTOR, '#frmSignup input[type="submit"]').click()

#
# Log in
#
driver.find_element(By.CSS_SELECTOR, 'a[href="login.html"]').click()
driver.find_element('id', 'txtEmail').send_keys(USERNAME)
driver.find_element('id', 'txtPassword').send_keys(PASSWORD)
driver.find_element(By.CSS_SELECTOR, '#frmLogin input[type="submit"]').click()

#
# Add products to the cart
#
PRODUCT_T_SHIRT = 'Mens Casual Premium Slim Fit T-Shirts'
XPATH_T_SHIRT = f"//article[header/h2[text()='{PRODUCT_T_SHIRT}']]"

# Explicit wait so that the webshop's API has time enough to send its response
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.XPATH, XPATH_T_SHIRT)))

article = driver.find_element(By.XPATH, XPATH_T_SHIRT)
article.find_element(By.XPATH, './/button').click()

PRODUCT_SSD = 'SanDisk SSD PLUS 1TB Internal SSD - SATA III 6 Gb/s'
XPATH_SSD = f"//article[header/h2[text()='{PRODUCT_SSD}']]"

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.XPATH, XPATH_SSD)))

article = driver.find_element(By.XPATH, XPATH_SSD)
# Executing a clear() and then assigning the value 2 to the number input
# did not work, as Selenium ignored the clear() and wrote 12 in the field.
# It is necessary to execute JavaScript code to get the value properly updated
numberInput = article.find_element(By.XPATH, './/input[@type="number"]')
driver.execute_script('arguments[0].value = "2";', numberInput)
article.find_element(By.XPATH, './/button').click()

#
# Changing product quantity in the cart
#
driver.find_element(By.CSS_SELECTOR, '#optCart > a').click()

numberInput = driver.find_element(By.XPATH, f'//td[text()="{PRODUCT_SSD}"]/following-sibling::td[contains(@class, "amountCell")]//input[@type="number"]')
driver.execute_script('arguments[0].value = "3";', numberInput)

driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

#
# Check out
#
ADDRESS = 'Guldbergsgade 29N'
POSTAL_CODE = '2200'
CITY = 'Copenhagen'
CUSTOMER_NAME = 'Pernille L. Hansen'
CARD_EXPIRATION = '2027-12'
CVV = '666'

driver.find_element('id', 'txtDeliveryAddress').send_keys(ADDRESS)
driver.find_element('id', 'txtDeliveryPostalCode').send_keys(POSTAL_CODE)
driver.find_element('id', 'txtDeliveryCity').send_keys(CITY)

driver.find_element('id', 'chkRepeat').click()

driver.find_element('id', 'txtCreditCardName').send_keys(CUSTOMER_NAME)
driver.find_element('id', 'txtExpiryDate').send_keys(CARD_EXPIRATION)
driver.find_element('id', 'txtCVV').send_keys(CVV)

driver.find_element(By.CSS_SELECTOR, '#checkout input[type="submit"]').click()

#
# Check that the cart is empty
#
driver.find_element(By.CSS_SELECTOR, '#optCart > a').click()

XPATH_EMPTY_CART = '//dialog[@id="alert"]//p'
alert_paragraph = driver.find_element(By.XPATH, XPATH_EMPTY_CART)
assert 'empty' in alert_paragraph.text

driver.find_element(By.CSS_SELECTOR, '#alert a[title="Close Alert"]').click()

#
# Log out
#
driver.find_element(By.CSS_SELECTOR, '#optLogout > a[title="Log out"]').click()

login_link = driver.find_element(By.CSS_SELECTOR, 'a[href="login.html"]')
assert login_link, 'Log out unsuccessful'

#
# Close browser
#
driver.quit()
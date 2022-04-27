from dotenv import dotenv_values
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.webelement import FirefoxWebElement
from selenium.webdriver.support import expected_conditions as EC

'''
KONFIG TARO DI SIINI AJA
'''
config = dotenv_values('.env')

ceisa_prm_url = 'http://prm.customs.go.id/Prm/'
username = config['USERNAME'] 
password = config['PASSWORD']
prm_key = config['PRM_KEY']
geckodriver = config['GECKODRIVER']

print(f'config: username={username}, password={password}, prm_key={prm_key}, geckodriver={geckodriver}')

# generate browser instance
options = FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options, executable_path=f"./{geckodriver}")

# enter url
print("Loading target url...")

try:
    driver.get('http://prm.customs.go.id/Prm/')
except WebDriverException as e:
    # welp, we failed to load url
    print(f'Failed to load: {ceisa_prm_url}, reason: {e.msg}')
    driver.quit()
    exit()

# where are we redirected to?
current_url = driver.current_url
must_login = False
print(f'Current url: {current_url}')
if current_url.startswith('http://ceisa.customs.go.id'):
    # we gotta login
    must_login = True

# verdict?
print("Login status: " + ("Already Logged in", "MUST LOGIN!")[must_login])

# grab input
el_username = driver.find_element_by_id('txtUserName')
el_password = driver.find_element_by_id('txtUserPassword')
btn_submit = driver.find_element_by_id('btnSubmit')

# send data
print("Entering login info...")
el_username.send_keys(username)
el_password.send_keys(password)

# click login?
btn_submit.click()
print("Submit login...")

# wait until some condition is met
WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.ID, 'txtKey'))
)
el_prm_key = driver.find_element_by_id('txtKey')

# what are we redirected to now?
current_url = driver.current_url
print(f'Current url: {current_url}')
if current_url.startswith('http://prm.customs.go.id'):
    # hmm? good?
    print('Now we need to enter PRM_KEY')
    if el_prm_key:
        el_fake_key = driver.find_element_by_id('fakeKey')
        el_fake_key.send_keys(prm_key)
        btn_login = driver.find_element_by_id('btnLogin')
        btn_login.click()
        print("PRM_KEY submitted....")

# gotta find something?
try:
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text()='Invalid')]"))
    )
    print("PRM KEY INVALID!")
except TimeoutException:
    print("PRM KEY ACCEPTED!")

# wait until page loaded, and grab the cookie
print("Waiting until login screen goes away...")
WebDriverWait(driver, 30).until_not(
    EC.presence_of_element_located((By.ID, 'btnLogin'))
)

# grab cookies
cookies = driver.get_cookies()
print(f'Cookies')
print(cookies)

# quit
driver.quit()

# filter data
cookie_strings = list(map(lambda x: x['name']+'='+x['value'], cookies))
cookie_strings = '; '.join(cookie_strings)
print('Cookie strings')
print(cookie_strings)

# write output
f = open("./cookies.txt","w")
f.write(cookie_strings)
f.close()


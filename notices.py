from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from colorama import Fore, init
import re
import os


def clean_html(raw_html):
    clean_r = re.compile('<.*?>')
    clean_text = re.sub(clean_r, '', raw_html)
    return clean_text

# comment 'init()', if running this script on Terminal or Pycharm or Windows Powershell.
# uncomment the following line, if running this script on Windows Command Prompt for the display of colors.
init()

course_urls = []
for_getting_course_ids = "http://id.bits-hyderabad.ac.in/moodle/my/index.php?mynumber=-2"

bits_username = os.environ['BITS_USERNAME']
bits_password = os.environ['BITS_PASSWORD']

driver = webdriver.PhantomJS('./phantomjs-2.1.1-windows/bin/phantomjs', service_args=['--load-images=no'])

driver.get('http://id.bits-hyderabad.ac.in/moodle/login/index.php')
driver.find_element_by_id("username").clear()
driver.find_element_by_id("username").send_keys(bits_username)
driver.find_element_by_id("password").clear()
driver.find_element_by_id("password").send_keys(bits_password)
driver.find_element_by_id("password").send_keys(Keys.ENTER)
print(Fore.MAGENTA + driver.title)

driver.get(for_getting_course_ids)
course_list = driver.find_element_by_class_name('course_list').find_elements_by_css_selector('a')
for x in course_list:
    course_urls.append(x.get_attribute('href'))

for x in course_urls:
    driver.get(x)
    course_name = driver.find_element_by_class_name('page-subtitle').get_attribute('innerHTML')
    print(Fore.LIGHTBLUE_EX + course_name)
    notices = driver.find_elements_by_class_name('mod-indent-outer')
    for y in notices:
        try:
            notice_title = y.find_element_by_class_name('instancename')
            myString = notice_title.get_attribute('innerHTML')
            try:
                num = myString.index('<')
                print(Fore.GREEN + myString[:num])
            except ValueError:
                print(Fore.GREEN + myString)
        except Exception:
            pass

        try:
            notice_body = y.find_elements_by_css_selector('p')
            for w in notice_body:
                print(Fore.CYAN + clean_html(w.get_attribute('innerHTML')))
        except Exception:
            pass

    print("\n")

driver.get("http://id.bits-hyderabad.ac.in/moodle/login/logout.php")
logout_elem = driver.find_element_by_tag_name('input')
logout_elem.click()
print(Fore.RESET + driver.title)
driver.quit()

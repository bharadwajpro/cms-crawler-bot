from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from colorama import Fore, init
import re
import os
import sqlite3
import json
import urllib3
import datetime
import sys

post_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='
fb_access_token = os.environ['CMS_FB_ACCESS_TOKEN']
http = urllib3.PoolManager()
urllib3.disable_warnings()
post_url += fb_access_token
full_data = '''
{
    "recipient": {
        "id": "1217316241672056"
    },
    "message": {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [{
                    "title": "",
                    "subtitle": ""
                }]
            }
        }
    }
}
'''


def send_to_bot(a, b):
    global full_data
    data = json.loads(full_data)
    data['message']['attachment']['payload']['elements'][0]['title'] = a
    data['message']['attachment']['payload']['elements'][0]['subtitle'] = b
    data = json.dumps(data)
    r = http.request('POST', post_url, headers={'Content-Type': 'application/json'}, body=data)
    print(r)


def clean_html(raw_html):
    clean_r = re.compile('<.*?>')
    clean_text = re.sub(clean_r, '', raw_html)
    return clean_text

conn = sqlite3.connect('cms.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS cms_notices (notice_title, notice_subtitle)
''')

# c.execute('SELECT * FROM cms_notices')
# print(c.fetchall())
# exit()

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

driver.get(for_getting_course_ids)
course_list = driver.find_element_by_class_name('course_list').find_elements_by_css_selector('a')
for x in course_list:
    course_urls.append(x.get_attribute('href'))

for x in course_urls:
    driver.get(x)
    course_name = driver.find_element_by_class_name('page-subtitle').get_attribute('innerHTML')
    notices = driver.find_elements_by_class_name('mod-indent-outer')
    for y in notices:
        notice_title = ''
        notice_subtitle = ''
        try:
            notice_title = y.find_element_by_class_name('instancename')
            notice_title = course_name + " | " + notice_title.get_attribute('innerHTML')
            try:
                num = notice_title.index('<')
                notice_title = notice_title[:num]
            except ValueError:
                pass
        except Exception:
            pass

        try:
            notice_body = y.find_elements_by_css_selector('p')
            for w in notice_body:
                notice_subtitle += clean_html(w.get_attribute('innerHTML'))
        except Exception:
            pass

        notice_subtitle = " ".join(notice_subtitle.split())
        notice_subtitle.strip()
        if notice_title == '':
            notice_title = 'Notice'
        if notice_subtitle == '':
            notice_subtitle = 'Body'
        c.execute("SELECT * FROM cms_notices WHERE notice_title=? AND notice_subtitle=?", (notice_title, notice_subtitle))
        no_rows = len(c.fetchall())
        if no_rows == 0:
            c.execute("INSERT INTO cms_notices VALUES (?, ?)", (notice_title, notice_subtitle))
            conn.commit()
            send_to_bot(notice_title, notice_subtitle)

driver.get("http://id.bits-hyderabad.ac.in/moodle/login/logout.php")
logout_elem = driver.find_element_by_tag_name('input')
logout_elem.click()
print(Fore.RESET + driver.title)
print("Done")
driver.quit()

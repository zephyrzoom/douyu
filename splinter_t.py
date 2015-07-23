__author__ = 'zeek'
import time
import notify2
from splinter import Browser
import html

browser = Browser()
browser.visit('http://www.douyutv.com/zeek')
last_list = 0
last_yuwan = 0
while True:
    if last_list % 20 == 10:
        browser.reload()

    time.sleep(2)

    try:
        element_list_chat = browser.find_by_xpath('//span[@class="text_cont"]')
        element_list_uid = browser.find_by_xpath('//a[@class="nick js_nick"]')
        element_list_yuwan = browser.find_by_xpath('//p[@class="text_cont"]/i')
    except Exception as err:
        print(err)
        continue
    if element_list_uid and last_list != len(element_list_uid):
        if last_yuwan != len(element_list_yuwan):
            element_list_chat.append('送了' + element_list_yuwan[-1].html + '鱼丸')
            last_yuwan += 1
        else:
            for i in range(last_yuwan):
                element_list_chat.insert(0, 0)

        print(element_list_chat[last_list].html)
        notify2.init("douyu")
        header = html.unescape(element_list_uid[last_list].html)
        content = html.unescape(element_list_chat[last_list].html)
        n = notify2.Notification(header, content)
        n.show()
        last_list += 1
    else:
        print('empty')

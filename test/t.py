__author__ = 'zeek'
import urllib.request
with urllib.request.urlopen('http://www.douyutv.com/member/cp/get_user_history') as f:
    print(f.read().decode('utf-8'))

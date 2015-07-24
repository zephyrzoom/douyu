
__author__ = 'zeek'

import os

def notify(title, message):
    t = '-title {!r}'.format(title)
    m = '-message {!r}'.format(message)
    os.system('terminal-notifier {}'.format(' '.join([m, t])))

notify(title='a', message='b' + str(100))

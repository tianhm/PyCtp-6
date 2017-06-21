import sys
import subprocess
import time

account = 'real_xh1'
# account = 'real_eb1'

mongodb = 'mongodb1'
# mongodb = 'mongodbi'

subprocess.Popen([sys.executable,'live_quote.py','-m','t','-a',account,'-d',mongodb], creationflags=subprocess.CREATE_NEW_CONSOLE)

time.sleep(10)

subprocess.Popen([sys.executable,'live_quote.py','-m','q','-p','futures','-e','cffex','-a',account,'-d',mongodb], creationflags=subprocess.CREATE_NEW_CONSOLE)
subprocess.Popen([sys.executable,'live_quote.py','-m','q','-p','futures','-e','shfe','-a',account,'-d',mongodb], creationflags=subprocess.CREATE_NEW_CONSOLE)
subprocess.Popen([sys.executable,'live_quote.py','-m','q','-p','futures','-e','dce','-a',account,'-d',mongodb], creationflags=subprocess.CREATE_NEW_CONSOLE)
subprocess.Popen([sys.executable,'live_quote.py','-m','q','-p','futures','-e','czce','-a',account,'-d',mongodb], creationflags=subprocess.CREATE_NEW_CONSOLE)

subprocess.Popen([sys.executable,'live_quote.py','-m','q','-p','options','-e','dce','-a',account,'-d',mongodb], creationflags=subprocess.CREATE_NEW_CONSOLE)


# cd 'Z:\williamyizhu On My Mac\Documents\workspace\PyCtp'
# python .\live_quote.py -m t -a real_eb1 -d mongodb1
# python .\live_quote.py -m t -a real_xh1 -d mongodb1
# python .\live_quote.py -m t -a real_ht1 -d mongodb1
# python .\live_quote.py -m q -p futures -e dce -a real_xh1 -d mongodb1
# python .\live_quote.py -m q -p options -e dce -a real_eb2 -d mongodb1

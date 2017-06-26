import sys
import subprocess
import time

# account = 'real_xh1'
account = 'real_eb1'

mongodb = 'ctp_mongodb2'
# mongodb = 'ctp_mongodb2i'

subprocess.Popen([sys.executable,'live_quote.py','-m','t','-a',account,'-d',mongodb], creationflags=subprocess.CREATE_NEW_CONSOLE)

time.sleep(10)

subprocess.Popen([sys.executable,'live_quote.py','-m','q','-p','futures','-e','cffex','-a',account,'-d',mongodb], creationflags=subprocess.CREATE_NEW_CONSOLE)
subprocess.Popen([sys.executable,'live_quote.py','-m','q','-p','futures','-e','shfe','-a',account,'-d',mongodb], creationflags=subprocess.CREATE_NEW_CONSOLE)
subprocess.Popen([sys.executable,'live_quote.py','-m','q','-p','futures','-e','dce','-a',account,'-d',mongodb], creationflags=subprocess.CREATE_NEW_CONSOLE)
subprocess.Popen([sys.executable,'live_quote.py','-m','q','-p','futures','-e','czce','-a',account,'-d',mongodb], creationflags=subprocess.CREATE_NEW_CONSOLE)

subprocess.Popen([sys.executable,'live_quote.py','-m','q','-p','options','-e','dce','-a',account,'-d',mongodb], creationflags=subprocess.CREATE_NEW_CONSOLE)
subprocess.Popen([sys.executable,'live_quote.py','-m','q','-p','options','-e','czce','-a',account,'-d',mongodb], creationflags=subprocess.CREATE_NEW_CONSOLE)


# cd 'Z:\williamyizhu On My Mac\Documents\workspace\PyCtp'
# python .\live_quote.py -m t -a real_eb1 -d ctp_mongodb2
# python .\live_quote.py -m t -a real_xh1 -d ctp_mongodb2
# python .\live_quote.py -m t -a real_ht1 -d ctp_mongodb2
# python .\live_quote.py -m q -p futures -e dce -a real_eb2 -d ctp_mongodb2
# python .\live_quote.py -m q -p options -e dce -a real_eb2 -d ctp_mongodb2

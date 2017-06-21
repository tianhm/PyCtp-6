import sys
import subprocess
import time

# mongodb = 'mongodb1'
mongodb = 'mongodbi'

subprocess.Popen([sys.executable,'live_quote.py','-m','t','-a','real_eb1','-d',mongodb], creationflags=subprocess.CREATE_NEW_CONSOLE)

time.sleep(10)

subprocess.Popen([sys.executable,'live_quote.py','-m','q','-p','futures','-e','cffex','-a','real_eb1','-d',mongodb], creationflags=subprocess.CREATE_NEW_CONSOLE)
subprocess.Popen([sys.executable,'live_quote.py','-m','q','-p','futures','-e','shfe','-a','real_eb1','-d',mongodb], creationflags=subprocess.CREATE_NEW_CONSOLE)
subprocess.Popen([sys.executable,'live_quote.py','-m','q','-p','futures','-e','dce','-a','real_eb1','-d',mongodb], creationflags=subprocess.CREATE_NEW_CONSOLE)
subprocess.Popen([sys.executable,'live_quote.py','-m','q','-p','futures','-e','czce','-a','real_eb1','-d',mongodb], creationflags=subprocess.CREATE_NEW_CONSOLE)

subprocess.Popen([sys.executable,'live_quote.py','-m','q','-p','options','-e','dce','-a','real_eb1','-d',mongodb], creationflags=subprocess.CREATE_NEW_CONSOLE)


# cd 'Z:\williamyizhu On My Mac\Documents\workspace\PyCtp'
# python .\live_quote.py -m t -a real_eb2 -d mongodb1
# python .\live_quote.py -m t -a real_xh -d mongodb1
# python .\live_quote.py -m t -a real_ht -d mongodb1
# python .\live_quote.py -m q -p futures -e dce -a real_eb2 -d mongodb1
# python .\live_quote.py -m q -p options -e dce -a real_eb2 -d mongodb1

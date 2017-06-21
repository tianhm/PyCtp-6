import os
import sys
workspace = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
xx = os.path.join(workspace, 'hf_py_ctp')
print(xx)

# print(os.getcwd())



sys.path.append(xx)

# from ctp_struct import *
from py_ctp.trade import Trade
from py_ctp.quote import Quote

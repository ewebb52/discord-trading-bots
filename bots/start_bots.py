import os 
from ssb import *
from rcb import *
from robin import *
from eth_bot import *
from ltc_bot import *

def parent_child(): 
    n = os.fork() 
    # n greater than 0  means parent process 
    if n > 0: 
        print("N. Parent process and id is : ", os.getpid()) 
        n2 = os.fork()
        if n2 > 0:
            #Running Read and Call
            print("run_rcb. Parent process and id is : ", os.getpid()) 
            run_rcb()
        else:
            #running Robinhood
            print("run_robinhood. Parent process and id is : ", os.getpid()) 
            run_robinhood()
        print("Processes Cancelled.")
    # n equals to 0 means child process 
    else: 
        n2 = os.fork()
        if n2 > 0:
            print("run_eth. Child process and id is : ", os.getpid()) 
            run_eth()
        else:
            n3 = os.fork()
            if n3 > 0:
                print("run_ltc. Child process and id is : ", os.getpid())
                run_ltc()
            else:
                print("run_ssb. Child process and id is : ", os.getpid())
                run_ssb()

# Driver code 
parent_child() 
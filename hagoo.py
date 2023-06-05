import subprocess
from multiprocessing import Process
import threading
import time
from sys import exit


def lonc():
    subprocess.run(["bash","-c","nohup python testowa/tester.py >/dev/null &"])


    
t1 = Process(target=lonc, args=())
t1.start()
    
    

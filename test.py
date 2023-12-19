from multiprocessing import Process, Manager, Queue, Lock
from time import sleep

def sleeper():
    sleep(10000)
    

yawn = Process(name='Sleeper',
                              target=sleep,
                              args=(),
                              daemon=True)
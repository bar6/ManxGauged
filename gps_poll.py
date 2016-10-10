import os 
from gps import *
from time import *
import time 
import threading 

class GpsPoller(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.session = gps(mode=WATCH_ENABLE)
        self.current_value = None 
        self.running = True 
        
    def get_current_value(self):
            return self.current_value
        
    def run(self):
        try:
            while self.running:
                self.current_value = self.session.next() 
        except StopIteration:
            pass 

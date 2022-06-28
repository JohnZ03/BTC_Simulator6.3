from utils import *
from event import Event
import random
import numpy as np
from heapq import *
import scipy


class Simulator:
    def __init__(self, network, initial_time=0, duration=3600000):
        self.initial_time = initial_time
        self.end_time = self.initial_time + duration
        self.network = network

        self.events_scheduler = []
        self.events_dic = {}
        self.count = 0

        self.now = initial_time
        self.data = {"blocks":{}}
        



    def _add_event(self, event, priority=0):
        self.count = self.count + 1
        # print(priority)
        entry = [priority, self.count, event]
        self.events_dic[event] = entry
        heappush(self.events_scheduler, entry)


    def _pop_event(self):
        while self.events_scheduler:
            priority, count, event = heappop(self.events_scheduler)
            del self.events_dic[event]
            return event
        raise KeyError('pop from an empty priority queue')

    def schedule_block_mining_event(self,node):
        delay = node.get_block_generation_time()
        time = delay + self.now #in ms
        event = Event("BM", node, time, msg=None)
        self._add_event(event,priority=time)

    def initiate_events(self):
        for nid, node in self.network.miners.items():
            self.schedule_block_mining_event(node)

    def schedule_block_propogation_event(self, sender, receiver, msg):
        delay = get_BP_delay(self.network, msg.size, sender.region, receiver.region)
        time = delay + self.now #in ms
        event = Event("BP", receiver, time, msg)
        self._add_event(event,priority=time)


    def process_event(self, event):
        node = event.node
        if event.type == "BM":
            node.build_new_block(self)
            self.schedule_block_mining_event(node)      
        elif event.type == "BP":
            node.receive_block(self, event.msg)

    def run(self):
        print(f'Simulation Starts at {self.now}')
        self.initiate_events()  
        while self.events_scheduler:
            event = self._pop_event()
            if event.time > self.end_time:
                break
            else:
                self.now = event.time
            self.process_event(event)
        
        print(f'Simulation Ends at {self.now}')
        
    def end(self):
        self.initial_time = 0
        self.end_time = 0
        self.network = 0

        self.events_scheduler = []
        self.events_dic = {}
        self.count = 0

        self.now = 0
        self.data = {"blocks":{}}




    
# atomicModel.py
import env

class State(object):
    def __init__(self):
        self.active = "active"
        self.passive = "passive"
        return
        
class Port(object):
    def __init__(self,name):
        self.name = name
        self.bag = []
        self.size = 0
    def append(self,item):
        self.bag.append(item)
        self.size += 1
    def pop(self):
        if len(self.bag) > 0:
            self.size -= 1
            return self.bag.pop()
        return None
    def contents(self):
        return self.bag


class AtomicModel(object):
    def __init__(self,name):
        self.name = name
        self.STATES = State()
        self.state = self.STATES.passive
        self.events = []
        self.next_event = (self.STATES.passive,-1)
        self.event_int = False
        self.event_ext = False
        self.in_ports = []
        self.out_ports = []
        return
    
    def add_in_port(self,name):
        self.in_ports.append(Port(name))
    
    def add_out_port(self,name):
        self.out_ports.append(Port(name))
        
    def get_in_port(self,name):
        for port in self.in_ports:
            if name == port.name:
                return port
        raise IndexError
        
    def append_out_port(self,name,item):
        for i, port in enumerate(self.out_ports):
            if name == port.name:
                self.out_ports[i].append(item)
                return
        raise IndexError
        
    def append_in_port(self,name,item):
        for i, port in enumerate(self.in_ports):
            if name == port.name:
                self.out_ports[i].append(item)
                return
        raise IndexError
    
    def delta_int(self):
        return
    
    def delta_ext(self):
        return
        
    def delta_con(self):
        self.delta_int()
        self.delta_ext()
        return
    
    def _lambda(self):
        return
        
    def hold_in(self,phase,delta):
        self.events.append((phase,env.n_step + delta))
        return
        
    def passivate(self):
        self.set_state(self.STATES.passive)
        return
        
    def set_state(self,state):
        self.state = state
        self.event_int = True
        return
        
    def check_for_event(self):
        if env.n_step == self.next_event[1]:
            self.set_state(self.next_event[0])
            self.next_event = self.events.pop(0)
            return True
        return False
    
    def check_for_ext(self):
        if len(self.in_ports) == 0:
            return False
        else:
            for port in self.in_ports:
                if len(port.bag) > 0:
                    self.event_ext = True
                    return True
        return False
        
    def event(self):
        if self.event_int and self.event_ext:
            self.event_int = False
            self.event_ext = False
            self.delta_con()
        elif self.event_int:
            self.event_int = False
            self.delta_int()
        elif self.event_ext:
            self.event_ext = False
            self.delta_ext()

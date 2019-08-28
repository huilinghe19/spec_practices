import os
import time
from sardana import State
from sardana.pool.controller import CounterTimerController, Type,\
    Description, DefaultValue
import SpecMotor
import SpecCommand 

def read_network_counts(interface):
    cmd = 'cat /proc/net/dev | grep {0}'.format(interface)
    with os.popen(cmd) as fd:
        output = fd.read()
        bytes_raw = output.split()[1]
        return int(bytes_raw)
    
def read_keithley():
    #m = SpecMotor.SpecMotor('copley', 'localhost:spec')
    #print m.getPosition()
    
    cmd = SpecCommand.SpecCommand('', 'localhost:spec')
    #cmd.executeCommand("mv copley -2000")
    #print m.getPosition()
    a = cmd.executeCommand("gpib_put(16, '*idn/?')")
    b = cmd.executeCommand("gpib_put(16, 'READ?')")
    c = cmd.executeCommand("gpib_get(16)")
    print a
    print b
    print c
    return c

class KeithleyController(CounterTimerController):
    """This controller provides interface for network packages counting.
    It counts the number of bytes of data transmitted or received by a network
    interface over the integration time.
   

    ctrl_properties = \
        {'interface': {Type : str,
                       Description : 'network interface to count packages',
                       DefaultValue : 'eno1'},
        }
    """
    
    ctrl_properties = \
        {'spec': {Type : str,
                       Description : 'spec host',
                       DefaultValue : 'localhost'},
        }
    def __init__(self, inst, props, *args, **kwargs):
        CounterTimerController.__init__(self,inst,props, *args, **kwargs)
        self.acq_time = 1.
        self.acq_end_time = time.time()
        self.start_counts = 0

    def LoadOne(self, axis, value):
        self.acq_time = value

    def StateOne(self, axis):
        state = State.On
        if time.time() < self.acq_end_time:
            state = State.Moving
        # due to sardana-org/sardana #621 we need to return also status
        status_string = 'My custom status info'
        return state, status_string

    def StartOne(self, axis, _):
        self.acq_end_time = time.time() + self.acq_time
        #self.start_counts = read_network_counts(self.interface)
        self.start_counts = read_keithley()
    # due to sardana-org/sardana #622 we need to implement StartAll
    def StartAll(self):
        pass

    def ReadOne(self, axis):
        #counts = read_network_counts(self.interface)
        value = read_keithley()
        #return counts - self.start_counts
        return value

    def AbortOne(self, axis):
        self.acq_end_time = time.time()
       


keithleyValue= read_keithley()
print keithleyValue
controller = KeithleyController({"a":"b"},{"c":"dxY"})
state = controller.StateOne(1)
value = controller.ReadOne(1)
print state
print value

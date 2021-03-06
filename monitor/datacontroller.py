
# -*- coding: utf-8 -*-
import time
import numpy as np
from .databackend import DataBackend, DataBackendHandler

class TimeDataInputManager:
    def __init__(self, arraysize, data_range):
        self.ymin,self.ymax=data_range
        self.arraysize=arraysize
        self.data=np.arange(self.ymin,self.ymax, (self.ymax-self.ymin)/self.arraysize)
    def get_range(self):
        return (self.ymin,self.ymax)

class DataInputs:

    class Handler(DataBackendHandler):
        def __init__(self, parent):
            self.parent=parent

        def update_inputs(self, **kwargs):
            if kwargs is not None:
                for key, value in kwargs.items():
                    if(key in self.parent.inputs):
                        oldval=self.parent.inputs[key]
                        if oldval != value:
                            self.parent.changed=True
                            self.parent.inputs[key]=value
    
        def update_timedata(self,timestamp, pressure, flow, volume):
            if not self.parent.freeze:
                self.parent.make_index(timestamp)
                self.parent.pressure.data[self.parent.index]=pressure
                self.parent.flow.data[self.parent.index]=flow
                self.parent.volume.data[self.parent.index]=volume
    
    def __init__(self, xmax, freq):
        self.running=True
        
        self.inputs = {}
        self.inputs[DataBackend.FIO2]=0
        self.inputs[DataBackend.PEP]=0
        self.inputs[DataBackend.PEP_ALARM]=False
        self.inputs[DataBackend.FR]=0
        self.inputs[DataBackend.PPLAT]=0
        self.inputs[DataBackend.VM]=0
        self.inputs[DataBackend.PCRETE]=0
        self.inputs[DataBackend.PCRETE_ALARM]=False
        self.inputs[DataBackend.VTE]=0
        self.inputs[DataBackend.VTE_ALARM]=False

        self.changed=False
        self.handler = DataInputs.Handler(self)
        
        self.index=0
        self.index_zero_time = 0
        self.freeze=False
        self.unfreeze=False
        self.xmax=xmax
        self.freq=freq
        self.arraysize=xmax*freq

        self.pressure=TimeDataInputManager(self.arraysize, (-30,105))
        self.flow=TimeDataInputManager(self.arraysize, (-100,100))
        self.volume=TimeDataInputManager(self.arraysize, (0,500))

    
    def settings_changed(self,reset=True):
        val = self.changed
        self.changed=False
        return val

    def get_index(self):
        return self.index

    def make_index(self,timestamp):
        if(timestamp-self.index_zero_time >= self.xmax or self.unfreeze):
            self.index=0
            self.index_zero_time=timestamp
            self.unfreeze=False
        else:
            diff=timestamp-self.index_zero_time
            self.index=int(diff*self.freq)
    def timedata_freeze(self, freeze=True):
        self.freeze=freeze
        self.unfreeze=True

class DataOutputManager:

    def __init__(self, backend, key, vmin=0, vmax=100, default=0, step=1):
        self.vmin=vmin
        self.vmax=vmax
        self.step=step
        self.value=default
        self.backend=backend
        self.key=key

    def update(self,value):
        self.value=value
        self.backend.set_setting(self.key,value)

class DataController:

    def __init__(self,backend):
        self.backend=backend
        self.inputs=None
        self.outputs={}

        self.outputs[backend.FIO2]=DataOutputManager(backend,backend.FIO2,0,100,default=21)
        self.outputs[backend.VT]=DataOutputManager(backend,backend.VT,0,1000,default=500, step=10)
        self.outputs[backend.FR]=DataOutputManager(backend,backend.FR,0,50,default=15)
        self.outputs[backend.PEP]=DataOutputManager(backend,backend.PEP,0,30,default=5)
        self.outputs[backend.FLOW]=DataOutputManager(backend,backend.FLOW,0,100,default=60)
        self.outputs[backend.TPLAT]=DataOutputManager(backend,backend.TPLAT,0,100,default=0)
        self.outputs[backend.PMIN]=DataOutputManager(backend,backend.PMIN,0,100,default=30)
        self.outputs[backend.PMAX]=DataOutputManager(backend,backend.PMAX,0,100,default=90)
        self.outputs[backend.VMIN]=DataOutputManager(backend,backend.VMIN,0,100,default=300, step=10)

    def init_inputs(self, xmax, freq):
        self.inputs=DataInputs(xmax,freq)
        self.backend.set_handler(self.inputs.handler)


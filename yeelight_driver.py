#!/usr/bin/python
from yeelight import Bulb,RGBTransition,Flow

class YeelightDriver(object):
    class Constants(object):
        sun_up=102, 20,0
        sun_low = 217,124,0
        min_duration = 50
        min_power = 1
        max_power = 81

    def __init__(self,ip):
        self.bulb= Bulb(ip)

    @property
    def is_bulb_on(self):
        res = self.bulb.get_properties()
        return res["power"]=="on"

    @staticmethod
    def __two_transitions(a, b, duration, powers):
        return [RGBTransition(a[0],
                             a[1],
                             a[2],
                              YeelightDriver.Constants.min_duration,
                             powers[0]),
               RGBTransition(b[0],
                             b[1],
                             b[2],
                             duration,
                             powers[1])]
    @staticmethod
    def array_transition(array):
        return [RGBTransition(r,g,b,duration,lum) for r,g,b,lum,duration in array]

    def run_command(self,command,options=[]):
        bulb=self.bulb
        def switch():
            if command == "on":
                return bulb.turn_on()
            if command == "off":
                return bulb.turn_off()
            if command in ("toggle","toogle"):
                return bulb.toggle()
                
            if command == "brightness":
                if not self.is_bulb_on:
                    bulb.turn_on()
                return bulb.set_brightness(int(options[0]))
            if command == "cozy":
                if not self.is_bulb_on:
                    bulb.turn_on()
                bulb.set_rgb(129,59,0)
                return bulb.set_brightness(19)
            if command in ("sunrise","sunset"):
                duration = int(options[0])
                a = self.Constants.sun_up if command == "sunset" else self.Constants.sun_low
                b = self.Constants.sun_up if command == "sunrise" else self.Constants.sun_low
                transitions = self.two_transitions(a,b,duration,(self.Constants.min_power,self.Constants.max_power))
                flow = Flow(count=1,action = Flow.actions.recover,transitions=transitions)
                return bulb.start_flow(flow)
            if command == "forest":
                array= [(34,74,0,10,60000),(60,112,17,5,60000),(94,150,48,7,60000)]
                transitions=self.array_transition(array)
                return self.bulb.start_flow(Flow(count=0,action = Flow.actions.recover,transitions=transitions))
        switch()
        return "ok"



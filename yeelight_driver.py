#!/usr/bin/python
from yeelight import Bulb,RGBTransition,Flow,SleepTransition

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
            if command == "white":
                if not self.is_bulb_on:
                    bulb.turn_on()
                bulb.set_rgb(255,255,255)
                return bulb.set_brightness(100)
            if command in ("sunrise","sunset"):
                if not self.is_bulb_on:
                    bulb.turn_on()
                duration = int(options[0])
                min_duration = self.Constants.min_duration
                if command == "sunrise":
                    array = [(102, 20,0, 1,min_duration ),
                             (169, 100, 20, 100, duration/2),
                             (255, 255, 255, 100, duration/2)]
                    transitions = self.array_transition(array)
                    action = Flow.actions.stay
                else:
                    array = [(205, 107, 0, 91, min_duration),#13462272
                             (102, 20, 0, 1, duration),
                             (102, 20, 0, 1, 2000)]
                    transitions = self.array_transition(array)
                    action = Flow.actions.off
                flow = Flow(count=1,action = action,transitions=transitions)
                return bulb.start_flow(flow)
            if command in ("forest","sea"):
                default_speed = 60000
                speed = options[0] if len(options)>0 else default_speed
                if type(speed) == list:
                    speed = default_speed

                if command == "sea":
                    array = [(0, 121, 217, 30, speed), (8, 0, 157, 50, speed), (0, 123, 202, 41, speed)]
                    transitions = self.array_transition(array)
                    if not self.is_bulb_on:
                        bulb.turn_on()
                    return self.bulb.start_flow(Flow(count=0, action=Flow.actions.recover, transitions=transitions))
                else:
                    array= [(34, 74, 0, 10, speed), (60, 112, 17, 5, speed), (94, 150, 48, 7, speed)]
                    transitions=self.array_transition(array)
                    if not self.is_bulb_on:
                        bulb.turn_on()
                    return self.bulb.start_flow(Flow(count=0,action = Flow.actions.recover,transitions=transitions))
        switch()
        return "ok"



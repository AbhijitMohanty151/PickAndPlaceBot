import os
import pprint
import pygame
import threading
import math
import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
ledg=35
ledr=37
m1=36
m2=31
m3=8
# m4=16
# m5=24
#m52=22
ser=40
pw1=32
pw2=33
pw3=10
# pw4=18
# pw5=26
GPIO.setup(m1,GPIO.OUT)
GPIO.setup(m2,GPIO.OUT)
GPIO.setup(m3,GPIO.OUT)
# GPIO.setup(m4,GPIO.OUT)
# GPIO.setup(m5,GPIO.OUT)
#GPIO.setup(m52,GPIO.OUT)
GPIO.setup(ser,GPIO.OUT)
GPIO.setup(pw1,GPIO.OUT)
GPIO.setup(pw2,GPIO.OUT)
GPIO.setup(pw3,GPIO.OUT)
# GPIO.setup(pw4,GPIO.OUT)
# GPIO.setup(pw5,GPIO.OUT)
GPIO.setup(ledg,GPIO.OUT)
GPIO.setup(ledr,GPIO.OUT)
pwm1 = GPIO.PWM(pw1, 100)
pwm2 = GPIO.PWM(pw2, 100)
pwm3 = GPIO.PWM(pw3, 100)
# pwm4 = GPIO.PWM(pw4, 100)
# pwm5 = GPIO.PWM(pw5, 100)
servo = GPIO.PWM(ser, 50)
pwm1.start(0)
pwm2.start(0)
pwm3.start(0)
# pwm4.start(0)
# pwm5.start(0)
servo.start(0)
pwm1.ChangeDutyCycle(0)
pwm2.ChangeDutyCycle(0)
pwm3.ChangeDutyCycle(0)
# pwm4.ChangeDutyCycle(0)
# pwm5.ChangeDutyCycle(0)
servo.ChangeDutyCycle(0)
class PS4Controller(object):

    controller = None
    axis_data = None
    button_data = None
    hat_data = None
#     def motor(self,a=0,b=0,c=0,d=0,e=0,f=0):
    def motor(self,a=0,b=0,c=0,d=0):
        pwm1.ChangeDutyCycle(abs(a))
        if b==0:
            pwm2.ChangeDutyCycle(0)
        else:
            pwm2.ChangeDutyCycle(abs(b))
        pwm3.ChangeDutyCycle(abs(c))
#         pwm4.ChangeDutyCycle(abs(d))
#         pwm5.ChangeDutyCycle(abs(e))
        if(a>0):
            GPIO.output(m1,GPIO.LOW)
        else:
           GPIO.output(m1,GPIO.HIGH)
        if(b>0):
            GPIO.output(m2,GPIO.HIGH)
        else:
           GPIO.output(m2,GPIO.LOW)
        if(c>0):
            GPIO.output(m3,GPIO.HIGH)
        else:
           GPIO.output(m3,GPIO.LOW)
#         if(d>0):
#             GPIO.output(m4,GPIO.LOW)
#         else:
#            GPIO.output(m4,GPIO.HIGH)
#         if(e>0):
#             GPIO.output(m5,GPIO.HIGH)
#         else:
#            GPIO.output(m5,GPIO.LOW)
        if(d>0):
            servo.ChangeDutyCycle(7.3)
        elif(d<0):
           servo.ChangeDutyCycle(6.5)
        else:
            servo.ChangeDutyCycle(0)
    def deg(self,a=0,b=0):
        if(abs(a) == 0 and abs(b) == 0):
            k=0
        elif(abs(a) == 0):
            k=90
        else:
            k=round(math.degrees(math.atan(b/a)),1)
        if(a<0):
            k=180-k
        else:
            if(b<0):
                k=abs(k)
            else:
                k=360-k
        if(abs(a) <= 0.5 and abs(b) <= 0.5):
            k=-1
        return k
    def init(self):
        """Initialize the joystick components"""
        
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()
    def listen(self):
        GPIO.output(ledr,GPIO.LOW)
        GPIO.output(ledg,GPIO.LOW)
        ps4.motor(0,0,0,0)
        a=0
        s=20
        if not self.axis_data:
            self.axis_data = {}
            for i in range(0,4):
                self.axis_data[i] = (0)

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    self.axis_data[event.axis] = round(event.value,1)
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.button_data[event.button] = True
                elif event.type == pygame.JOYBUTTONUP:
                    self.button_data[event.button] = False
                elif event.type == pygame.JOYHATMOTION:
                    self.hat_data[event.hat] = event.value
                #os.system('clear')
                #pprint.pprint(self.button_data)
                #pprint.pprint(self.axis_data)
                #pprint.pprint(self.hat_data)
                a1=ps4.deg(self.axis_data[2],self.axis_data[3])
                #print(a1)
                if self.button_data[4]==True:
                    print("inc")
                    s=20
                if self.button_data[6]==True:
                    print("dec")
                    s=10
                if self.button_data[5]==True:
                    print("inc")
                    s=30
                if self.button_data[7]==True:
                    print("dec")
                    s=45
                if self.button_data[8]==True:
                    print("off")
                    GPIO.output(ledr,GPIO.HIGH)
                    GPIO.output(ledg,GPIO.LOW)
                    a=0
                    s=20
                if self.button_data[9]==True:
                    print("on")
                    GPIO.output(ledr,GPIO.LOW)
                    GPIO.output(ledg,GPIO.HIGH)
                    a=1
                if a==1:
                    if self.axis_data[1]<-0.5:
                        print("fwd")
                        ps4.motor(s,s,0,0)
                    elif self.axis_data[1]>0.5:
                        print("rev")
                        ps4.motor(-1*s,-1*s,0,0)
                    elif self.axis_data[0]<-0.5:
                        print("rt")
                        ps4.motor(-1*s,s,0,0)
                    elif self.axis_data[0]>0.5:
                        print("lt")
                        ps4.motor(s,-1*s,0,0)
                    elif a1<=90 and a1>=1:
                        print("fwd rt")
                        ps4.motor(s,0,0,0)
                    elif a1<=180 and a1>=90:
                        print("fwd lt")
                        ps4.motor(0,s,0,0)
                    elif a1<=270 and a1>=180:
                        print("rev lt")
                        ps4.motor(0,-1*s,0,0)
                    elif a1<=360 and a1>=270:
                        print("rev rt")
                        ps4.motor(-1*s,0,0,0)
                    elif self.button_data[3]==True:
                        print("up")
                        ps4.motor(0,0,20,0)
                    elif self.button_data[1]==True:
                        print("dwn")
                        ps4.motor(0,0,-20,0)
                    elif self.button_data[0]==True:
                        print("open")
                        ps4.motor(0,0,0,1)
                    elif self.button_data[2]==True:
                        print("close")
                        ps4.motor(0,0,0,-1)
                    else:
                        print("stop")
                        ps4.motor(0,0,0,0)
            
ps4 = PS4Controller()
ps4.init()
ps4.listen()
#GPIO.output(d4,GPIO.LOW)
#pwm3.ChangeDutyCycle(0)
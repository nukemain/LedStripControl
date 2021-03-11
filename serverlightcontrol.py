import time
import pigpio
import socket
import sys
from gpiozero import Button
from signal import signal, SIGTERM, SIGHUP

pigs = pigpio.pi()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.bind((socket.gethostname(), 1234))
print(socket.gethostname())
s.bind(("192.168.0.100", 1025))





def shutdown():
    print("SHUTDOWN")
    red_alert(3)
    turn_off_lights()
    print("shutting down")
    sys.exit()

def turn_off_lights():
    print("turn_off_lights")
    pigs.set_PWM_dutycycle(17, 0)
    pigs.set_PWM_dutycycle(22, 0)
    pigs.set_PWM_dutycycle(24, 0)

def red_alert(flashes):
    print("red alert: "+str(flashes))
    flashesb = flashes
    pigs.set_PWM_dutycycle(17, 0)
    pigs.set_PWM_dutycycle(22, 0)
    pigs.set_PWM_dutycycle(24, 0)
    i = 0
    f = 0
    while True:
        if(i < flashesb):
            if(f == 0):
                f = 1
                i = i + 1
                pigs.set_PWM_dutycycle(17, 255)
                time.sleep(1)
            else:
                f = 0
                pigs.set_PWM_dutycycle(17, 0)
                time.sleep(1)
        else:
            break
    pigs.set_PWM_dutycycle(17, 0)

def safe_exit():
    print("safe_exit")
    pigs.set_PWM_dutycycle(17, 0)
    pigs.set_PWM_dutycycle(22, 0)
    pigs.set_PWM_dutycycle(24, 0)
    exit(1)


button = Button(26)
button.when_pressed = shutdown
signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

while True:
    try:
        # now our endpoint knows about the OTHER endpoint.
        s.listen(5)
        clientsocket, address = s.accept()
        print(f"Connection from {address} has been established.")
        rcvdData = clientsocket.recv(1024).decode()
        rlen = len(rcvdData)
        if(rlen==0):
            print("pc's fucked")
            turn_off_lights()
            sys.exit()
        else:
            rcvdTable = rcvdData.split("_")
            print(rcvdTable)

            brightnessR = rcvdTable[0] #pin 17
            brightnessG = rcvdTable[1] #pin 22
            brightnessB = rcvdTable[2] #pin 24

            username = rcvdTable[3]
            additional_info = rcvdTable[4]
            additional_info_value = rcvdTable[5]

            if(str(additional_info) == "CLOSE"):
                print("closing")
                turn_off_lights()
                sys.exit()

            if(str(additional_info) == "ALERT"):
                red_alert(int(additional_info_value))
            if(str(additional_info) == "ALERTC"):
                red_alert(int(additional_info_value))
                sys.exit()
            else:
                pigs.set_PWM_dutycycle(17, int(brightnessR))
                pigs.set_PWM_dutycycle(22, int(brightnessG))
                pigs.set_PWM_dutycycle(24, int(brightnessB))
    except KeyboardInterrupt:
        turn_off_lights()
        sys.exit()
'''
pigs.set_PWM_dutycycle(17, 0)
pigs.set_PWM_dutycycle(22, 0)
pigs.set_PWM_dutycycle(24, 0)
'''
import time
import pigpio
import socket
import sys

pigs = pigpio.pi()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.bind((socket.gethostname(), 1234))
print(socket.gethostname())
s.bind(("192.168.0.100", 1025))

def turn_off_lights():
    pigs.set_PWM_dutycycle(17, 0)
    pigs.set_PWM_dutycycle(22, 0)
    pigs.set_PWM_dutycycle(24, 0)

while True:
    # now our endpoint knows about the OTHER endpoint.
    s.listen(5)
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")
    rcvdData = clientsocket.recv(1024).decode()
    rcvdTable = rcvdData.split("_")
    print(rcvdTable)

    brightnessR = rcvdTable[0] #pin 17
    brightnessG = rcvdTable[1] #pin 22
    brightnessB = rcvdTable[2] #pin 24

    username = rcvdTable[3]
    additional_info = rcvdTable[4]

    if(str(additional_info) == "CLOSE"):
        print("closing")
        turn_off_lights()
        sys.exit()

    pigs.set_PWM_dutycycle(17, int(brightnessR))
    pigs.set_PWM_dutycycle(22, int(brightnessG))
    pigs.set_PWM_dutycycle(24, int(brightnessB))
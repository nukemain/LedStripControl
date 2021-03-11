import socket
from SpotifyAPI import MySpotifyAPI
import time
import sys

API = MySpotifyAPI()
songname = ''
oldsongname = ''
i = 0
'''
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("IP_HERE", 1025))
'''

try:
    while True:
        time.sleep(1)
        API.call_token_refresh("C:\\Users\\Sowap\\MySpotifyAPITokenVault.txt")
        print(API.get_currently_playing_songs_name()+"_1")
        if(API.get_currently_playing_songs_name == "JSONERROR_JSONERROR"):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(("IP_HERE", 1025))
                sendData = "0_0_0_PC_ALERTR_3"
                s.send(sendData.encode())
                # ERROR FLASHING
                # ERROR FLASHING
                # ERROR FLASHING
                # ERROR FLASHING
                # ERROR FLASHING
            except TimeoutError:
                print("TimeoutError: could not connect to pi")
                break
        else:
            songname = API.get_currently_playing_songs_name()
            if(songname == oldsongname):
                i = i + 1
                print("pause_" + str(i))
                oldsongname = songname
            else:
                if(API.download_image_of_currently_playing_song("C:\\Users\\Sowap\\Desktop\\test\\currently_playing_songs_img") == "ERROR_NOTLISTENING"):
                    print("you are not listening to anything")
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect(("IP_HERE", 1025))
                        sendData = "0_0_0_PC_ALERTR_3"
                        s.send(sendData.encode())
                        
                        # ERROR FLASHING
                        # ERROR FLASHING
                        # ERROR FLASHING
                        # ERROR FLASHING
                        # ERROR FLASHING
                    except TimeoutError:
                        print("TimeoutError: could not connect to pi")
                        break
                else:
                    colors = API.dominant_color("C:\\Users\\Sowap\\Desktop\\test\\currently_playing_songs_img.png")
                    #print(API.most_common_used_color())
                    red = round(int(colors[0]))
                    green = round(int(colors[1]))
                    blue = round(int(colors[2]))

                    if(red > 255):
                        red = 255
                    if(green > 255):
                        green = 255
                    if(blue > 255):
                        blue = 255   

                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect(("IP_HERE", 1025))
                        print("Sending color data")
                    except TimeoutError:
                        print("TimeoutError: could not connect to pi")
                        break
                    additional_argument = "NONE"
                    additional_argument_value = "0"
                    sendData = str(red)+"_"+str(green)+"_"+str(blue)+"_PC_"+additional_argument+"_"+additional_argument_value
                    s.send(sendData.encode())
                    oldsongname = songname

except KeyboardInterrupt:
    print('Interrupted')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("IP_HERE", 1025))
        #sendData = "0_0_0_PC_CLOSE_0"
        sendData = "0_0_0_PC_ALERTC_1"
        s.send(sendData.encode())
        sys.exit()
    except TimeoutError:
        print("TimeoutError: could not connect to pi")

sys.exit() 

import socket
from SpotifyAPI import MySpotifyAPI
import time
API = MySpotifyAPI()
songname = ''
oldsongname = ''
i = 0
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    while True:
        time.sleep(1)
        API.call_token_refresh("C:\\Users\\Sowap\\MySpotifyAPITokenVault.txt")
        print(API.get_currently_playing_songs_name()+"_1")
        songname = API.get_currently_playing_songs_name()
        if(songname == oldsongname):
            i = i + 1
            print("pause_" + str(i))
            oldsongname = songname
        else:
            print(API.download_image_of_currently_playing_song("C:\\Users\\Sowap\\Desktop\\test\\currently_playing_songs_img")+"_2")
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
                s.connect(("192.168.0.100", 1025))
            except TimeoutError:
                print("TimeoutError: could not connect to pi")
                break
            additional_argument = "NONE"
            sendData = str(red)+"_"+str(green)+"_"+str(blue)+"_PC_"+additional_argument
            s.send(sendData.encode())
            oldsongname = songname
except KeyboardInterrupt:
    print('Interrupted')
    s.connect(("192.168.0.100", 1025))
    sendData = "0_0_0_PC_CLOSE"
    s.send(sendData.encode())


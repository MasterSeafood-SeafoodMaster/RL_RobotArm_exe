import socket
from l298n_test import l298n
from moveLib import movementManager

HOST="192.168.137.116"
def start_server(host=HOST, port=12345):
    driver = l298n()
    mm=movementManager()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Server listening on {host}:{port}")
        ignore=0
        
        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    if ignore>0:
                        ignore-=1
                    else:
                        s=data.decode()
                        rl=(int(s[0:2])-45) #r90
                        fb=(int(s[2:4])-45)*-1 #b90
                        rl=rl/45*50
                        fb=fb/45*50

                        a=s[4]
                        b=s[5]
                        x=s[6]
                        y=s[7]
                        print(fb+rl, fb-rl)
                        driver.set_motor_speed(fb+rl, fb-rl)

                        if a=="1": 
                            if mm.foward==False:
                                mm.lookForward()
                            else:
                                mm.reset()
                            ignore=10
                        elif b=="1": mm.aim('red')
                        elif x=="1": 
                            if mm.loaded == False:
                                mm.load()
                            else:
                                mm.unload()
                            ignore=10                        
                            
                        elif y=="1":
                            if mm.block == False:
                                mm.grab()
                            else:
                                mm.putdown()
                            ignore=10
                            



if __name__ == "__main__":
    start_server()

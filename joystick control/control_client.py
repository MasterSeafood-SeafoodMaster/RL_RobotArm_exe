import socket
import time
from controler import JoystickHandler

HOST="192.168.137.116"
def send_joystick_state(host=HOST, port=12345):
    cont = JoystickHandler()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        while True:
            cont.update()
            state = cont.get_joystick_state()
            client_socket.sendall(state.encode())
            time.sleep(0.05)

if __name__ == "__main__":
    send_joystick_state()

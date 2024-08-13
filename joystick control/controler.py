import pygame
import sys

class JoystickHandler:
    def __init__(self):
        pygame.init()
        if pygame.joystick.get_count() == 0:
            print("没有检测到任何操纵杆。")
            sys.exit()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        self.num_axes = self.joystick.get_numaxes()
        self.num_buttons = self.joystick.get_numbuttons()
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Joystick Button and Axis Detection")

    def get_joystick_state(self):
        state = ""
        for i in range(2):
            axis_value = self.joystick.get_axis(i)
            fixed = int(round((axis_value + 1), 2) * 45)
            sf = str(fixed).zfill(2)
            if axis_value > 0.2:
                state += sf
            elif axis_value < -0.2:
                state += sf
            else:
                state += "45"
        for i in range(4):
            if self.joystick.get_button(i):
                state += "1"
            else:
                state += "0"
        return state

    def update(self):
        # Call this method to update the pygame event queue
        pygame.event.pump()

if __name__ == "__main__":
    joystick_handler = JoystickHandler()
    for _ in range(100):
        joystick_handler.update()
        state = joystick_handler.get_joystick_state()
        print(state)
        time.sleep(0.05)
    pygame.quit()

import RPi.GPIO as GPIO
import time


class Car:
    def __init__(self):

        self.enA=21; self.in1=26; self.in2=19;
        self.in3=13; self.in4=6; self.enB=5;

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.enA, GPIO.OUT)
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        GPIO.setup(self.enB, GPIO.OUT)
        GPIO.setup(self.in3, GPIO.OUT)
        GPIO.setup(self.in4, GPIO.OUT)

        self.pwmA = GPIO.PWM(self.enA, 800)
        self.pwmB = GPIO.PWM(self.enB, 800)

    def left(self):
        GPIO.output(self.in1, False)
        GPIO.output(self.in2, True)
        self.pwmA.start(100)
        GPIO.output(self.in3, False)
        GPIO.output(self.in4, True)
        self.pwmB.start(100)
    def right(self):
        GPIO.output(self.in1, True)
        GPIO.output(self.in2, False)
        self.pwmA.start(100)
        GPIO.output(self.in3, True)
        GPIO.output(self.in4, False)
        self.pwmB.start(100)

    def fd(self):
        GPIO.output(self.in1, True)
        GPIO.output(self.in2, False)
        self.pwmA.start(100)
        GPIO.output(self.in3, False)
        GPIO.output(self.in4, True)
        self.pwmB.start(100)

    def bd(self):
        GPIO.output(self.in1, False)
        GPIO.output(self.in2, True)
        self.pwmA.start(100)
        GPIO.output(self.in3, True)
        GPIO.output(self.in4, False)
        self.pwmB.start(100)
    def stop(self): 
        self.pwmA.stop()
        self.pwmB.stop()


if __name__ == '__main__':
    car=Car()
    car.left()
    time.sleep(1)
    car.right()
    time.sleep(1)
    car.fd()
    time.sleep(1)
    car.bd()
    time.sleep(1)

    GPIO.cleanup()

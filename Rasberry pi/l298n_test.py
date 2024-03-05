import RPi.GPIO as GPIO


class l298n:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.ENA = 26
        self.IN1 = 19
        self.IN2 = 13

        self.IN3 = 21
        self.IN4 = 20
        self.ENB = 16

        GPIO.setup(self.ENA, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.ENB, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.IN1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.IN2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.IN3, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.IN4, GPIO.OUT, initial=GPIO.LOW)

        self.pA = GPIO.PWM(self.ENA, 100)
        self.pB = GPIO.PWM(self.ENB, 100)
        self.pA.start(0)
        self.pB.start(0)

    def set_motor_speed(self, lSpeed, rSpeed):
        if lSpeed >= 0:
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            
        else:
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
            
        if rSpeed >= 0:
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)
        else:
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)

        self.pA.ChangeDutyCycle(abs(lSpeed))
        self.pB.ChangeDutyCycle(abs(rSpeed))

    def release(self):
        self.pA.stop()
        self.pB.stop()
        GPIO.cleanup()

if __name__=='__main__':
    import time
    driver = l298n()
    driver.set_motor_speed(50, 50)
    time.sleep(1)
    driver.set_motor_speed(0, 0)
    time.sleep(1)

    driver.set_motor_speed(-50, 50)
    time.sleep(1)
    driver.set_motor_speed(0, 0)
    time.sleep(1)

    driver.set_motor_speed(50, -50)
    time.sleep(1)
    driver.set_motor_speed(0, 0)
    time.sleep(1)

    driver.set_motor_speed(-50, -50)
    time.sleep(1)
    driver.set_motor_speed(0, 0)
    time.sleep(1)

    driver.release()





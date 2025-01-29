import machine
import utime
from pixy2 import Pixy2SPI, Line

pixy = Pixy2SPI(cs=0)

# Motor GPIO pins
LEFT_MOTOR_PIN1 = 0
LEFT_MOTOR_PIN2 = 1
RIGHT_MOTOR_PIN1 = 2
RIGHT_MOTOR_PIN2 = 3

# Initialize motor control pins
left_motor_forward = machine.Pin(LEFT_MOTOR_PIN1, machine.Pin.OUT)
left_motor_backward = machine.Pin(LEFT_MOTOR_PIN2, machine.Pin.OUT)
right_motor_forward = machine.Pin(RIGHT_MOTOR_PIN1, machine.Pin.OUT)
right_motor_backward = machine.Pin(RIGHT_MOTOR_PIN2, machine.Pin.OUT)

def set_motor_speed(motor_forward, motor_backward, speed):
    if speed > 0:
        motor_forward.on()
        motor_backward.off()
    elif speed < 0:
        motor_forward.off()
        motor_backward.on()
    else:
        motor_forward.off()
        motor_backward.off()

    # Adjust the duty cycle for speed control
    speed = abs(speed)
    speed = min(speed, 100)
    pwm_duty = int((speed / 100) * 1023)
    pwm.freq(1000) 
    pwm.duty_u16(pwm_duty)

# Initialize PWM for motor speed control
pwm = machine.PWM(machine.Pin(LEFT_MOTOR_PIN1))

# Initialize line detection parameters
LINE_THRESHOLD = 50
MAX_SPEED = 100
BASE_SPEED = 50

while True:
    lines = pixy.get_lines()

    if lines:
        lines.sort(key=lambda line: line.angle)

        center_line = lines[len(lines) // 2]

        error = center_line.x - pixy.frame_width // 2

        speed_left = BASE_SPEED + (error * MAX_SPEED // LINE_THRESHOLD)
        speed_right = BASE_SPEED - (error * MAX_SPEED // LINE_THRESHOLD)

        set_motor_speed(left_motor_forward, left_motor_backward, speed_left)
        set_motor_speed(right_motor_forward, right_motor_backward, speed_right)

        print(f"Error: {error}, Left Speed: {speed_left}, Right Speed: {speed_right}")

    utime.sleep_ms(10)

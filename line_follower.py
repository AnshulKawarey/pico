import time
import machine

PIXYCAM_ADDRESS = 0x54

motor_left_forward = machine.Pin(11, machine.Pin.OUT)
motor_left_backward = machine.Pin(12, machine.Pin.OUT)
motor_right_forward = machine.Pin(13, machine.Pin.OUT)
motor_right_backward = machine.Pin(14, machine.Pin.OUT)


target_center = 160
kp = 0.1 

def follow_line():
    i2c = machine.I2C(0, scl=machine.Pin(21), sda=machine.Pin(20), freq=100000)

    while True:
        i2c.writeto(PIXYCAM_ADDRESS, bytes([174, 193]))

        block_data = i2c.readfrom(PIXYCAM_ADDRESS, 14)

        if block_data[0] == 0xaa and block_data[1] == 0x55:
            block_center = (block_data[7] << 8) | block_data[6]

            error = target_center - block_center

            motor_speed = int(kp * error)

            left_speed = 50 + motor_speed
            right_speed = 50 - motor_speed

            motor_left_forward.value(left_speed > 0)
            motor_left_backward.value(left_speed < 0)
            motor_right_forward.value(right_speed > 0)
            motor_right_backward.value(right_speed < 0)

            motor_left_forward.duty(abs(left_speed))
            motor_left_backward.duty(abs(left_speed))
            motor_right_forward.duty(abs(right_speed))
            motor_right_backward.duty(abs(right_speed))

        time.sleep(0.1)

follow_line()
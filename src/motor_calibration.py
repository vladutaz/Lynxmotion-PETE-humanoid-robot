import serial
import time
import pygame

from ssc32u import SSC32U
from Config import *


def calibrate_motor(channel, min_pulse=500, max_pulse=2500, step=100, delay=1):
    """
    Calibrate a single motor by moving it through its range of motion.
    
    Args:
        channel: Servo channel (0-31)
        min_pulse: Minimum pulse width in microseconds
        max_pulse: Maximum pulse width in microseconds
        step: Step size for pulse width increment
        delay: Delay between movements in seconds
    """
    
    try:
        ssc = SSC32U()
        
        print(f"Calibrating motor on channel {channel}")
        
        # Move from min to max
        for pulse in range(min_pulse, max_pulse + 1, step):
            ssc.move_servo(channel, pulse, time_ms=500)
            time.sleep(delay)
        
        # Move from max to min
        for pulse in range(max_pulse, min_pulse - 1, -step):
            ssc.move_servo(channel, pulse, time_ms=500)
            time.sleep(delay)
        
        print("Calibration complete.")
    
    except Exception as e:
        print(f"Error during calibration: {e}")
    
    finally:
        ssc.close()

def get_pygame_key():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return 'x' # Treat closing the window as exit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return chr(0x1b) # ESC key
            elif event.key == pygame.K_w:
                return 'w'
            elif event.key == pygame.K_s:
                return 's'
    return None

def manual_calibration(channel, step=100, delay=1):
    """
    Calibrate a single motor moving it manually step by step.
    
    Args:
        channel: Servo channel (0-31)
        step: Step size for pulse width increment
        delay: Delay between movements in seconds
    """
    
    print("--------Manual Control--------\n")
    print("x or esc to exit | w to move CW | s to move CCW\n")
    print(f"You are now controling motor {channel}")

    try:
        ssc = SSC32U()
        pos = Config().get_motor_home_position(channel)


        running = True
        while(running):
            key = get_pygame_key()

            if key == chr(0x1b) or key == 'x':
                running = False
            elif key == 'w':
                ssc.move_servo(channel, pos+step, time_ms=500)
                pos += step
            elif key == 's':
                ssc.move_servo(channel, pos-step)

    except Exception as e:
        print(f"Error during calibration: {e}")
    
    finally:
        ssc.close()

if __name__ == "__main__":
    print("Normal Calibration")
    for channel in range(31):
        calibrate_motor(channel)

    print("Manual Calibration")
    for channel in range(31):
        manual_calibration(channel)
    
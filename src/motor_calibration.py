import serial
import time
import pygame

from ssc32u import SSC32U
from Config import Config


def calibrate_motor(channel, ssc=None, min_pulse=500, max_pulse=2500, step=100, delay=1):
    """
    Calibrate a single motor by moving it through its range of motion.
    
    Args:
        channel: Servo channel (0-31)
        board: SSC32U board instance
        min_pulse: Minimum pulse width in microseconds
        max_pulse: Maximum pulse width in microseconds
        step: Step size for pulse width increment
        delay: Delay between movements in seconds
    """

    try:
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

def get_pygame_key():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return 'x' # T  reat closing the window as exit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return chr(0x1b) # ESC key
            elif event.key == pygame.K_w:
                return 'w'
            elif event.key == pygame.K_s:
                return 's'
            elif event.key == pygame.K_x:
                return 'x'
            elif event.key == pygame.K_SPACE:
                return 'space'
    return None

def manual_calibration(channel, ssc=None, step=10, delay=1):
    """
    Calibrate a single motor moving it manually step by step.
    
    Args:
        channel: Servo channel (0-31)
        step: Step size for pulse width increment
        delay: Delay between movements in seconds
    """
    
    print("--------Manual Control--------\n")
    print("x or esc to exit | w to move CW | s to move CCW | space to save position\n")
    print(f"You are now controling motor {channel}")

    try:
        pos = Config().get_motor_home_position(channel)


        running = True
        while(running):
            key = get_pygame_key()

            if key == chr(0x1b) or key == 'x':
                running = False
            elif key == 'w':
                ssc.move_servo(channel, pos+step)
                pos += step
            elif key == 's':
                ssc.move_servo(channel, pos-step)
                pos -= step
            elif key == 'space':
                Config().set_home_pos(channel, pos, save = True)

    except Exception as e:
        print(f"Error during calibration: {e}")

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Motor Calibration")
    ssc = None

    try:
        ssc = SSC32U()
        #print("Normal Calibration")
        #for channel in range(31):   
        #    calibrate_motor(channel, ssc)

        print("Manual Calibration")
        for channel in range(31):
            manual_calibration(channel, ssc)

    except Exception as e:
        print(f"Error during calibration: {e}")

    finally:
        pygame.quit()
        if ssc is not None:
            ssc.close()
    
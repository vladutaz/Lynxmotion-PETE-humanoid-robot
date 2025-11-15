import serial
import time

from ssc32u import SSC32U


if __name__ == "__main__":
    # Change this to your COM port
    # Windows: 'COM2', 'COM3', etc.
    # If using Bluetooth, ensure the correct COM port is selected
    PORT = 'COM3'
    
    try:
        ssc = SSC32U(PORT, baudrate=115200)
        
        # Center all servos
        print("\nCentering all servos")
        ssc.center_all_servos(num_servos=31)
        motor_position = 1500
        time.sleep(2)
        
        # Manual control loop
        print("\nManual Servo Control")
        print("Use 'a' for Clock-wise and 'd' for Counter-clockwise")
        servo_to_move = int(input("Enter the servo channel to move (0-31): "))
        print("Press Ctrl+C to exit")   
        
        while True:
            direction = input("Enter direction (a/d): ").strip().lower()
            if direction == 'a':
                motor_position += 50  # Clock-wise
            elif direction == 'd':
                motor_position -= 50  # Counter-clockwise
            ssc.move_servo(servo_to_move, motor_position)
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        ssc.close()
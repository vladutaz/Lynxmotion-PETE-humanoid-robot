import serial
import time

from ssc32u import SSC32U


if __name__ == "__main__":
    # Change this to your COM port
    # Windows: 'COM2', 'COM3', etc.
    # If using Bluetooth, ensure the correct COM port is selected and select in and out
    PORT = 'COM3'
    #PORT_IN = 'COM6'  # Bluetooth in
    #PORT_OUT = 'COM7' # Bluetooth out
    BAUDRATE = 115200
    
    try:
        ssc = SSC32U(PORT, baudrate=BAUDRATE)
        #ssc_in = SSC32U(PORT_IN, baudrate=BAUDRATE)
        #ssc_out = SSC32U(PORT_OUT, baudrate=BAUDRATE)
        # Center all servos
        print("\nCentering all servos")
        ssc.center_all_servos(num_servos=31)
        
        print("All servos centered.")
        time.sleep(2)
        
        # Move multiple servos at once
        #print("\n--- Moving multiple servos ---")
        #ssc.move_servos({
        #    0: 1500,
        #    1: 2000,
        #    2: 1000,
        #    3: 1800
        #}, time_ms=2000)
        #time.sleep(2.5)
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        ssc.close()
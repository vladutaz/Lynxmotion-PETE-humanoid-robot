import serial
import time

from ssc32u import SSC32U


if __name__ == "__main__":
    ssc = None
    
    try:
        ssc = SSC32U()
        print("\nCentering all servos")
        
        ssc.center_all_servos()
        
        print("All servos centered.")
        time.sleep(2)
        
    except Exception as e:  
        print(f"Error: {e}")
    
    finally:
        if ssc is not None:
            ssc.close()
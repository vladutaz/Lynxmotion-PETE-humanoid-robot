import serial
import time
import yaml

CONFIG_FILE = '../Config/motor_config.yaml'

class SSC32U:
    """
    Controller class for SSC-32U servo controller
    """
    
    def __init__(self, port, baudrate=115200, timeout=1):
        """
        Initialize connection to SSC-32U
        
        Args:
            port: COM port (e.g., 'COM5' on Windows, '/dev/rfcomm0' on Linux)
            baudrate: Communication speed (default: 9600)
            timeout: Serial timeout in seconds
        """
        try:
            self.serial = serial.Serial(port, baudrate, timeout=timeout)
            time.sleep(2)
            print(f"Connected to SSC-32U on {port}")
        except serial.SerialException as e:
            print(f"Error connecting: {e}")
            raise
    
    def send_command(self, command):
        """
        Send raw command to SSC-32U
        
        Args:
            command: Command string (will automatically add carriage return)
        """
        if not command.endswith('\r'):
            command += '\r'
        self.serial.write(command.encode())
        print(f"Sent: {command.strip()}")
    
    def move_servo(self, channel, position, time_ms=1000):
        """
        Move a single servo to a position
        
        Args:
            channel: Servo channel (0-31)
            position: Pulse width in microseconds (500-2500)
            time_ms: Movement time in milliseconds (default: 1000)
        """
        command = f"#{channel}P{position}T{time_ms}"
        self.send_command(command)
    
    def move_servos(self, servo_positions, time_ms=1000):
        """
        Move multiple servos simultaneously
        
        Args:
            servo_positions: Dictionary of {channel: position}
            time_ms: Movement time in milliseconds
        """
        command = ""
        for channel, position in servo_positions.items():
            command += f"#{channel}P{position}"
        command += f"T{time_ms}"
        print(f"Sending command: {command}")
        self.send_command(command)
    
    def center_servo(self, channel, time_ms=1000):
        """
        Move servo to center position (1500us)
        
        Args:
            channel: Servo channel (0-31)
            time_ms: Movement time in milliseconds
        """
        self.move_servo(channel, 1500, time_ms)
    
    def center_all_servos(self, num_servos=6, time_ms=2000):
        """
        Center all servos
        
        Args:
            num_servos: Number of servos to center (default: 6)
            time_ms: Movement time in milliseconds
        """
        servo_positions = {i: 1500 for i in range(num_servos)}
        print(f"Centering {num_servos} servos")
        self.move_servos(servo_positions, time_ms)
    
    def close(self):
        """
        Close the serial connection
        """
        if self.serial.is_open:
            self.serial.close()
            print("Connection closed")
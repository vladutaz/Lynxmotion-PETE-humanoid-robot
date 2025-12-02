import serial
import time
import yaml

from typing import Optional, List, Dict
from dataclasses import dataclass
from Config import CONFIG_FILE, Config

#CONFIG_FILE = '../Config/motor_config.yaml'

@dataclass
class LimbConfig:
    motor_ids: List[int]
    home_positions: List[float]
    joint_names: List[str]

class SSC32U:
    """
    Controller class for SSC-32U servo controller
    """
    
    def __init__(self,timeout=1):
        """
        Initialize connection to SSC-32U
        
        Args:
            port: COM port (e.g., 'COM5' on Windows, '/dev/rfcomm0' on Linux)
            baudrate: Communication speed (default: 9600)
            timeout: Serial timeout in seconds
        """
        self.libs = self._parse_limbs()
        self.port = None
        self.baudrate = None

        try:

            if self.port is None:
                self.port = Config().get_system_conf("port")
            if self.baudrate is None:
                self.baudrate = Config().get_system_conf("baud_rate")

            self.serial = serial.Serial(self.port, self.baudrate, timeout=timeout)
            time.sleep(2)
            print(f"Connected to SSC-32U on {self.port}")
        except serial.SerialException as e:
            print(f"Error connecting: {e}")
            raise


    def _parse_limbs(self) -> dict:
        """Parse limb configurations into structured objects"""
        limbs = {}

        cfg_instance = Config()
        
        robot_config = cfg_instance.get_robot_config()
        servo_data = robot_config.get('servos', {})

        for name, data in servo_data.items():
            limbs[name] = LimbConfig(
                motor_ids=data['motor_ids'],
                home_positions=data['home_positions'],
                joint_names=data['joint_names']
            )
        return limbs
    

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
        self.move_servo(channel, Config().get_system_conf("center_position"), time_ms)
    
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
            self.port = None
            self.baudrate = None
            self.serial.close()
            print("Connection closed")
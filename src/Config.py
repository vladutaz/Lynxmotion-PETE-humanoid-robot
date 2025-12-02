from enum import Enum
from typing import Union, Dict
from pathlib import Path
import threading
from sympy import content
import yaml
import os

__all__ = ["Config"]

CONFIG_FILE = os.path.join(os.path.dirname(__file__), '../Config/motor_config.yaml')


class Config:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, config_path=CONFIG_FILE):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Config, cls).__new__(cls)
                cls._instance._load(config_path)
        return cls._instance

    def _load(self, path):
        with open(path, 'r') as f:
            content = f.read()
        
        # Print the file with line numbers
        #print("=" * 50)
        #print("YAML FILE CONTENT:")
        #print("=" * 50)
        #for i, line in enumerate(content.split('\n'), 1):
        #    print(f"{i:3d}: {repr(line)}")
        #print("=" * 50)
    
        # Try to parse
        self._data: dict = yaml.safe_load(content)

    ##############################################################
    # Getters
    ##############################################################
    
    def get_motor_home_position(self, motor_id: int) -> float:
        """
        Get home position for a specific motor ID
        
        Args:
            motor_id: Motor ID (e.g., 0, 1, 12, 13, etc.)
            
        Returns:
            float: Home position for that motor
        """
        servos = self._data.get('servos', {})
        
        for limb_name, limb_data in servos.items():
            if not isinstance(limb_data, dict):
                continue
            
            if 'motor_ids' in limb_data and 'home_positions' in limb_data:
                motor_ids = limb_data['motor_ids']
                home_positions = limb_data['home_positions']
                
                if motor_id in motor_ids:
                    index = motor_ids.index(motor_id)
                    return home_positions[index]
        
        raise ValueError(f"Motor ID {motor_id} not found in configuration")
    
    def get_motor_home_map(self) -> Dict[int, float]:
        """
        Get complete mapping of motor_id -> home_position
        
        Returns:
            dict: {motor_id: home_position}
        """
        motor_map = {}
        servos = self._data.get('servos', {})
        
        for limb_name, limb_data in servos.items():
            # Skip non-limb entries
            if not isinstance(limb_data, dict):
                continue
                
            if 'motor_ids' in limb_data and 'home_positions' in limb_data:
                motor_ids = limb_data['motor_ids']
                home_positions = limb_data['home_positions']
                
                for motor_id, home_pos in zip(motor_ids, home_positions):
                    motor_map[motor_id] = home_pos
        
        return motor_map
    
    def get_limb_config(self, limb_name: str) -> dict:
        """Get configuration for a specific limb"""
        servos = self._data.get('servos', {})
        if limb_name not in servos:
            raise ValueError(f"Limb '{limb_name}' not found in configuration")
        return servos[limb_name]
    
    def get_all_limbs(self):
        """Get all configured limb names"""
        limbs = []
        servos = self._data.get('servos', {})
        for key, value in servos.items():
            if isinstance(value, dict) and 'motor_ids' in value:
                limbs.append(key)
        return limbs

    def get_system_conf(self, key: str):
        """Get system configuration value"""
        return self._data.get("system", {}).get(key)
    
    def get_robot_config(self):
        """Get robot configuration"""
        return self._data.get('robot_config', {})
    
    ##############################################################
    # Setters
    ##############################################################

    def set_home_pos(self, motor_id: int, pos: float, save: bool = False) -> None:
        """
        Set home position for a specific motor ID
        
        Args:
            motor_id: Motor ID (e.g., 0, 1, 12, 13, etc.)
            pos: float
            save: bool - Change the yaml file or not
        """

        print(f"Servo {motor_id} has home position set to {pos}")
        servos = self._data.get('servos', {})

        for limb_name, limb_data in servos.items():
            if not isinstance(limb_data, dict):
                continue
        
            if 'motor_ids' in limb_data and 'home_positions' in limb_data:
                motor_ids = limb_data['motor_ids']
                home_positions = limb_data['home_positions']
                if motor_id in motor_ids:
                    index = motor_ids.index(motor_id)
                    home_positions[index] = pos
                    if save:
                        self.save_config()
                    return

        raise ValueError(f"Motor ID {motor_id} not found in configuration")
    
    def save_config(self, path=None):
        """
        Save the current configuration back to the YAML file
    
        Args:
            path: Optional path to save to. If None, uses the original config file path.
        """
        if path is None:
            path = CONFIG_FILE
    
        with open(path, 'w') as f:
            yaml.dump(self._data, f, default_flow_style=False, sort_keys=False, width=1000)
    
        print(f"Configuration saved to {path}")
    


if __name__ == "__main__":
    config = Config()
    
    # Test system config
    print("Baud rate:", config.get_system_conf("baud_rate"))
    
    # Test motor home position lookup
    print("\nMotor home positions:")
    print("Motor 0:", config.get_motor_home_position(0))
    print("Motor 12:", config.get_motor_home_position(12))
    print("Motor 24:", config.get_motor_home_position(24))
    
    # Test complete motor map
    print("\nAll motor mappings:")
    motor_map = config.get_motor_home_map()
    for motor_id, home_pos in sorted(motor_map.items()):
        print(f"  Motor {motor_id}: {home_pos}")
    
    # Test limb config
    print("\nRight arm config:")
    print(config.get_limb_config('right_arm'))
    
    # Test all limbs
    print("\nAll limbs:")
    print(config.get_all_limbs())
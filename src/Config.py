from enum import Enum
from typing import Union, Dict
import threading
import yaml

__all__ = ["Config"]


CONFIG_FILE = '../Config/motor_config.yaml'


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
            self._data: dict = yaml.safe_load(f)

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
        for limb_name, limb_data in self._data.items():
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
        
        for limb_name, limb_data in self._data.items():
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
        if limb_name not in self._data:
            raise ValueError(f"Limb '{limb_name}' not found in configuration")
        return self._data[limb_name]
    
    def get_all_limbs(self):
        """Get all configured limb names"""
        limbs = []
        for key, value in self._data.items():
            if isinstance(value, dict) and 'motor_ids' in value:
                limbs.append(key)
        return limbs

    def get_system_conf(self, key: str):
        """Get system configuration value"""
        return self._data.get("system", {}).get(key)
    
    ##############################################################
    # Setters
    ##############################################################

    def set_home_pos(self, motor_id: int, pos: float) -> None:
        """
        Set home position for a specific motor ID
        
        Args:
            motor_id: Motor ID (e.g., 0, 1, 12, 13, etc.)
            pos: float
        """
        for limb_name, limb_data in self._data.items():
            if not isinstance(limb_data, dict):
                continue
        
        if 'motor_ids' in limb_data and 'home_positions' in limb_data:
            motor_ids = limb_data['motor_ids']
            home_positions = limb_data['home_positions']
        if motor_id in motor_ids:
            index = motor_ids.index(motor_id)
            home_positions[index] = pos
            return  # done!

        raise ValueError(f"Motor ID {motor_id} not found in configuration")
    

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
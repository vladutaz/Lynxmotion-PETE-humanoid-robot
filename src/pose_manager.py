from enum import Enum
from typing import Union, Dict
from pathlib import Path
from sympy import content
import threading
import yaml
import os
import serial
import time
import pygame

from ssc32u import SSC32U
from Config import Config

__all__ = ["PoseManager"]

POSES_FILE = os.path.join(os.path.dirname(__file__), '../Config/poses.yaml')

class PoseManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, config_path=POSES_FILE):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Config, cls).__new__(cls)
                cls._instance._load(config_path)
        return cls._instance

    def _load(self, path):
        with open(path, 'r') as f:
            content = f.read()
        self._data: dict = yaml.safe_load(content)

    def save_pose(self, path=None, pos_name:str = None):
        """
        Save the current configuration back to the YAML file
    
        Args:
            path: Optional path to save to. If None, uses the original config file path.
        """
        if path is None:
            path = POSES_FILE

        with open(path, 'w') as f:
            yaml.dump(self._data, f, default_flow_style=False, sort_keys=False, width=1000)
    
        print(f"Configuration saved to {path}")

    def add_pose(self, motor_id: int, pos: float, pos_name: str) -> None:
        """
        Set pose
        
        Args:
            motor_id: Motor ID (e.g., 0, 1, 12, 13, etc.)
            pos: float
            pos_name: str - set the name of the pos
        """

        save = True
        poses = self._data.get('poses', {})

        print(f"New pose added called: {pos_name}")

        if pos_name is not poses or not isinstance(poses[pos_name], list):
            poses[pos_name] = []

        for name, steps in poses.items():
            if not isinstance(steps, dict):
                continue
        
            if 'motor_ids' in steps and 'position' in steps:
                motor_ids = steps['motor_ids']
                position = steps['position']
                if motor_id in motor_ids:
                    index = motor_ids.index(motor_id)
                    position[index] = pos
                    if save:
                        self.save_pose()
                    return

    def get_pose(self):
        pass

    def update_frame(self):
        pass

if __name__ == "__main__":
    pose = PoseManager()


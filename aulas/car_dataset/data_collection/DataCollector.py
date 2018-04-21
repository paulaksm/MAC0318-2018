from Camera import Camera
import os
import sys
from pathlib import Path

path_current_dir = Path(os.getcwd())
two_level_up = path_current_dir.parents[1]
sys.path.append(str(two_level_up))

from python_java.USBInterface import USBInterface

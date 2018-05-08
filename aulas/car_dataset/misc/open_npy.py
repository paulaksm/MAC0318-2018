from pathlib import Path
import os
import sys
import numpy as np
import cv2

path_current_dir = Path(os.getcwd())
one_level_up = path_current_dir.parents[0]
parent_dir = os.path.join(str(one_level_up), "data_manipulation")
sys.path.append(str(parent_dir))

import util

command2int = {"up": 0, "left": 1, "right": 2}
int2command = {i[1]: i[0] for i in command2int.items()}

data, labels = util.load_dataset(sys.argv[1], sys.argv[2])

dir_names = [ int2command.get(i) for i in np.unique(labels) ]

for d in dir_names:
    path = os.path.join(os.getcwd(), d)
    if not os.path.isdir(path):
        os.mkdir(path)

for idx, img in enumerate(data):
    path = os.path.join(os.getcwd(), int2command.get(labels.item(idx)))
    img = util.get_image(img, height=45, width=80,channels=1)
    path = os.path.join(path, str(idx) + '.png')
    cv2.imwrite(path, img)

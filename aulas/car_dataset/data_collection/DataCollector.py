import os
import sys
import argparse
import pickle
import keyboard as key
from pathlib import Path
from Camera import Camera

path_current_dir = Path(os.getcwd())
one_level_up = path_current_dir.parents[0]
two_level_up = path_current_dir.parents[1]
parent_dir = os.path.join(str(two_level_up), "python_java")
sys.path.append(str(one_level_up))
sys.path.append(str(parent_dir))
import util         # file located in ../util.py
import USBInterface # file located in ../../python_java/USBInterface.py

class DataCollector(object):

    def __init__(self, camera, brick, name):
        date = util.get_date()
        if not os.path.exists(name):
            os.mkdir(name)
        self.dir_name = os.path.join(name, date)
        self.pickle_name = os.path.join(name, date + "_pickle")
        if not os.path.isdir(self.dir_name):
            os.mkdir(self.dir_name)
        self.data_dict = {}
        self.count = 0
        self.brick = brick
        self.camera = camera

    def save_image_and_label(self, img, label):
        img_name = str(self.count) + ".png"
        img_name = os.path.join(self.dir_name, img_name)
        self.camera.save_picture(img_name, img)
        self.data_dict[str(self.count)] = label
        self.count += 1

    def generate_data(self):
        """
        Method to generate the dataset.
        The car is controlled with the keyboard using the arrow keys, to exit just type "q".
        """
        print("Ready...")
        while True:
            img = self.camera.take_picture()

            if key.is_pressed('q'):
                self.brick.send('\x64')
                print('Exiting...')
                break
            elif key.is_pressed('up'):
                self.brick.send('\x01')
                self.save_image_and_label(img, 'up')

            elif key.is_pressed('down'):
                self.brick.send('\x02')

            elif key.is_pressed('left'):
                self.brick.send('\x04')
                self.save_image_and_label(img, 'left')

            elif key.is_pressed('right'):
                self.brick.send('\x03')
                self.save_image_and_label(img, 'right')
            else:
                self.brick.send('\x05')

        with open(self.pickle_name, "wb") as labels_file:
            pickle.dump(self.data_dict, labels_file)

def main():
    """
    Data Collector class 
    """
    description = "Class for data collection using a camera and a remote controlled robot car connected to USB"
    parser = argparse.ArgumentParser(description=description)
    
    parser.add_argument('-n',
                        '--folder_name',
                        default='pista',
                        type=str, help='name of the folder that the generated collection will be saved (default=pista)')
    parser.add_argument('-he',
                        '--height',
                        default=120,
                        type=int, help='height of the image (default=120)')
    parser.add_argument('-w',
                        '--width',
                        default=160,
                        type=int, help='width of the image (default=160)')
    parser.add_argument('-cam',
                        '--cam_device',
                        default=0,
                        type=int, help='ID of the recording camera (default=0)')

    user_args = parser.parse_args()
    camera = Camera(user_args.height, user_args.width, user_args.cam_device)
    raise_exception = False
    try:
        brick = next(USBInterface.find_bricks(debug=False))
        brick.connect()
    except StopIteration:
        raise_exception = True
    assert raise_exception==0, "No NXT found..." 
    dc = DataCollector(camera, brick, user_args.folder_name)
    dc.generate_data()

if __name__=='__main__':
    main()

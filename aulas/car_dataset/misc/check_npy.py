import argparse
import os
import sys
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
from pathlib import Path

path_current_dir = Path(os.getcwd())
one_level_up = path_current_dir.parents[0]
parent_dir = os.path.join(str(one_level_up), "data_manipulation")
sys.path.append(str(parent_dir))
from util import get_image_and_command, load_dataset         # file located in ../data_manipulation/util.py

def dataset_info(data, labels):
    data_info = "data shape = {}\n".format(data.shape)
    data_info += "data type = {}\n".format(data.dtype)
    data_info += "labels shape = {}\n".format(labels.shape)
    data_info += "labels type = {}\n".format(labels.dtype)
    print(data_info)

def show_sample(data, 
                labels, 
                sample=None, 
                transformation=None, 
                height=120,
                width=160,
                channels=3):
    if sample is None:
        sample = np.random.randint(0, len(labels))
    assert sample <= len(labels), "Provided index is out of bounds for the given dataset"
    img, label = get_image_and_command(data[sample],
                                       labels[sample],
                                       height=height,
                                       width=width,
                                       channels=channels)
    if transformation is None:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mode = "RGB"
    else: # greyscale or binary
        mode = "L"        
    print("Image shape {}".format(img.shape))
    img = Image.fromarray(img, mode=mode)
    img.show()
    print("Action = {} for sample at index {}".format(label, sample))

def main():
    """
    Data Collector class 
    """
    description = "Class for data collection using a camera and a remote controlled robot car connected to USB"
    parser = argparse.ArgumentParser(description=description)
    
    parser.add_argument('data_npy',
                        type=str, help='path to data npy file')
    parser.add_argument('labels_npy',
                        type=str, help='path to labels npy file')
    parser.add_argument('-s',
                        '--sample',
                        default=-1,
                        type=int, help='index of item to be displayed (default=random)')
    transformation_list = """greyscale,
                             binarize"""
    parser.add_argument('-t',
                        '--transformation',
                        default=None,
                        type=str, help="dataset color mode, choose from {} (default=RGB)".format(transformation_list))
    parser.add_argument('-he',
                        '--height',
                        default=120,
                        type=int, help='height of the image (default=120)')
    parser.add_argument('-w',
                        '--width',
                        default=160,
                        type=int, help='width of the image (default=160)')
    parser.add_argument('-c',
                        '--channels',
                        default=3,
                        type=int, help='channels of the image (default=3)')

    user_args = parser.parse_args()
    if user_args.sample == -1:
        user_args.sample = None
    data, labels = load_dataset(user_args.data_npy,
                                user_args.labels_npy)
    dataset_info(data,
                 labels)
    show_sample(data,
                labels,
                sample=user_args.sample,
                transformation=user_args.transformation,
                height=user_args.height,
                width=user_args.width,
                channels=user_args.channels)

if __name__=='__main__':
    main()

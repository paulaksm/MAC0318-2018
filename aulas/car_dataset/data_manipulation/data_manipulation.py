import os
import argparse
import numpy as np
from util import get_image_and_command, get_image, get_flat_shape
from util import load_dataset, save_dataset
import image_manipulation as img_mani  


def extend_dataset_flip_axis(data,
                             labels,
                             height=60,
                             width=80,
                             channels=3):
    """
    Balance and extend dataset
    by generating new images flipping the horizontal
    axis (only applicable to images labeled 'left' or 'right').
    This function is hard-coded, it assumes the following codification:
        - "up": 0
        - "left": 1
        - "right": 2

    :param data: dataset
    :type data: np.array
    :param label: labels
    :type label: np.array
    :param height: image height
    :type height: int
    :param width: image width
    :type width: int
    :param channels: image channels
    :type channels: int
    :return: extended images, extended labels
    :rtype: np.array, np.array
    """
    all_images = []
    all_labels = []
    flat_shape = data.shape[1]
    for i in range(data.shape[0]):
        orig_label = labels[i]
        if orig_label == 0:
            continue
        frame, cmd = get_image_and_command(data[i],
                                           labels[i],
                                           height,
                                           width,
                                           channels)
        if orig_label == 1:
            flip_cmd = 2
        else:
            flip_cmd = 1
        flip = np.flip(frame, axis=1)
        flip = np.array(flip.reshape(flat_shape))
        all_images.append(flip)
        all_labels.append(flip_cmd)
    all_labels = np.array(all_labels).astype('uint8')
    all_labels = all_labels.reshape((all_labels.shape[0], 1))
    extended_images = np.concatenate((data, all_images), axis=0)
    extended_labels = np.concatenate((labels, all_labels), axis=0)
    return extended_images, extended_labels


def transfor_dataset(data,
                     transformation,
                     height=45, # 120
                     width=80, # 160
                     channels=3):
    """
    Create a new dataset by applying a function "transformation"
    available at image_manipulation.
    Returns a new dataset and the new shape of its contents.
    The new shape will have only height and width.

    :param transformation: function
    :type transformation: np.array -> np.array
    :param data: dataset
    :type data: np.array
    :param height: image height
    :type height: int
    :param width: image width
    :type width: int
    :param channels: image channels
    :type channels: int
    :return: transformed dataset, shape
    :rtype: np.array, tuple
    """
    new_dataset = []
    new_shape = ()
    for i in range(data.shape[0]):
        image = get_image(data[i],
                          height,
                          width,
                          channels)
        new_image = transformation(image)
        if new_shape == ():
            new_shape = new_image.shape
        new_image = new_image.reshape(get_flat_shape(new_image))
        new_dataset.append(new_image)
    new_dataset = np.array(new_dataset).astype('uint8')
    return new_dataset, new_shape



def binarize_dataset(data,
                     height=45,
                     width=80,
                     channels=3):
    """
    Create a new dataset by applying the function binarize_image.

    :param data: dataset
    :type data: np.array
    :param height: image height
    :type height: int
    :param width: image width
    :type width: int
    :param channels: image channels
    :type channels: int
    :return: transformed dataset, shape
    :rtype: np.array, tuple
    """
    data, shape = transfor_dataset(data,
                                   img_mani.binarize_image,
                                   height,
                                   width,
                                   channels)
    return data, shape


def gray_dataset(data,
                 height=120,
                 width=160,
                 channels=3):
    """
    Create a new dataset by applying the function grayscale_image.

    :param data: dataset
    :type data: np.array
    :param height: image height
    :type height: int
    :param width: image width
    :type width: int
    :param channels: image channels
    :type channels: int
    :return: transformed dataset, shape
    :rtype: np.array, tuple
    """
    data, shape = transfor_dataset(data,
                                   img_mani.grayscale_image,
                                   height,
                                   width,
                                   channels)
    return data, shape


def green_dataset(data,
                  height=120,
                  width=160,
                  channels=3):
    """
    Create a new dataset by applying the function green_channel.

    :param data: dataset
    :type data: np.array
    :param height: image height
    :type height: int
    :param width: image width
    :type width: int
    :param channels: image channels
    :type channels: int
    :return: transformed dataset, shape
    :rtype: np.array, tuple
    """
    data, shape = transfor_dataset(data,
                                   img_mani.green_channel,
                                   height,
                                   width,
                                   channels)
    return data, shape

def cut_top_bottom_dataset(data,
                           height=120,
                           width=160,
                           channels=3):
    """
    Create a new dataset by applying the function top_bottom_cut.

    :param data: dataset
    :type data: np.array
    :param height: image height
    :type height: int
    :param width: image width
    :type width: int
    :param channels: image channels
    :type channels: int
    :return: transformed dataset, shape
    :rtype: np.array, tuple
    """
    data, shape = transfor_dataset(data,
                                   img_mani.top_bottom_cut,
                                   height,
                                   width,
                                   channels)
    return data, shape


def dataset_augmentation(data, labels, height=120, width=160, channels=3):
    """
    Augment a dataset by inserting a vertical random shadow and
    by bluring with a Gaussian convolution

    :param data: dataset
    :type data: np.array
    :param labels: labels
    :type labels: np.array
    :param width: image width
    :type width: int
    :param height: image height
    :type heights: int
    :param channels: image channels
    :type channels: int
    :return: extended images, extended labels
    :rtype: np.array, np.array
    """
    all_images = []
    all_labels = []
    size = data.shape[0]
    flat_shape = data.shape[1]
    for i in range(size):
        image = get_image(data[i], height, width, channels)
        new_image = img_mani.random_shadow(image)
        new_image = new_image.reshape(flat_shape)
        new_label = labels[i]
        all_images.append(new_image)
        all_labels.append(new_label)
        new_image = img_mani.gaussian_blur(image)
        new_image = new_image.reshape(flat_shape)
        all_images.append(new_image)
        all_labels.append(new_label)
    all_labels = np.array(all_labels).astype('uint8')
    all_labels = all_labels.reshape((all_labels.shape[0], 1))
    extended_images = np.concatenate((data, all_images), axis=0)
    extended_labels = np.concatenate((labels, all_labels), axis=0)
    return extended_images, extended_labels


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('data_path',
                        type=str, help='path to current data')
    parser.add_argument('labels_path',
                        type=str, help='path to current labels')
    parser.add_argument('new_data_folder_path',
                        type=str, help='path to data and labels to be saved')  
    parser.add_argument('dataset_name',
                        default='dataset', 
                        type=str, help='name for dataset. (Default) dataset')  
    parser.add_argument("-he",
                        "--image_height",
                        type=int,
                        default=120,
                        help="original height number (default=120)")
    parser.add_argument("-w",
                        "--image_width",
                        type=int,
                        default=160,
                        help="original width number (default=160)")
    parser.add_argument("-c",
                        "--image_channels",
                        type=int,
                        default=3,
                        help="number of channels (default=3)")
    parser.add_argument('-b',
                        '--binarize',
                        action='store_true',
                        help='flag to binarize the dataset (default=False)')
    parser.add_argument('-ctb',
                        '--cut_top_bottom',
                        action='store_true',
                        help='flag to cut the top and bottom of the dataset images, resizing to their original shape (default=False)')
    parser.add_argument('-g',
                        '--grayscale',
                        action='store_true',
                        help='flag to grayscale the dataset (default=False)')
    parser.add_argument('-gr',
                        '--green_channel',
                        action='store_true',
                        help='flag to create the dataset with only its green channel (default=False)')
    parser.add_argument('-x',
                        '--extend_dataset',
                        action='store_true',
                        help='flag to extend the dataset by flipping its horizontal axis in left/right labeled images (default=False)')
    user_args = parser.parse_args()
    args_list = [user_args.binarize, user_args.green_channel, user_args.grayscale]
    assert sum(args_list) <= 1, "Multiple flags selected for image manipulaiton"
    data, labels = load_dataset(user_args.data_path,
                                user_args.labels_path)
    print("After load: data shape {}, labels shape {}".format(data.shape, labels.shape))
    if user_args.extend_dataset:
        data, labels = extend_dataset_flip_axis(data,
                                                labels,
                                                height=user_args.image_height,
                                                width=user_args.image_width,
                                                channels=user_args.image_channels)
        print("After extension: data shape {}, labels shape {}".format(data.shape, labels.shape))
    data_shape = (user_args.image_height,
                  user_args.image_width,
                  user_args.image_channels)
    if user_args.cut_top_bottom:
        data, data_shape = cut_top_bottom_dataset(data,
                                                  height=user_args.image_height,
                                                  width=user_args.image_width,
                                                  channels=user_args.image_channels)
    if user_args.binarize:
        data, data_shape = binarize_dataset(data,
                                            height=user_args.image_height,
                                            width=user_args.image_width,
                                            channels=user_args.image_channels)
    if user_args.grayscale:
        data, data_shape = gray_dataset(data,
                                        height=user_args.image_height,
                                        width=user_args.image_width,
                                        channels=user_args.image_channels)
    if user_args.green_channel:
        data, data_shape = green_dataset(data,
                                         height=user_args.image_height,
                                         width=user_args.image_width,
                                         channels=user_args.image_channels)
    #data, labels = dataset_augmentation(data, labels)
    if user_args.cut_top_bottom or user_args.binarize or user_args.green_channel or user_args.grayscale:
        print("After transformation: data shape {}, labels shape {}".format(data.shape, labels.shape))
    save_dataset(data,
                 labels,
                 user_args.new_data_folder_path,
                 data_shape,
                 user_args.dataset_name)


if __name__ == '__main__':
    main()

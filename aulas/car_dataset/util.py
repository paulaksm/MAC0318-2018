import time
import numpy as np
import matplotlib.pyplot as plt
import argparse

dict_command2int = {"up": 0, "left": 1, "right": 2}
dict_int2command = {i[1]:i[0] for i in dict_command2int.items()}

def get_date():
    return time.strftime("%Y-%m-%d-%H-%M-%S")

# def command2int(command):
#     return dict_command2int[command]

# def int2command(label):
#     return dict_int2command[label]

def plot_histogram(label_path):
    """
    Plot dataset histogram 

    :type label_path: str 
    :param label_path: absolute path to labels.npy  
    """
    labels = np.load(label_path)
    bins = len(np.unique(labels))
    data_hist = plt.hist(labels, 
                         bins=np.arange(bins+1) - 0.5, 
                         edgecolor='black')        
    axes = plt.gca()  # Get Current Axes
    axes.set_ylim([0, len(labels)])
    plt.title("Histogram of {} images".format(len(labels)))
    plt.xticks(np.arange(bins+1), 
               np.unique(labels))
    plt.xlabel("Label")
    plt.ylabel("Frequency")
    for i in range(bins):
        plt.text(data_hist[1][i] + 0.1,
                 data_hist[0][i] + (data_hist[0][i] * 0.2),
                 str(int(data_hist[0][i])))
    plt.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('labels_path',
                        type=str, help='path to labels')
    user_args = parser.parse_args()
    plot_histogram(user_args.labels_path)

if __name__=="__main__":
    main()

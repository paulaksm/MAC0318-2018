import math
import numpy as np
import matplotlib.pyplot as plt
from pandas_ml import ConfusionMatrix

def plot_histogram(labels):
    """
    Plot dataset histogram

    """
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

    plt.plot()

def plot_img_grid(data, 
                  labels, 
                  max_cols=1):
    max_rows = math.ceil(len(labels) / max_cols)
    for i in range(len(labels)):
        plt.subplot(max_rows, 
                    max_cols, 
                    i + 1)
        array_imshow(data[i],
                     labels[i], 
                     grid=False, 
                     fontsize=10)
    plt.tight_layout()
    
def array_imshow(img_array, 
                 label=None, 
                 shape=(28,28), 
                 grid=False, 
                 fontsize=18):
    img = array2img(img_array, 
                    shape=shape)
    plt.xlabel("Digit: {}".format(label), 
               fontsize=fontsize)
    plt.grid(grid)
    plt.imshow(img, 
               cmap='binary')

def array2img(img_array, 
              shape=(28,28)):
    return np.reshape(img_array, shape)

def get_samples(data, 
                labels, 
                size=3):
    idx_samples = np.random.randint(low=0, 
                                    high=len(labels),
                                    size=size)
    sample_data = np.array([data[idx] for idx in idx_samples])
    sample_labels = np.array([labels[idx] for idx in idx_samples])
    return sample_data, sample_labels

def plot_confusion_matrix_metrics(true_labels=None, 
                                  predicted_labels=None, 
                                  normalized=False):
    cm = ConfusionMatrix(true_labels, 
                         predicted_labels)
    cm.plot(cmap='GnBu', 
            normalized=normalized)
    ax = plt.gca()
    label_dict = {"True": 1, "False": 0}
    str_labels = [ 'Digit {}'.format(label_dict.get(i.get_text(), i)) for i in ax.get_xticklabels() ] 
    ax.set_xticklabels(str_labels, 
                       rotation=0, 
                       horizontalalignment='center')
    ax.set_yticklabels(str_labels)
    cm_array = cm.to_array()
    width, height = cm_array.shape
    for x in range(width):
        for y in range(height):
            plt.annotate(str(cm_array[x][y]), 
                         xy=(y, x), 
                         horizontalalignment='center',
                         verticalalignment='center')
    plt.show()
    print(cm)
    print("===================================================")
    print("Evaluation metrics:")
    cm.print_stats()

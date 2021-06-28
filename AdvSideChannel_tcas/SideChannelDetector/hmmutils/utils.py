import os
import sys
sys.path.append(os.getcwd())

import numpy as np
from scipy.signal import spectrogram
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score



NUM_WORKERS = 32
WIN_SIZE = 8

def split(sample, win_size):
    sample = sample[:len(sample)//win_size*win_size]
    return sample.reshape(-1, win_size)

def plot_roc(scores_neg, scores_pos):
    scores_all = scores_neg + scores_pos
    labels_all = len(scores_neg) * [0] + len(scores_pos) * [1]
    fpr, tpr, ths = roc_curve(labels_all, scores_all, pos_label=0)
    plt.plot(fpr, tpr)

def compute_spectrogram_scipy(signal, win_size):
    spct = spectrogram(signal, nperseg=win_size, noverlap=win_size//2)
    return spct[2]

def load_data(dataset_dir, feature_choice='time', win_size=4):
    class_names = os.listdir(dataset_dir)
    data = {}
    for cname in class_names:
        data_class = []
        sample_names = os.listdir(os.path.join(dataset_dir, cname))
        for i in range(len(sample_names)):
            sample = np.load(os.path.join(dataset_dir, cname, sample_names[i]), encoding='latin1', allow_pickle=True).item()['trace']
            # ipdb.set_trace()
            if feature_choice == 'time':
                sample = split(sample, win_size)
            elif feature_choice == 'fft':
                sample = compute_spectrogram_scipy(sample, win_size).T
            else:
                print('wrong feature choice specified!')
                return 1
            # data_len.append(len(sample['trace']))
            # data_text.append(sample['text'])
            # data_name.append(os.path.join(cname, sample_names[i]))
            data_class.append(sample)
        # data_class_concat = np.concatenate(data_class, axis=0)
        data[cname] = data_class
    
    return data

def concat_data(data):
    sequence = []
    ll = []
    for _, value in data.items():
        sequence.append(value[0])
        ll.append(value[0].shape[0])
    sequence = np.concatenate(sequence, axis=0)
    # ipdb.set_trace()
    return sequence, ll
 
def fit_model(model, sample, key):
    model.fit(sample)
    return key, model

def get_prediction(models, sample, label):
    scores = {}
    for key, model in models.items():
        s = model.score(sample)
        scores[key] = s
    # ipdb.set_trace()
    predicted = max(scores, key=scores.get)
    return label == predicted

def get_score(models, sample):
    scores = {}
    for key, model in models.items():
        s = model.score(sample)
        scores[key] = s
    score_max = max(scores.values())
    return score_max


    return model.score(sample)

def hmm_forward(models, sample, label):
    scores = {}
    for key, model in models.items():
        s = model.score(sample)
        scores[key] = s
    return scores, label
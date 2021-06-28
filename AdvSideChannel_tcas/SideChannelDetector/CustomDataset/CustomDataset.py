import os
import numpy as np

from torch.utils.data.dataset import Dataset
import torch
import torch.nn as nn
from torchaudio.transforms import Spectrogram

import ipdb


def custom_collate(batch):
    # images = [item[0] for item in batch]
    # targets = [item[1] for item in batch]
    # targets = torch.LongTensor(targets)
    # return [images, targets]

    transposed = list(zip(*batch))
    images = transposed[0]
    # targets = torch.stack(transposed[1], 0, out=None)
    targets = torch.LongTensor(transposed[1])
    return [images, targets]

def sort_batch(batch):
    batch_length = list(map(len, batch))
    perm_idx = sorted(list(range(len(batch_length))), key=lambda k: batch_length[k], reverse=True)
    batch_sorted = [batch[perm_idx[i]] for i in range(len(batch_length))]
    return batch_sorted, perm_idx

def normalize(signal):
    return (signal - signal.mean()) / signal.std()


def default_loader(path):
    return np.load(path, encoding='latin1', allow_pickle=True).item()['trace']
        
def make_dataset(dir, class_to_idx):
    samples = []
    # dir = os.path.expanduser(dir)
    for target in sorted(class_to_idx.keys()):
        d = os.path.join(dir, target)
        if not os.path.isdir(d):
            continue
        for root, _, fnames in sorted(os.walk(d)):
            for fname in sorted(fnames):
                path = os.path.join(root, fname)
                item = (path, class_to_idx[target])
                samples.append(item)
    return samples

def pad(sample, max_len):
    sample_padded = np.zeros(max_len)
    if len(sample) <= max_len:
        sample_padded[:len(sample)] = sample
        return sample_padded
    if len(sample) > max_len:
        return sample[:max_len]

def split(sample, win_size):
    sample = sample[:len(sample)//win_size*win_size]
    return sample.reshape(-1, win_size)

def compute_spectrogram(signal, win_size):
    spectrogram = Spectrogram(n_fft=win_size, win_length=win_size, power=2, normalized=True)
    spct = spectrogram(signal)
    return spct.T



class SideChannelDetector(Dataset):
    def __init__(self, root, max_len, win_size, loader=default_loader, feature_choice='time'):
        self.root = os.path.expanduser(root)
        self.max_len = max_len
        self.win_size = win_size
        self.feature_choice = feature_choice
        classes, class_to_idx = self._find_classes(self.root)
        samples = make_dataset(self.root, class_to_idx)
        self.loader = loader
        self.classes = classes
        self.class_to_idx = class_to_idx
        self.samples = samples
        self.targets = [s[1] for s in samples]

    def __getitem__(self, index):
        path, target = self.samples[index]
        sample = self.loader(path)
        sample = normalize(sample)
        # sample = pad(sample, self.max_len)
        sample = torch.Tensor(sample)
        if self.feature_choice == 'time':
            sample = split(sample, self.win_size)
        elif self.feature_choice == 'fft':
            sample = compute_spectrogram(sample, self.win_size)
        else:
            print('invalid feature choice!')
        # ipdb.set_trace()
        return sample, target

    def __len__(self):
        return len(self.samples)
    
    def _find_classes(self, dir):
        classes = [d.name for d in os.scandir(dir) if d.is_dir()]
        classes.sort()
        class_to_idx = {classes[i]: i for i in range(len(classes))}
        return classes, class_to_idx

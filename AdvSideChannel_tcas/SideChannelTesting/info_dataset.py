import numpy as np 
import argparse
import matplotlib.pyplot as plt
import matplotlib
from tqdm import tqdm

import os
from itertools import combinations

from dtw import dtw

def plot_dir(dir, dest):
    if not os.path.exists(dest):
        os.mkdir(dest)
    sample_names = os.listdir(dir)
    plot = plt.figure(figsize=(16, 9))
    for sname in sample_names:
        sample = np.load(os.path.join(dir, sname), allow_pickle=True).item()['trace']
        plt.plot(sample)
    # mng = plt.get_current_fig_manager()
    # mng.window.state('zoomed')
    plot.savefig(os.path.join(dest, dir.split('\\')[-1]+'.png'))
    plt.close()

def plot_dir_interactive(dir):
    sample_names = os.listdir(dir)
    plot = plt.figure(figsize=(16, 9))
    for sname in sample_names:
        sample = np.load(os.path.join(dir, sname), allow_pickle=True).item()['trace']
        plt.plot(sample)
    

def plot_sample(name):
    sample = np.load(name, allow_pickle=True).item()['trace']
    plt.plot(sample)

def plot_compare(data, dest):
    if not os.path.exists(dest):
        os.mkdir(dest)
    C = list(combinations(list(range(len(data))), 2))
    for pair in tqdm(C):
        plot = plt.figure(figsize=(16, 9))
        plt.plot(data[pair[0]])
        plt.plot(data[pair[1]]) 
        plot.savefig(os.path.join(dest, str(pair[0])+'_'+str(pair[1])+'.png'))
        plt.close()

def plot_pair(s1, s2):
    plt.plot(s1)
    plt.plot(s2)
    plt.show()

def truncate(trace, trigger):
    return trace[np.where(trigger > 2.5)]

def load_dir(dir):
    sample_names = os.listdir(dir)
    data = []
    for sname in sample_names:
        sample = np.load(os.path.join(dir, sname), allow_pickle=True).item()['trace']
        data.append(sample)
    return data

def check_length(ll):
    for i in range(1, ll):
        traces = load_dir(os.path.join(arg.dataset_dir, 'test0000'+'{0:0=2d}'.format(i)))
        print('test0000'+'{0:0=2d}:'.format(i), end=" ")
        for t in traces:
            print(len(t), end=" ")
        print('\n')
    
def dtw_path(s1, s2):
    l2_norm = l2_norm = lambda x, y: (x - y) ** 2
    dist, cost_matrix, acc_cost_matrix, path = dtw(s1, s2, dist=l2_norm)
    plt.imshow(acc_cost_matrix.T, origin='lower', cmap='gray', interpolation='nearest')
    plt.plot(path[0], path[1], 'w')
    plt.show()

def dtw_trace(s1, s2):
    l2_norm = l2_norm = lambda x, y: (x - y) ** 2
    dist, cost_matrix, acc_cost_matrix, path = dtw(s1, s2, dist=l2_norm)
    plt.plot(s1[path[0]])
    plt.plot(s2[path[1]])
    plt.show()

def load_dir(dir):
    data = []
    filenames = os.listdir(dir)
    for name in filenames:
        sample = np.load(os.path.join(dir, name), encoding='latin1', allow_pickle=True).item()['trace']
        data.append(sample)
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Concatenate small data files')
    parser.add_argument('-d', '--dataset-dir', type=str, help='Specify the dataset folder')
    parser.add_argument('--pc', type=bool, default=False, help='Specify the dataset folder')
    parser.add_argument('--pd', type=bool, default=False, help='Specify the dataset folder')
    arg = parser.parse_args()

    # data = np.load(arg.input, encoding='latin1', allow_pickle=True).item()

    # matplotlib.use('Agg')

    class_names = os.listdir(arg.dataset_dir)

    data_len = []
    data = []
    data_text = []
    data_name = []
    for cname in class_names:
        # load one example for each class
        filenames = os.listdir(os.path.join(arg.dataset_dir, cname))
        data.append(np.load(os.path.join(arg.dataset_dir, cname, filenames[0]), encoding='latin1', allow_pickle=True).item()['trace'])

        sample_names = os.listdir(os.path.join(arg.dataset_dir, cname))
        for i in range(len(sample_names)):
            sample = np.load(os.path.join(arg.dataset_dir, cname, sample_names[i]), encoding='latin1', allow_pickle=True).item()
            data_len.append(len(sample['trace']))
            data_text.append(sample['text'])
            data_name.append(os.path.join(cname, sample_names[i]))
    
    data_info = list(zip(data_name, data_text, data_len))
    # for entry in data_info:
    #     print(entry)

    info = list(zip(*data_info))
    print('max len is: {}'.format(max(info[2])))

    # plot singals in each dir
    if arg.pd:
        for cname in tqdm(class_names):
            plot_dir(os.path.join(arg.dataset_dir, cname), 'plot_dir')
    
    if arg.pc:
        plot_compare(data, 'plot')
    # print(data_len)
    # print(max(data_len))

    # data1 = load_dir('attack_input/test000001.smt2')
    # data2 = load_dir('attack_input/test000002.smt2')
    # data3 = load_dir('attack_input/test000003.smt2')
    # plot_pair(data1[0], data2[0])

    # data1 = load_dir('../SideChannelTesting/train_cw0/test000001.smt2')
    # data2 = load_dir('../SideChannelTesting/train_cw1/test000001.smt2')
    # data3 = load_dir('SideChannelTesting/train/test000001.smt2')
    # plot_pair(data1[0], data2[0])

    
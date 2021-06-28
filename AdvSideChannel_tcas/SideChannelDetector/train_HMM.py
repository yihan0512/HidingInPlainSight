import argparse
import os
import sys
sys.path.append(os.getcwd())

from tqdm import tqdm

from hmmlearn.hmm import GaussianHMM, GMMHMM
import numpy as np
from scipy.signal import spectrogram
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score

from CustomDataset.CustomDataset import split
from CheckpointWriter.CheckpointWriter_hmm import CheckpointWriter

import ipdb
import pickle

from multiprocessing import Pool

from hmmutils import *

NUM_WORKERS = 32
WIN_SIZE = 8

def plot_roc(scores_neg, scores_pos):
    scores_all = scores_neg + scores_pos
    labels_all = len(scores_neg) * [0] + len(scores_pos) * [1]
    fpr, tpr, ths = roc_curve(labels_all, scores_all, pos_label=0)
    auc = roc_auc_score(labels_all, scores_all)
    plt.plot(fpr, tpr)
    return auc

def compute_spectrogram_scipy(signal, win_size):
    # spct = spectrogram(signal, nperseg=win_size, noverlap=win_size//2)
    spct = spectrogram(signal, nperseg=win_size, noverlap=0)
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

def test_model(models, test_data):
    count = 0
    correct = 0
    results = []
    for key, value in tqdm(test_data.items()):
        for signal in value:
            res = get_prediction(models, signal, key)
            results.append(res)
            count += 1
            correct += res
        ipdb.set_trace()
    print('accuracy is {}%'.format(correct/count*100))

def test_model_parallel(models, test_data):
    pool = Pool(NUM_WORKERS)

    samples = []
    for key, value in test_data.items():
        for signal in value:
            samples.append([signal, key])
    
    jobs = []
    for sample in samples:
        job = pool.apply_async(hmm_forward, (models, sample[0], sample[1]))
        jobs.append(job)
        
    outputs = []
    for job in tqdm(jobs):
        output = job.get()
        outputs.append(output)
    
    results = []
    for output in outputs:
        predicted = max(output[0], key=output[0].get)
        results.append(predicted==output[1])
    
    accu = sum(results)/len(samples)*100
    print('Accuracy is {}%'.format(accu))
    return accu
    
    # return results

def test_detector(models, benign_program, malicious_programs, feature_choice='time', win_size=8):    
    # get scores for benign samples
    samples = []
    data_dir = os.path.join('../', 'SideChannelTesting', 'test')
    data_dir = os.path.join('../../', 'AdvSideChannel_'+benign_program, 'SideChannelTesting', 'test')
    benign_data = load_data(data_dir, feature_choice, win_size=win_size)
    for key, value in benign_data.items():
        for signal in value:
            samples.append(signal)
    
    scores_benign = []
    pool = Pool(NUM_WORKERS)
    jobs = []
    for sample in samples:
        job = pool.apply_async(get_score, (models, sample))
        jobs.append(job)
    
    for job in tqdm(jobs):
        res = job.get()
        scores_benign.append(res)


    # get scores for malicious samples
    samples = []
    for program in malicious_programs:
        test_data_dir = os.path.join('../../', 'AdvSideChannel_'+program, 'SideChannelTesting', 'test')
        test_data = load_data(test_data_dir, feature_choice=feature_choice, win_size=win_size)
        for key, value in test_data.items():
            for signal in value:
                samples.append(signal)

    scores_malicious = []
    pool = Pool(NUM_WORKERS)
    jobs = []
    for sample in samples:
        job = pool.apply_async(get_score, (models, sample))
        jobs.append(job)
    
    for job in tqdm(jobs):
        res = job.get()
        scores_malicious.append(res)

    return scores_benign, scores_malicious

# def train_single_hmm():
#     train_data = load_data('../SideChannelTesting/train', win_size=WIN_SIZE)
#     # test_data = load_data('../SideChannelTesting/test', win_size=WIN_SIZE)
#     train_seq, train_len = concat_data(train_data)
#     # ipdb.set_trace()
#     model = GMMHMM(n_components=5, n_mix=1, covariance_type='diag', n_iter=200, verbose=True)
#     model.fit(train_seq, train_len)


#     # save the model
#     with open('hmm_single.pth', 'wb') as handle:
#         pickle.dump(model, handle, protocol=pickle.HIGHEST_PROTOCOL)

#     # test model
#     samples = []
#     scores = {}
#     programs = ['tcas', 'dijkstra', 'pid', 'kalman', 'particle']
#     for program in programs:
#         scores_program = []
#         test_data_dir = os.path.join('../../', 'AdvSideChannel_'+program, 'SideChannelTesting', 'test')
#         test_data = load_data(test_data_dir, win_size=WIN_SIZE)
#         for key, value in tqdm(test_data.items()):
#             for signal in value:
#         #         s = model.score(signal)
#         #         scores_program.append(s)
#         # scores[program] = scores_program
#                 samples.append(signal)

#     scores = []
#     pool = Pool(NUM_WORKERS)
#     jobs = []
#     for sample in samples:
#         job = pool.apply_async(get_score, (model, sample))
#         jobs.append(job)
    
#     for job in jobs:
#         res = job.get()
#         scores.append(res)


#     ipdb.set_trace()
#     return scores
    
def train_multiple_hmm():
    train_data = load_data('data/train', win_size=WIN_SIZE)
    test_data = load_data('data/test', win_size=WIN_SIZE)
    # train_data_fft = load_data('data/train', feature_choice='fft', win_size=8)
    models = {}
    for index, (key, value) in enumerate(train_data.items()):
        # ipdb.set_trace()
        print('{}: training hmm for {}...'.format(index, key))
        model = GMMHMM(n_components=10, n_mix=1, covariance_type='diag', n_iter=200, verbose=True)
        key, model = fit_model(model, value[0], key)
        models[key] = model


    # save the model
    with open('hmm.pth', 'wb') as handle:
        pickle.dump(models, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
    # load the model
    # with open('hmm.pth', 'rb') as handle:
    #     models = pickle.load(handle)

    # iter over all test data
    # test_model(models, test_data)
    for key, value in tqdm(test_data.items()):
        scores = {}
        for key1, model in models.items():
            s = model.score(np.concatenate(value, axis=0))
            scores[key1] = s
        ipdb.set_trace()

def train_multiple_hmm_parallel():
    train_data = load_data('../SideChannelTesting/train', win_size=WIN_SIZE)
    test_data = load_data('../SideChannelTesting/test', win_size=WIN_SIZE)
    # train_data_fft = load_data('data/train', feature_choice='fft', win_size=8)

    pool = Pool(NUM_WORKERS)
    jobs = []
    models = {}
    for index, (key, value) in enumerate(train_data.items()):
        # ipdb.set_trace()
        model = GMMHMM(n_components=10, n_mix=1, covariance_type='diag', n_iter=200, verbose=False)
        # model = GMMHMM(n_components=20, n_mix=1, covariance_type='diag', n_iter=200, verbose=False)
        job = pool.apply_async(fit_model, (model, np.concatenate(value, axis=0), key))
        jobs.append(job)
    
    for job in tqdm(jobs):
        key, model = job.get()
        models[key] = model
    
    # save the model
    with open('hmm.pth', 'wb') as handle:
        pickle.dump(models, handle, protocol=pickle.HIGHEST_PROTOCOL)
    model_specs = {}
    model_specs['base'] = {}
    model_specs['base']['win_size'] = WIN_SIZE
    model_specs['base']['n_components'] = n_components 
    model_specs['base']['n_mix'] = n_mix
    model_specs['base']['num_paths'] = 24
    model_specs['base']['feature_choice'] = feature_choice
    checkpoint = CheckpointWriter(os.path.join('checkpoints', expr_log), model_specs)
        
    # load the model
    # with open('hmm.pth', 'rb') as handle:
    #     models = pickle.load(handle)

    # test model
    results = test_model_parallel(models, test_data)

    scores_benign, scores_malicious = test_detector(models, ['dijkstra', 'pid', 'kalman', 'particle'])
    plt.plot(scores_bengin+scores_malicious)
    plt.savefig('scores.png')

def inference_multiple_hmm():
    # load test data
    # train_data = load_data('../SideChannelTesting/train', win_size=WIN_SIZE)
    # test_data = load_data('../SideChannelTesting/test', win_size=WIN_SIZE)

    # load the model
    with open('checkpoints/hmm_time/best_val_snapshot.ckpt', 'rb') as handle:
        models = pickle.load(handle)

    # test_model_parallel(models, test_data)

    # for key, value in tqdm(test_data.items()):
    #     scores = {}
    #     for key1, model in models.items():
    #         s = model.score(np.concatenate(value, axis=0))
    #         scores[key1] = s
    #     ipdb.set_trace()

    scores_benign, scores_malicious = test_detector(models, ['dijkstra', 'pid', 'kalman', 'particle'])
    plt.figure()
    plot_roc(scores_benign, scores_malicious)
    plt.savefig('roc.png')

# def train_second_model():
#     train_data = load_data('data/train', win_size=WIN_SIZE)
#     test_data = load_data('data/test', win_size=WIN_SIZE)

#     key = 'test000005.smt2'
#     model = GMMHMM(n_components=20, n_mix=1, covariance_type='diag', n_iter=200, verbose=True)
#     model.fit(train_data[key][0])
#     models = {}
#     models[key] = model
    
#     test_model(models, train_data)

#             #         s = model.score(signal)
#         #         scores_program.append(s)
#         # scores[program] = scores_program


if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser(description='training BiRNNattn')
    parser.add_argument('-w', '--window', default=8, type=int, help='window size')
    parser.add_argument('--n-components', default=30, type=int, help='number of states')
    parser.add_argument('--n-mix', default=1, type=int, help='number of mixture')
    parser.add_argument('--training', default='../SideChannelTesting/train', type=str, help='Specify training dir')
    parser.add_argument('--testing', default='../SideChannelTesting/test', type=str, help='Specify testing dir')
    parser.add_argument('-l', '--log', type=str, help='Specify expr dir')
    parser.add_argument('-f', '--feature', default='time', type=str, help='Specify feature choice')
    args = parser.parse_args()

    win_size = args.window
    n_components = args.n_components
    n_mix = args.n_mix
    train_folder = args.training
    test_folder = args.testing
    expr_log = args.log
    feature_choice = args.feature

    train_data = load_data(train_folder, feature_choice=feature_choice, win_size=win_size)
    test_data = load_data(test_folder, feature_choice=feature_choice, win_size=win_size)
    # train_data_fft = load_data('data/train', feature_choice='fft', win_size=8)

    pool = Pool(NUM_WORKERS)
    jobs = []
    models = {}
    for index, (key, value) in enumerate(train_data.items()):
        # ipdb.set_trace()
        model = GMMHMM(n_components=n_components, n_mix=n_mix, covariance_type='diag', n_iter=200, verbose=False)
        # model = GMMHMM(n_components=20, n_mix=1, covariance_type='diag', n_iter=200, verbose=False)
        job = pool.apply_async(fit_model, (model, np.concatenate(value, axis=0), key))
        jobs.append(job)
    
    for job in tqdm(jobs):
        key, model = job.get()
        models[key] = model
    
    pool.close()
    pool.join()
    
    # init checkpoint writer
    model_specs = {}
    model_specs['base'] = {}
    model_specs['base']['win_size'] = win_size
    model_specs['base']['n_components'] = n_components 
    model_specs['base']['n_mix'] = n_mix
    model_specs['base']['num_paths'] = 24
    model_specs['base']['feature_choice'] = feature_choice
    checkpoint = CheckpointWriter(os.path.join('checkpoints', expr_log), model_specs)
        

    # test model
    accuracy_val = test_model_parallel(models, test_data)

    # test detector
    # scores_benign, scores_malicious = test_detector(models, 'tcas', ['dijkstra', 'pid', 'kalman', 'particle'], feature_choice, win_size)
    scores_benign, scores_malicious = test_detector(models, 'tcas', ['dijkstra', 'pid'], feature_choice, win_size)
    plt.figure()
    plt.plot(scores_benign+scores_malicious)
    plt.savefig('scores.png')
    plt.close()
    plt.figure()
    auc = plot_roc(scores_benign, scores_malicious)
    print('AUC is {}'.format(auc))
    plt.savefig('roc.png')
    plt.close()

    # save the model
    likelihoods = []
    for key, model in models.items():
        likelihoods.append(model.monitor_.history[-1])
    
    likelihood_val = sum(likelihoods) / len(likelihoods)


    checkpoint.save(models, accuracy_val, likelihood_val)
    

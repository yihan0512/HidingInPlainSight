import numpy as np 
import matplotlib.pyplot as plt

import os
import argparse

from tqdm import trange

def parseFile(filename):
    with open(filename, 'r') as f:
        text = f.read()
    testcases = text.split('File')[1:]
    testcases_new = dict()
    for testcase in testcases:
        key = testcase.split('smt2\n')[0][2:-1]
        value = testcase.split('smt2\n')[1].split('\n')[:-1]
        value_new = []
        for tc in value:
            try:
                text = tc.split('\t')[1]
            except:
                print(testcase.split('smt2\n'))
            value_new.append(text)
        testcases_new[key] = value_new
    return testcases_new

def plotSave(signal, save_dir, title):
    plt.plot(signal.T)
    plt.ylim([0, 1.1])
    plt.title(title)
    plt.savefig(save_dir)
    plt.close()

def plotAxvline(signal, testcase_count):
    plt.plot(signal.T)
    for i in range(50):
        plt.axvline(sum(testcase_count[:i])*10)
    plt.show()


def getScorePath(score, num_list, index):
    if index == 0:
        start = 0
    else:
        start = sum(num_list[:index]) * 10
    end = sum(num_list[:index+1]) * 10
    return score[:, start:end]

if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser(description='training BiRNNattn')
    parser.add_argument('--data', default='results_benign', type=str, help='Specify results dir')
    parser.add_argument('--mode', default='interactive', type=str, help='plot all testcases or path by path')
    arg = parser.parse_args()

    seed_dir = 'C:\\Users\\char8\\Documents\\Zahra\\SideChannelTesting_Zahra\\seed\\seed_dijkstra_multiple_utf8.txt'

    # results_dir = 'results_benign'
    # results_plot_dir = 'results_benign_plot'
    mode = arg.mode
    results_dir = arg.data
    plot_dir = results_dir+'_plot'
    results_names = os.listdir(results_dir) 

    if mode == 'all':
        if not os.path.exists(plot_dir):
            os.mkdir(plot_dir)
        for result in results_names:
            [score, predict, label] = np.load(os.path.join(results_dir, result), allow_pickle=True)
            plt.figure(figsize=(16, 9)) 
            plt.plot(score)
            # plt.plot(label.numpy()/24)
            # plt.plot(predict.numpy()/24)
            plt.ylim([0, 1.1])
            # plt.plot(predict.numpy()/50)
            plt.title(score.mean())
            plt.savefig(os.path.join(plot_dir, result.split('.')[0]))
            plt.close()
    elif mode == 'path':
        path_dir = plot_dir + '_path'
        if not os.path.exists(plot_dir+'_path'):
            os.mkdir(plot_dir+'_path')

        # load score
        score_all = []
        for result in results_names:
            [score, predicted, label] = np.load(os.path.join(results_dir, result), allow_pickle=True)
            score_all.append(score)
        score_all = np.array(score_all)

        # load path info
        testcase = parseFile(seed_dir)
        testcase_name = list(testcase.keys())
        testcase_name.sort()
        testcase_num = []
        for name in testcase_name:
            testcase_num.append(len(testcase[name]))

        for i in trange(50):
            score_path = getScorePath(score_all, testcase_num, i)
            plotSave(score_path, os.path.join(plot_dir+'_path', 'path'+str(i)), testcase_name[i])

        # plotAxvline(score_all[:5], testcase_num)
        '''
        m = score_all.mean(axis=1)
        s = score_all.std(axis=1)
        plt.errorbar(np.arange(len(m)), m, yerr=s, fmt='o'), plt.xlabel('random injections'), plt.ylabel('mean and std of scores across the path'), plt.show()
        '''


    elif mode == 'testcase':
        testcase_dir = plot_dir + '_testcase'
        if not os.path.exists(testcase_dir):
            os.mkdir(testcase_dir)

        # load score
        score_all = []
        for result in results_names:
            [score, predicted, label] = np.load(os.path.join(results_dir, result), allow_pickle=True)
            score_all.append(score)
        score_all = np.array(score_all)

        for i in trange(0, score_all.shape[1], 10):
            plotSave(score_all[:, i:i+10], os.path.join(testcase_dir, 'path'+str(label[i])+'testcase'+str(i)), str(i))
    
    elif mode == 'error_graph':
        path_dir = plot_dir + '_path'
        if not os.path.exists(plot_dir+'_path'):
            os.mkdir(plot_dir+'_path')

        # load score
        score_all = []
        for result in results_names:
            [score, label, predict] = np.load(os.path.join(results_dir, result), allow_pickle=True)
            score_all.append(score)
        score_all = np.array(score_all)

        # load path info
        testcase = parseFile(seed_dir)
        testcase_name = list(testcase.keys())
        testcase_name.sort()
        testcase_num = []
        for name in testcase_name:
            testcase_num.append(len(testcase[name]))

        m = score_all.mean(axis=1)
        s = score_all.std(axis=1)
        plt.errorbar(np.arange(len(m)), m, yerr=s, fmt='o'), plt.xlabel('random injections'), plt.ylabel('mean and std of scores across the path'), plt.show()


    else:
        score_all = []
        for result in results_names:
            [score, label, predict] = np.load(os.path.join(results_dir, result), allow_pickle=True)
            score_all.append(score)
        score_all = np.array(score_all)
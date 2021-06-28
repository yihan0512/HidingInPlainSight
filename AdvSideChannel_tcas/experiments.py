from SideChannelDetector import parse_s
from SideChannelDetector import inference_HMM
from SideChannelDetector import inference_Detector
from SideChannelTesting import capture_arm_cw
import subprocess

import os
import sys
import shutil
from time import time
from random import randint
from random import choice
import json

import numpy as np
import matplotlib.pyplot as plt

from SideChannelDetector import mal_list

import ipdb
import argparse

from sklearn.metrics import roc_curve, roc_auc_score

PROJECT_DIR = os.getcwd()
SOURCE_DIR = os.path.join(PROJECT_DIR, 'firmware', 'simpleserial-main')

def random_combination(s1, s2):
    ind1 = 0
    ind2 = 0
    sn = ''
    while len(sn) < len(s1) + len(s2):
        side = randint(0, 1)
        if side:
            try:
                sn += s1[ind1]
                ind1 += 1
            except:
                pass
        else:
            try:
                sn += s2[ind2]
                ind2 += 1
            except:
                pass
    return sn

def random_injection(can_loc):
    rand_inj = []
    for item in can_loc:
        rand_inj.append(choice(item))
    return rand_inj

def combination_whole(s1, s2, slot):
    return ''.join(s1[:slot] + s2 + s1[slot:])

def program_reset():
    os.chdir(SOURCE_DIR)
    subprocess.call(['cp', 'simpleserial-main_benign.s', 'simpleserial-main.s'])
    output = subprocess.run(["sh", "windows_make_binary.sh", "main"], capture_output=True)
    if output.stderr != b'':
        print('build failed with {}'.format(output.stderr))
    else:
        output = subprocess.run(["st-flash", "--reset", "--format", "ihex", "write", "./simpleserial-main-CW308_STM32F3.hex"], capture_output=True)
        if output.stderr.split()[-1] != b'good!':
            print('flash failed with {}'.format(output.stderr))
    print('----------------finished reseting the program!---------------------')
    
def clear_dir(directory):
    shutil.rmtree(directory)
    os.mkdir(directory)


if __name__ == '__main__':
    # general setup 
    root_folder = os.getcwd() 
    source_dir = os.path.join(root_folder, 'firmware', 'simpleserial-main')

    asm =  os.path.join(source_dir, 'simpleserial-main.s')
    asm_benign = os.path.join(source_dir, 'simpleserial-main_benign.s')
    
    seed_dir = os.path.join(source_dir, 'klee_ifelse.txt')
    # seed_dir = os.path.join(source_dir, 'tcas-seed-10.txt')

    testing_folder = os.path.join(root_folder, 'SideChannelTesting')
    detector_folder = os.path.join(root_folder, 'SideChannelDetector')
    ben_data_folder = os.path.join(testing_folder, 'train')
    ben_test_data_folder = os.path.join(testing_folder, 'test')
    mal_data_folder = os.path.join(testing_folder, 'attack_input')
    single_data_folder = os.path.join(testing_folder, 'single')
    testcase_data_folder = os.path.join(testing_folder, 'testcase')
    max_len = 1200
    num_paths = 24
    batch_size = 128
    did = 1
    # candidateLocations = [
    #     [708, 319, 321, 327, 328, 330, 332, 333, 334],
    #     [708],
    #     [708, 319, 321, 327, 328, 330, 332, 333, 334, 336, 338, 339, 342],
    #     [708, 319, 321, 327, 328, 330, 332, 333, 334, 336, 338, 339, 348, 349, 364, 366, 369, 372, 74, 75, 77, 78, 121, 122, 123, 126, 86, 87],
    #     [708, 319, 321, 327, 328],
    #     [708, 319, 321, 327, 328, 330, 332, 333, 334, 336, 338, 339, 348, 349, 364, 366, 369, 372, 74, 75, 77, 78, 121, 122, 123, 126, 86],
    #     [708, 319, 321, 327, 328, 330, 332, 333, 334, 336, 338, 339, 342, 348, 349, 364, 366, 369, 372, 74, 75, 77, 78, 121, 122, 123, 126, 86, 87, 88, 89, 133, 134, 136, 138, 139, 140],
    #     [708, 319, 321, 327, 328, 330, 332, 333, 334, 336, 338, 339, 348, 349, 364, 366, 369, 372, 74, 75],
    #     [708, 319, 321, 327, 328, 330, 332, 333, 334, 336, 338, 339, 348, 349, 364, 366, 369, 372, 74, 75, 77, 78],
    #     [708, 319, 321, 327, 328, 330, 332, 333, 334, 336, 338, 339, 348, 349, 364, 366, 369, 372, 74, 75, 77, 78, 121, 122, 123, 126, 86, 87, 88, 89, 133, 134, 136, 138, 139, 140, 142, 143, 145, 146, 149, 152, 383, 386, 387, 388, 391, 392, 393, 396, 195, 196, 198, 200, 241, 242, 243, 246, 208, 209, 210, 211, 253, 254, 260, 263, 265, 266, 267, 270, 401, 404, 405, 406, 407, 408, 409, 449, 454, 417],
    #     [708, 319, 321, 327, 328, 330, 332, 333, 334, 336, 338, 339, 348, 349, 364],
    #     [708, 319, 321, 327, 328, 330, 332, 333, 334, 336, 338, 339, 348, 349, 364, 366, 369, 372]
    # ]
    # locations = [708, 319, 321, 327, 328, 330, 332, 333, 334, 336, 338, 339, 348, 349, 364, 366, 369, 372, 74, 75, 77, 78, 121, 122, 123, 126, 86, 87, 88, 89, 133, 134, 136, 138, 139, 140, 142, 143, 145, 146, 149, 152, 383, 386, 387, 388, 391, 392, 393, 396, 195, 196, 198, 200, 241, 242, 243, 246, 208, 209, 210, 211, 253, 254, 260, 263, 265, 266, 267, 270, 401, 404, 405, 406, 407, 408, 409, 449, 454, 417]
    candidate_locations = list(range(638, 649)) + list(range(281, 402)) + list(range(63, 144)) + list(range(173, 255))
    exclude = list(range(110, 112)) + list(range(137, 139)) + list(range(246, 248)) + list(range(315, 317)) + list(range(358, 360)) + list(range(397, 401)) 
    locations = [l for l in candidate_locations if l not in exclude]


    # checkpoint_dir = 'SideChannelDetector/checkpoints/merge'
    # model_dict_pth = os.path.join(checkpoint_dir, 'model.json')
    # with open(model_dict_pth, 'r') as f:
    #     model_dict = json.load(f)
    # model_dict['base']['model_name'] = checkpoint_dir

    # with open('perm_list.txt', 'r') as f:
    #     perm_list = f.readlines()


    # capture single
    if 0:
        ret = capture_arm_cw.capture_single(Nt=40, seed=seed_dir, index=13, root=single_data_folder)
        if ret:
            # print('{} not working!'.format(comb_name))
            print('trigger missed!')

    # collect train and test data for retrain purpose
    if 0:
        program_reset()
        capture_arm_cw.capture_all(N=num_paths, Nt=20, seed=seed_dir, root=ben_data_folder)
        capture_arm_cw.capture_all(N=num_paths, Nt=10, seed=seed_dir, root=ben_test_data_folder)


    # collect full benign data and run a validation test on the current model
    # BiLSTM
    if 0:
        # program_reset()
        # capture_arm_cw.capture_all(N=num_paths, Nt=10, seed=seed_dir, root=ben_test_data_folder)
        checkpoint_name = 'fft_0606'
        checkpoint_dir = os.path.join(detector_folder, 'checkpoints', checkpoint_name)
        model_dict_pth = os.path.join(checkpoint_dir, 'model.json')
        with open(model_dict_pth, 'r') as f:
            model_dict = json.load(f)
        model_dict['base']['model_name'] = checkpoint_dir
        model = 'base'
        score, label, predicted = inference_Detector.inference_BiLSTM(data_dir=ben_test_data_folder, model_name=model_dict[model]['model_name'], input_size=model_dict[model]['input_size'], max_len=model_dict[model]['max_len'], hidden_size=model_dict[model]['hidden_size'], num_layers=model_dict[model]['num_layers'], num_classes=model_dict[model]['num_paths'], batch_size=batch_size, feature_choice=model_dict[model]['feature_choice'])
        print('mean: {}, std: {}'.format(score.mean(), score.std()))
    # BiLSTMAdv
    if 0:
        # program_reset()
        # capture_arm_cw.capture_all(N=num_paths, Nt=10, seed=seed_dir, root=ben_test_data_folder)
        checkpoint_name = 'bilstm_time_adv_2'
        checkpoint_dir = os.path.join(detector_folder, 'checkpoints', checkpoint_name)
        model_dict_pth = os.path.join(checkpoint_dir, 'model.json')
        with open(model_dict_pth, 'r') as f:
            model_dict = json.load(f)
        model_dict['base']['model_name'] = checkpoint_dir
        model = 'base'
        score, label, predicted = inference_Detector.inference_BiLSTMAdv(data_dir=ben_test_data_folder, model_name=model_dict[model]['model_name'], input_size=model_dict[model]['input_size'], max_len=model_dict[model]['max_len'], hidden_size=model_dict[model]['hidden_size'], num_layers=model_dict[model]['num_layers'], num_classes=model_dict[model]['num_paths'], batch_size=batch_size, feature_choice=model_dict[model]['feature_choice'])
        # print('mean: {}, std: {}'.format(score.mean(), score.std()))
        ipdb.set_trace()
    # BiRNN
    if 0:
        # program_reset()
        # capture_arm_cw.capture_all(N=num_paths, Nt=10, seed=seed_dir, root=ben_test_data_folder)
        checkpoint_name = 'birnn_time_0606'
        checkpoint_dir = os.path.join(detector_folder, 'checkpoints', checkpoint_name)
        model_dict_pth = os.path.join(checkpoint_dir, 'model.json')
        with open(model_dict_pth, 'r') as f:
            model_dict = json.load(f)
        model_dict['base']['model_name'] = checkpoint_dir
        model = 'base'
        score, label, predicted = inference_Detector.inference_BiRNN(data_dir=ben_test_data_folder, model_name=model_dict[model]['model_name'], input_size=model_dict[model]['input_size'], max_len=model_dict[model]['max_len'], hidden_size=model_dict[model]['hidden_size'], num_layers=model_dict[model]['num_layers'], num_classes=model_dict[model]['num_paths'], batch_size=8, feature_choice=model_dict[model]['feature_choice'])
        print('mean: {}, std: {}'.format(score.mean(), score.std()))
    # HMM
    if 0:
        # program_reset()
        # capture_arm_cw.capture_all(N=num_paths, Nt=20, seed=seed_dir, root=mal_data_folder)
        checkpoint_name = 'hmm_time'
        checkpoint_dir = os.path.join(detector_folder, 'checkpoints', checkpoint_name)
        model_dict_pth = os.path.join(checkpoint_dir, 'model.json')
        with open(model_dict_pth, 'r') as f:
            model_dict = json.load(f)
        model_dict['base']['model_name'] = checkpoint_name
        model = 'base'
        score, label, predicted = inference_HMM.inference_HMM(data_dir=mal_data_folder, model_name=model_dict[model]['model_name'], win_size=model_dict[model]['win_size'], feature_choice=model_dict[model]['feature_choice'])
        print('mean: {}, std: {}'.format(score.mean(), score.std()))



    # #  [placeholder] collect full benign data and run a validation test on the current model
    # if 0:
    #     program_reset_placeholder()
    #     capture_arm_cw.capture_all(num_paths, 10, seed_dir, ben_test_data_folder)
    #     model = 'hs_32_nl_4'
    #     score, label, predicted = inference_Detector.inference_detector(data_dir=ben_test_data_folder, model_name=model_dict[model]['model_name'], input_size=model_dict[model]['input_size'], max_len=model_dict[model]['max_len'], hidden_size=model_dict[model]['hidden_size'], num_layers=model_dict[model]['num_layers'], num_classes=model_dict[model]['num_paths'], batch_size=8)
    
    # roc curve
    if 0:
        # program_reset()
        hiding_dir = '/home/cspl/Documents/projects/HidingInPlainSight/'
        data_dirs = [
            os.path.join(hiding_dir, 'AdvSideChannel_dijkstra', 'SideChannelTesting', 'test'),
            os.path.join(hiding_dir, 'AdvSideChannel_pid', 'SideChannelTesting', 'test'),
            os.path.join(hiding_dir, 'AdvSideChannel_kalman', 'SideChannelTesting', 'test'),
            os.path.join(hiding_dir, 'AdvSideChannel_particle', 'SideChannelTesting', 'test'),
        ]

        checkpoint_name = 'bilstm_fft_1'
        checkpoint_dir = os.path.join(detector_folder, 'checkpoints', checkpoint_name)
        model_dict_pth = os.path.join(checkpoint_dir, 'model.json')
        with open(model_dict_pth, 'r') as f:
            model_dict = json.load(f)
        model_dict['base']['model_name'] = checkpoint_name
        model = 'base'
        # positive samples
        score_pos = np.array([])
        label_pos = []
        for data_dir in data_dirs:
            score, label, predicted = inference_Detector.inference_BiLSTM(data_dir=data_dir, model_name=model_dict[model]['model_name'], input_size=model_dict[model]['input_size'], max_len=model_dict[model]['max_len'], hidden_size=model_dict[model]['hidden_size'], num_layers=model_dict[model]['num_layers'], num_classes=model_dict[model]['num_paths'], batch_size=batch_size, feature_choice=model_dict[model]['feature_choice'])
            score_pos = np.concatenate((score_pos, score))
            label_pos += len(score)*[1]

        # negative sample            
        score, label, predicted = inference_Detector.inference_BiLSTM(data_dir=ben_test_data_folder, model_name=model_dict[model]['model_name'], input_size=model_dict[model]['input_size'], max_len=model_dict[model]['max_len'], hidden_size=model_dict[model]['hidden_size'], num_layers=model_dict[model]['num_layers'], num_classes=model_dict[model]['num_paths'], batch_size=batch_size, feature_choice=model_dict[model]['feature_choice'])

        # classifier performance

        # detector performance
        score_neg = score
        label_neg = len(score)*[0]
        score_all = np.concatenate((score_pos, score_neg))
        label_all = np.array(label_pos + label_neg)
        auc = roc_auc_score(label_all, score_all)
        print('AUC is {}'.format(auc))
        fpr, tpr, ths = roc_curve(label_all, score_all, pos_label=0)
        plt.figure()
        plt.plot(fpr, tpr)
        plt.savefig(checkpoint_name+'_roc.png')
        plt.close()
        plt.figure()
        plt.plot(score_all)
        plt.savefig(checkpoint_name+'_scores.png')
        plt.close()


        np.save('roc.npy', [score_all, label_all])
    # BiRNN
    if 0:
        # program_reset()
        hiding_dir = '/home/cspl/Documents/projects/HidingInPlainSight/'
        data_dirs = [
            os.path.join(hiding_dir, 'AdvSideChannel_dijkstra', 'SideChannelTesting', 'test'),
            os.path.join(hiding_dir, 'AdvSideChannel_pid', 'SideChannelTesting', 'test'),
            os.path.join(hiding_dir, 'AdvSideChannel_kalman', 'SideChannelTesting', 'test'),
            os.path.join(hiding_dir, 'AdvSideChannel_particle', 'SideChannelTesting', 'test'),
        ]

        checkpoint_name = 'birnn_fft_0606_2'
        checkpoint_dir = os.path.join(detector_folder, 'checkpoints', checkpoint_name)
        model_dict_pth = os.path.join(checkpoint_dir, 'model.json')
        with open(model_dict_pth, 'r') as f:
            model_dict = json.load(f)
        model_dict['base']['model_name'] = checkpoint_name
        model = 'base'
        # positive samples
        score_pos = np.array([])
        label_pos = []
        for data_dir in data_dirs:
            score, label, predicted = inference_Detector.inference_BiRNN(data_dir=data_dir, model_name=model_dict[model]['model_name'], input_size=model_dict[model]['input_size'], max_len=model_dict[model]['max_len'], hidden_size=model_dict[model]['hidden_size'], num_layers=model_dict[model]['num_layers'], num_classes=model_dict[model]['num_paths'], batch_size=batch_size, feature_choice=model_dict[model]['feature_choice'])
            score_pos = np.concatenate((score_pos, score))
            label_pos += len(score)*[1]

        # negative sample            
        score, label, predicted = inference_Detector.inference_BiRNN(data_dir=ben_test_data_folder, model_name=model_dict[model]['model_name'], input_size=model_dict[model]['input_size'], max_len=model_dict[model]['max_len'], hidden_size=model_dict[model]['hidden_size'], num_layers=model_dict[model]['num_layers'], num_classes=model_dict[model]['num_paths'], batch_size=batch_size, feature_choice=model_dict[model]['feature_choice'])

        # classifier performance

        # detector performance
        score_neg = score
        label_neg = len(score)*[0]
        score_all = np.concatenate((score_pos, score_neg))
        label_all = np.array(label_pos + label_neg)
        auc = roc_auc_score(label_all, score_all)
        print('AUC is {}'.format(auc))
        fpr, tpr, ths = roc_curve(label_all, score_all, pos_label=0)
        plt.figure()
        plt.plot(fpr, tpr)
        plt.savefig(checkpoint_name+'_roc.png')
        plt.close()
        plt.figure()
        plt.plot(score_all)
        plt.savefig(checkpoint_name+'_scores.png')
        plt.close()


        np.save('roc.npy', [score_all, label_all])
        
    # replace attack
    if 0:
        mals = [
            mal_list.data_injection,
            mal_list.control_parameter,
            mal_list.overwrite_output,
            # mal_list.data_logging,
        ]
        for malware in mals:
            # malware = mal_list.data_injection
            ret = parse_s.replace_malware_chunks(asm, malware)
            if ret:
                print("failed to replace!")
                sys.exit()

            # capture signals
            ret = capture_arm_cw.capture_all(N=num_paths, Nt=10, seed=seed_dir, root=mal_data_folder)
            if ret:
                # print('{} not working!'.format(comb_name))
                print('trigger missed!')
                # sys.exit()
                continue

            # # send to detector
            model = 'base'
            score, label, predicted = inference_Detector.inference_detector(data_dir=mal_data_folder, model_name=model_dict[model]['model_name'], input_size=model_dict[model]['input_size'], max_len=model_dict[model]['max_len'], hidden_size=model_dict[model]['hidden_size'], num_layers=model_dict[model]['num_layers'], num_classes=model_dict[model]['num_paths'], batch_size=8)
            print('mean: {}, std: {}'.format(score.mean(), score.std()))
    
    # whole attack
    if 0:
        mals = [
            mal_list.data_injection,
            mal_list.control_parameter,
            mal_list.overwrite_output,
            # mal_list.data_logging,
        ]
        for malware in mals:
            # malware = mal_list.data_injection
            comb = len(malware)*[721]
            ret = parse_s.insert_malware_chunks(comb, asm, malware)
            if ret:
                print("failed to replace!")
                sys.exit()

            # capture signals
            ret = capture_arm_cw.capture_all(N=num_paths, Nt=10, seed=seed_dir, root=mal_data_folder)
            if ret:
                # print('{} not working!'.format(comb_name))
                print('trigger missed!')
                sys.exit()

            # # send to detector
            model = 'base'
            score, label, predicted = inference_Detector.inference_detector(data_dir=mal_data_folder, model_name=model_dict[model]['model_name'], input_size=model_dict[model]['input_size'], max_len=model_dict[model]['max_len'], hidden_size=model_dict[model]['hidden_size'], num_layers=model_dict[model]['num_layers'], num_classes=model_dict[model]['num_paths'], batch_size=8)
            print('mean: {}, std: {}'.format(score.mean(), score.std()))
    


    # random attack 
    # BiLSTM
    if 0:
        checkpoint_dir = 'SideChannelDetector/checkpoints/bilstm_time/'
        model_dict_pth = os.path.join(checkpoint_dir, 'model.json')
        with open(model_dict_pth, 'r') as f:
            model_dict = json.load(f)
        model_dict['base']['model_name'] = checkpoint_dir
        model = 'base'


        # get baseline results
        score, label, predicted = inference_Detector.inference_BiLSTM(data_dir=mal_data_folder, model_name=model_dict[model]['model_name'], input_size=model_dict[model]['input_size'], max_len=model_dict[model]['max_len'], hidden_size=model_dict[model]['hidden_size'], num_layers=model_dict[model]['num_layers'], num_classes=model_dict[model]['num_paths'], batch_size=batch_size, feature_choice=model_dict[model]['feature_choice'])
        score_baseline = score.mean()

        score_all = []

        log_file = os.path.join(os.getcwd(), 'random_attack'+checkpoint_dir.split('/')[-1]+'.txt')
        with open(log_file, 'w+') as f:
            pass

        mals = [
            mal_list.data_injection,
            mal_list.control_parameter,
            mal_list.overwrite_output,
            # mal_list.data_logging,
        ]

        for malware in mals:
            malware = mal_list.data_injection
            # candidateLocations = len(malware)*[list(range(212, 279))]
            candidateLocations = len(malware)*[locations]
            for i in range(1000):
                comb = len(malware)*[638]
                # comb = random_injection(candidateLocations)
                print(comb)
                ret = parse_s.insert_malware_chunks(comb, asm, malware)
                if ret:
                    print("failed to replace!")
                    # sys.exit()
                    continue
                
                ipdb.set_trace()

                # capture signals
                ret = capture_arm_cw.capture_all(N=num_paths, Nt=10, seed=seed_dir, root=mal_data_folder, device_id=0)
                if ret:
                    # print('{} not working!'.format(comb_name))
                    print('trigger missed!')
                    # sys.exit()
                    continue

                # # send to detector
                score, label, predicted = inference_Detector.inference_BiLSTM(data_dir=mal_data_folder, model_name=model_dict[model]['model_name'], input_size=model_dict[model]['input_size'], max_len=model_dict[model]['max_len'], hidden_size=model_dict[model]['hidden_size'], num_layers=model_dict[model]['num_layers'], num_classes=model_dict[model]['num_paths'], batch_size=batch_size, feature_choice=model_dict[model]['feature_choice'])
                record = '{}: mean: {}, min: {}, std: {}'.format(comb, score.mean()/score_baseline, (score/score_baseline).min(), (score/score_baseline).std())
                print(record)
                # print(predicted)
                # score_all.append(score)
                
                with open(log_file, 'a') as f:
                    f.write(record+'\n')
    # BiLSTMAdv
    if 1:
        checkpoint_dir = 'SideChannelDetector/checkpoints/bilstm_time_adv'
        model_dict_pth = os.path.join(checkpoint_dir, 'model.json')
        with open(model_dict_pth, 'r') as f:
            model_dict = json.load(f)
        model_dict['base']['model_name'] = checkpoint_dir
        model = 'base'

        score_all = []

        log_file = os.path.join(os.getcwd(), 'random_attack'+'bilstm_time_adv'+'.txt')
        with open(log_file, 'w+') as f:
            pass

        mals = [
            mal_list.data_injection,
            mal_list.control_parameter,
            mal_list.overwrite_output,
            # mal_list.data_logging,
        ]

        for malware in mals:
            malware = mal_list.data_injection
            # candidateLocations = len(malware)*[list(range(212, 279))]
            candidateLocations = len(malware)*[locations]
            for i in range(1000):
                # comb = len(malware)*[212]
                comb = random_injection(candidateLocations)
                print(comb)
                ret = parse_s.insert_malware_chunks(comb, asm, malware)
                if ret:
                    print("failed to replace!")
                    # sys.exit()
                    continue

                # capture signals
                # ret = capture_arm_cw.capture_all(N=num_paths, Nt=5, seed=seed_dir, root=mal_data_folder, device_id=0)
                # if ret:
                #     # print('{} not working!'.format(comb_name))
                #     print('trigger missed!')
                #     # sys.exit()
                #     continue

                # # send to detector
                score, label, predicted = inference_Detector.inference_BiLSTMAdv(data_dir=mal_data_folder, model_name=model_dict[model]['model_name'], input_size=model_dict[model]['input_size'], max_len=model_dict[model]['max_len'], hidden_size=model_dict[model]['hidden_size'], num_layers=model_dict[model]['num_layers'], num_classes=model_dict[model]['num_paths'], batch_size=batch_size, feature_choice=model_dict[model]['feature_choice'])
                # record = 'mean: {}, min: {}, std: {}'.format(score.mean(), score.min(), score.std())
                # print(record)

                asr = (sum(predicted==0)/predicted.shape[0])
                record = '{}: ASR: {}'.format(comb, 1-asr)
                print(record)

                # ipdb.set_trace()

                # print(predicted)
                # score_all.append(score)
                
                with open(log_file, 'a') as f:
                    f.write(record+'\n')
    # BiRNN
    if 0:
        checkpoint_name = 'birnn_time'
        checkpoint_dir = os.path.join(detector_folder, 'checkpoints', checkpoint_name)
        model_dict_pth = os.path.join(checkpoint_dir, 'model.json')
        with open(model_dict_pth, 'r') as f:
            model_dict = json.load(f)
        model_dict['base']['model_name'] = checkpoint_name
        model = 'base'

        # get baseline score
        score, label, predicted = inference_Detector.inference_BiRNN(data_dir=ben_test_data_folder, model_name=model_dict[model]['model_name'], input_size=model_dict[model]['input_size'], max_len=model_dict[model]['max_len'], hidden_size=model_dict[model]['hidden_size'], num_layers=model_dict[model]['num_layers'], num_classes=model_dict[model]['num_paths'], batch_size=win_size, feature_choice=model_dict[model]['feature_choice'])
        score_baseline = score.mean()


        score_all = []

        log_file = os.path.join(os.getcwd(), 'random_attack_'+checkpoint_name+'.txt')
        with open(log_file, 'w+') as f:
            pass

        mals = [
            mal_list.data_injection,
            mal_list.control_parameter,
            mal_list.overwrite_output,
            # mal_list.data_logging,
        ]

        for malware in mals:
            malware = mal_list.data_injection
            # candidateLocations = len(malware)*[list(range(212, 279))]
            candidateLocations = len(malware)*[locations]
            for i in range(1000):
                # comb = len(malware)*[212]
                comb = random_injection(candidateLocations)
                print(comb)
                ret = parse_s.insert_malware_chunks(comb, asm, malware)
                if ret:
                    print("failed to replace!")
                    # sys.exit()
                    continue

                # capture signals
                ret = capture_arm_cw.capture_all(N=num_paths, Nt=10, seed=seed_dir, root=mal_data_folder, device_id=0)
                if ret:
                    # print('{} not working!'.format(comb_name))
                    print('trigger missed!')
                    # sys.exit()
                    continue

                # # send to detector
                score, label, predicted = inference_Detector.inference_BiRNN(data_dir=mal_data_folder, model_name=model_dict[model]['model_name'], input_size=model_dict[model]['input_size'], max_len=model_dict[model]['max_len'], hidden_size=model_dict[model]['hidden_size'], num_layers=model_dict[model]['num_layers'], num_classes=model_dict[model]['num_paths'], batch_size=8, feature_choice=model_dict[model]['feature_choice'])
                record = 'mean: {}, min: {}, std: {}'.format(score.mean()/score_baseline, score.min()/score_baseline, (score/score_baseline).std())
                print(record)
                # print(predicted)
                # score_all.append(score)
                
                with open(log_file, 'a') as f:
                    f.write('{} --- '.format(comb)+record+'\n')
    # HMM
    if 0:
        checkpoint_name = 'hmm_fft'
        checkpoint_dir = os.path.join(detector_folder, 'checkpoints', checkpoint_name)
        model_dict_pth = os.path.join(checkpoint_dir, 'model.json')
        with open(model_dict_pth, 'r') as f:
            model_dict = json.load(f)
        model_dict['base']['model_name'] = checkpoint_name
        model = 'base'

        # get baseline performance
        score, label, predicted = inference_HMM.inference_HMM(data_dir=ben_test_data_folder, model_name=model_dict[model]['model_name'], win_size=model_dict[model]['win_size'], feature_choice=model_dict[model]['feature_choice'])
        score_baseline = score.mean()
        print('baseline score is {}'.format(score_baseline))
        

        score_all = []

        log_file = os.path.join(os.getcwd(), 'random_attack_'+checkpoint_name+'.txt')
        with open(log_file, 'w+') as f:
            pass

        mals = [
            mal_list.data_injection,
            mal_list.control_parameter,
            mal_list.overwrite_output,
            # mal_list.data_logging,
        ]

        for malware in mals:
            malware = mal_list.data_injection
            # candidateLocations = len(malware)*[list(range(212, 279))]
            candidateLocations = len(malware)*[locations]
            for i in range(1000):
                # comb = len(malware)*[212]
                comb = random_injection(candidateLocations)
                print(comb)
                ret = parse_s.insert_malware_chunks(comb, asm, malware)
                if ret:
                    print("failed to replace!")
                    # sys.exit()
                    continue

                # capture signals
                ret = capture_arm_cw.capture_all(N=num_paths, Nt=10, seed=seed_dir, root=mal_data_folder, device_id=0)
                if ret:
                    # print('{} not working!'.format(comb_name))
                    print('trigger missed!')
                    # sys.exit()
                    continue

                # # send to detector
                score, label, predicted = inference_HMM.inference_HMM(data_dir=mal_data_folder, model_name=model_dict[model]['model_name'], win_size=model_dict[model]['win_size'], feature_choice=model_dict[model]['feature_choice'])
                record = 'mean: {}, min: {}, std: {}'.format(score.mean()/score_baseline, (score/score_baseline).min(), (score/score_baseline).std())
                print(record)
                # print(predicted)
                # score_all.append(score)
                
                with open(log_file, 'a') as f:
                    f.write('{} --- '.format(comb)+record+'\n')

    # transferability
    # BiLSTM
    if 0:
        malware = mal_list.data_injection

        comb = [188, 392, 82, 128, 377, 183, 224, 320, 324, 363, 204, 250] # BiLSTM
        # comb = [240, 103, 396, 213, 292, 76, 373, 344, 396, 96, 229, 70] # BiRNN
        # comb = [100, 324, 368, 190, 391, 181, 380, 325, 202, 90, 103, 87] # HMM
        print(comb)

        # inject the chunks
        ret = parse_s.insert_malware_chunks(comb, asm, malware)
        if ret:
            print("failed to replace!")
            sys.exit()
            # continue

        # capture signals
        ret = capture_arm_cw.capture_all(N=num_paths, Nt=10, seed=seed_dir, root=mal_data_folder, device_id=0)
        if ret:
            # print('{} not working!'.format(comb_name))
            print('trigger missed!')
            sys.exit()
            # continue
        
        # send to BiLSTM
        print('querying BiLSTM...')
        checkpoint_name = 'bilstm_time'
        checkpoint_dir = os.path.join(detector_folder, 'checkpoints', checkpoint_name)
        model_dict_pth = os.path.join(checkpoint_dir, 'model.json')
        with open(model_dict_pth, 'r') as f:
            model_dict = json.load(f)
        model_dict['base']['model_name'] = checkpoint_name
        model = 'base'
        score, label, predicted = inference_Detector.inference_BiLSTM(data_dir=mal_data_folder, model_name=model_dict[model]['model_name'], input_size=model_dict[model]['input_size'], max_len=model_dict[model]['max_len'], hidden_size=model_dict[model]['hidden_size'], num_layers=model_dict[model]['num_layers'], num_classes=model_dict[model]['num_paths'], batch_size=batch_size, feature_choice=model_dict[model]['feature_choice'])
        record = 'mean: {}, min: {}, std: {}'.format(score.mean(), score.min(), score.std())
        print(record)


        #  send to BiRNN 
        print('qeurying BiRNN...')
        checkpoint_name = 'birnn_time'
        checkpoint_dir = os.path.join(detector_folder, 'checkpoints', checkpoint_name)
        model_dict_pth = os.path.join(checkpoint_dir, 'model.json')
        with open(model_dict_pth, 'r') as f:
            model_dict = json.load(f)
        model_dict['base']['model_name'] = checkpoint_name
        model = 'base'
        score, label, predicted = inference_Detector.inference_BiRNN(data_dir=mal_data_folder, model_name=model_dict[model]['model_name'], input_size=model_dict[model]['input_size'], max_len=model_dict[model]['max_len'], hidden_size=model_dict[model]['hidden_size'], num_layers=model_dict[model]['num_layers'], num_classes=model_dict[model]['num_paths'], batch_size=8, feature_choice=model_dict[model]['feature_choice'])
        record = 'mean: {}, min: {}, std: {}'.format(score.mean(), score.min(), score.std())
        print(record)

        # send to HMM
        print('querying HMM...')
        checkpoint_name = 'hmm_time'
        checkpoint_dir = os.path.join(detector_folder, 'checkpoints', checkpoint_name)
        model_dict_pth = os.path.join(checkpoint_dir, 'model.json')
        with open(model_dict_pth, 'r') as f:
            model_dict = json.load(f)
        model_dict['base']['model_name'] = checkpoint_name
        model = 'base'
        score, label, predicted = inference_HMM.inference_HMM(data_dir=mal_data_folder, model_name=model_dict[model]['model_name'], win_size=model_dict[model]['win_size'], feature_choice=model_dict[model]['feature_choice'])
        record = 'mean: {}, min: {}, std: {}'.format(score.mean(), score.min(), score.std())
        print(record)
    
    # adversarial training data collection
    if 0:
        combs = [
            [347, 186, 202, 332, 370, 313, 311, 177, 189, 99, 249, 331],
            [319, 389, 357, 132, 378, 292, 252, 254, 113, 320, 349, 286],
            [329, 90, 105, 94, 182, 115, 252, 120, 310, 344, 183, 88],
            [72, 85, 307, 225, 129, 102, 200, 208, 174, 337, 395, 68],
            [220, 233, 391, 220, 379, 218, 103, 85, 327, 70, 305, 107],
            [218, 201, 374, 297, 223, 106, 134, 71, 104, 233, 340, 253],
            [643, 194, 341, 106, 67, 253, 106, 339, 209, 177, 301, 87],
            [385, 387, 646, 230, 383, 340, 181, 116, 194, 294, 647, 363],
            [227, 231, 176, 314, 393, 101, 223, 129, 384, 203, 283, 344],
            [372, 127, 196, 320, 328, 64, 385, 376, 388, 105, 182, 180],            
            [401, 195, 376, 352, 101, 220, 66, 109, 218, 74, 282, 250],            
            [369, 642, 329, 82, 330, 336, 288, 294, 352, 123, 345, 97],
        ]

        for i, comb in enumerate(combs):
            save_path = os.path.join(testing_folder, 'adv_train', str(i))
            if not os.path.exists(save_path):
                os.mkdir(save_path)

            malware = mal_list.data_injection
            print(comb)
            # inject the chunks
            ret = parse_s.insert_malware_chunks(comb, asm, malware)
            if ret:
                print("failed to replace!")
                # sys.exit()
                continue

            # capture signals
            ret = capture_arm_cw.capture_all(N=num_paths, Nt=10, seed=seed_dir, root=save_path, device_id=0)
            if ret:
                # print('{} not working!'.format(comb_name))
                print('trigger missed!')
                # sys.exit()
                continue













































    # collect data for current version of the program and run detector
    if 0:
        capture_arm_cw.capture_all(num_paths, 10, seed_dir, ben_test_data_folder)
        model = '09282020'
        score, label, predicted = inference_Detector.inference_detector(data_dir=ben_test_data_folder, model_name=model_dict[model]['model_name'], input_size=model_dict[model]['input_size'], max_len=model_dict[model]['max_len'], hidden_size=model_dict[model]['hidden_size'], num_layers=model_dict[model]['num_layers'], num_classes=model_dict[model]['num_paths'], batch_size=8)

    # collect a single path multiple times and run detector
    if 0:
        path_id = 26
        capture_arm_cw.capture_single(20, seed_dir, path_id, single_data_folder)
        score, label, predicted = inference_Detector.inference_detector(single_data_folder, 4, max_len, 128, 2, 50, 8)

    # collect a single testcase multiple times and run detector
    if 0:
        path_id = 3
        testcase_id = 4
        capture_arm_cw.capture_testcase(100, seed_dir, path_id, 4, testcase_data_folder)
        score, label, predicted = inference_Detector.inference_detector(testcase_data_folder, 4, max_len, 128, 2, 50, 8)

    # collect full benign data multiple times
    if 0:
        program_reset()
        for i in range(10):
            print('#{} iteration...'.format(i))
            capture_arm_cw.capture_all(50, 10, seed_dir, ben_test_data_folder)
            score, label, predicted = inference_Detector.inference_detector(ben_test_data_folder, 4, max_len, 128, 2, 50, 8)
            result_dir = os.path.join(detector_folder, 'results_benign_1', str(i))
            np.save(result_dir, [score, predicted, label])

    # collect several full mal data of random choices (chunks) of injection multiple times
    if 0:
        for it1 in range(1, 100):
            it = 1
            # comb = random_combination(''.join(A_list), ''.join(a_list))
            comb = random_injection(candidateLocations)
            # comb = 12*[708]
            comb_name = "_".join([str(item) for item in comb])
            score_dir = 'chunk_injection_1'
            print('Generated combination: {}'.format(comb))
            if not os.path.exists(os.path.join(detector_folder, score_dir)):
                os.mkdir(os.path.join(detector_folder, score_dir))
            for i in range(it):
                # inject malware
                ret = parse_s.insert_malware_chunks(comb, asm, mal_list)
                if ret:
                    print("failed to inject!")
                    continue

                # capture signals
                ret = capture_arm_cw.capture_all(N=num_paths, Nt=10, seed=seed_dir, root=mal_data_folder)
                if ret:
                    # print('{} not working!'.format(comb_name))
                    print('trigger missed!')
                    continue

                # send to detector
                model = 'hs_128_nl_2'
                print('Querying {}...'.format(model))
                # send to detector
                score, label, predicted = inference_Detector.inference_detector(data_dir=mal_data_folder, model_name=model_dict[model]['model_name'], input_size=model_dict[model]['input_size'], max_len=model_dict[model]['max_len'], hidden_size=model_dict[model]['hidden_size'], num_layers=model_dict[model]['num_layers'], num_classes=model_dict[model]['num_paths'], batch_size=8)

                # save
                result_dir = os.path.join(detector_folder, score_dir, comb_name+'-'+str(i))
                np.save(result_dir, [score, predicted, label])
    
    # test single for an arbitrary path
    if 0:
        comb = [330, 708, 342, 327, 321, 338, 140, 336, 708, 333, 338, 321]
        comb = 1*[728]
        ret = parse_s.insert_malware_chunks(comb, asm, mal_list)
        if ret:
            print("failed to inject!")
            sys.exit()

        # capture signals
        ret = capture_arm_cw.capture_single(Nt=40, seed=seed_dir, index=13, root=single_data_folder)
        if ret:
            # print('{} not working!'.format(comb_name))
            print('trigger missed!')
            sys.exit()

        # # send to detector
        model = '09282020_1'
        score, label, predicted = inference_Detector.inference_detector(data_dir=single_data_folder, model_name=model_dict[model]['model_name'], input_size=model_dict[model]['input_size'], max_len=model_dict[model]['max_len'], hidden_size=model_dict[model]['hidden_size'], num_layers=model_dict[model]['num_layers'], num_classes=model_dict[model]['num_paths'], batch_size=8)

    # test full for an arbitrary injection
    if 0:
        comb = [330, 708, 342, 327, 321, 338, 140, 336, 708, 333, 338, 321]
        comb = 4*[728]
        ret = parse_s.insert_malware_chunks(comb, asm, mal_list)
        if ret:
            print("failed to inject!")

        # capture signals
        ret = capture_arm_cw.capture_all(N=num_paths, Nt=10, seed=seed_dir, root=mal_data_folder)
        if ret:
            # print('{} not working!'.format(comb_name))
            print('trigger missed!')
            sys.exit()

        # send to detector
        model = '10062020'
        score, label, predicted = inference_Detector.inference_detector(data_dir=mal_data_folder, model_name=model_dict[model]['model_name'], input_size=model_dict[model]['input_size'], max_len=model_dict[model]['max_len'], hidden_size=model_dict[model]['hidden_size'], num_layers=model_dict[model]['num_layers'], num_classes=model_dict[model]['num_paths'], batch_size=8)



    # rebuild and program with the current version of assembly
    if 0:
        os.chdir("C:/Users/char8/Documents/AdvSideChannel_tcas/firmware/simpleserial-tcas")
        output = subprocess.run(["windows_make_binary.bat", "tcas"], capture_output=True)
        if output.stderr != b'':
            print('build failed with {}'.format(output.stderr))
        else:
            output = subprocess.run(["st-flash.exe", "--reset", "--format", "ihex", "write", "./simpleserial-tcas-CW308_STM32F3.hex"], capture_output=True)
            if output.stderr.split()[-1] != b'good!':
                print('flash failed with {}'.format(output.stderr))

    
    # single permutation and inject
    if 0:
        comb = [330, 708, 342, 327, 321, 338, 140, 336, 708, 333, 338, 321]
        ret = parse_s.insert_malware_chunks(comb, asm, mal_list)
        if ret:
            print("failed to inject!")

    # try permutations from a file wrt different models
    if 0:
        # secify permutation
        perm_list_name = 'perm_list.txt'
        with open(perm_list_name, 'r') as f:
            perm_list = f.read().splitlines()

        for comb in perm_list: 
            print("Processing combinations: {}".format(comb))
            # inject malware
            ret = parse_s.insert_malware_chunks(list(map(int, comb.split('_'))), asm, mal_list)
            if ret:
                print("failed to inject!")
                continue

            # capture signals
            print('collecting data to {}...'.format(mal_data_folder))
            ret = capture_arm_cw.capture_all(N=num_paths, Nt=10, seed=seed_dir, root=mal_data_folder)
            if ret:
                # print('{} not working!'.format(comb_name))
                print('trigger missed!')
                continue

            for model in model_dict.keys():
                print('Querying {}...'.format(model))
                # send to detector
                score, label, predicted = inference_Detector.inference_detector(data_dir=mal_data_folder, model_name=model_dict[model]['model_name'], input_size=model_dict[model]['input_size'], max_len=model_dict[model]['max_len'], hidden_size=model_dict[model]['hidden_size'], num_layers=model_dict[model]['num_layers'], num_classes=model_dict[model]['num_paths'], batch_size=8)

                score_dir = 'transferability-'+model
                if not os.path.exists(os.path.join(detector_folder, score_dir)):
                    os.mkdir(os.path.join(detector_folder, score_dir))
                result_dir = os.path.join(detector_folder, score_dir, comb)
                np.save(result_dir, [score, predicted, label])

    # try a single permutation from a file wrt to a single model
    if 0:
        # reset data dir
        clear_dir(mal_data_folder)

        # secify permutation
        perm_list_name = 'perm_list.txt'
        with open(perm_list_name, 'r') as f:
            perm_list = f.read().splitlines()

        for comb in perm_list:
            print("Processing combinations: {}".format(comb))
            # inject malware
            ret = parse_s.insert_malware_chunks(list(map(int, comb.split('_'))), asm, mal_list)
            if ret:
                print("failed to inject!")

            # capture signals
            print('collecting data to {}...'.format(mal_data_folder))
            ret = capture_arm_cw.capture_all(N=num_paths, Nt=10, seed=seed_dir, root=mal_data_folder)
            if ret:
                # print('{} not working!'.format(comb_name))
                print('trigger missed!')

            model = 'hs_128_nl_2'
            print('Querying {}...'.format(model))
            # send to detector
            score, label, predicted = inference_Detector.inference_detector(data_dir=mal_data_folder, model_name=model_dict[model]['model_name'], input_size=model_dict[model]['input_size'], max_len=model_dict[model]['max_len'], hidden_size=model_dict[model]['hidden_size'], num_layers=model_dict[model]['num_layers'], num_classes=model_dict[model]['num_paths'], batch_size=8)

            score_dir = 'validate-'+model
            if not os.path.exists(os.path.join(detector_folder, score_dir)):
                os.mkdir(os.path.join(detector_folder, score_dir))
            result_dir = os.path.join(detector_folder, score_dir, comb)
            np.save(result_dir, [score, predicted, label])

    # collect single path mal data of random choices several times
    if 0:
        for it1 in range(1, 100):
            # generate random permutation
            comb = random_injection(candidateLocations)
            comb_name = "_".join([str(item) for item in comb])
            print('Generated combination: {}'.format(comb))

            # create dir to store results
            score_dir = 'chunk_injection_single'
            if not os.path.exists(os.path.join(detector_folder, score_dir)):
                os.mkdir(os.path.join(detector_folder, score_dir))

            # inject malware
            ret = parse_s.insert_malware_chunks(comb, asm, mal_list)
            if ret:
                print("failed to inject!")
                continue

            # capture signals
            ret = capture_arm_cw.capture_single(Nt=40, seed=seed_dir, index=8, root=single_data_folder)
            if ret:
                # print('{} not working!'.format(comb_name))
                print('trigger missed!')
                continue

            # send to detector
            score, label, predicted = inference_Detector.inference_detector(data_dir=single_data_folder, input_size=4, max_len=max_len, hidden_size=128, num_layers=2, num_classes=num_paths, batch_size=8)

            # save
            result_dir = os.path.join(detector_folder, score_dir, comb_name)
            np.save(result_dir, [score, predicted, label])

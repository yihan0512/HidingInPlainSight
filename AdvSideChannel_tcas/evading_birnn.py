# mcts
from __future__ import division
from copy import deepcopy
from mcts import mcts

import ast

import os
import argparse

# malware injection
from SideChannelDetector import parse_s, mal_list
from SideChannelDetector import inference_Detector
from SideChannelTesting import capture_arm_cw, NUM_PATHS
from utils.utils import program_reset, read_results

import numpy as np

import json
import ipdb

class EvadingSideChannelDetectorState():
    def __init__(self, malware, locations, detector_checkpoint, batch_size):
        source_dir = os.path.join('firmware', 'simpleserial-main')
        testing_folder = 'SideChannelTesting/'

        self.asm = 'simpleserial-main.s' # name of the asm file
        
        self.seed_dir = os.path.join(source_dir, 'klee_ifelse.txt')
        self.data_dir = os.path.join(testing_folder, 'attack')
        self.malware = malware
        
        model_dict_pth = os.path.join(detector_checkpoint, 'model.json')
        with open(model_dict_pth, 'r') as f:
            self.model_dict = json.load(f)
        self.model = 'base'
        self.model_dict[self.model]['model_name'] = detector_checkpoint
        self.batch_size = batch_size
        
        self.eta = 1

        self.injectedProgram = len(self.malware) * [0]
        self.candidateLocations = locations
        '''
        available injection locations for each malware chunk
        candidateLocations = [
            [141, 152, 163, ...],
            [141, 172, 198, ...],
            [172, 173, 174, ...],
            ...
        ]
        '''
        
        # baseline score
        print('--------------getting baseline score-----------')
        program_reset()
        ret = capture_arm_cw.capture_all(N=NUM_PATHS, Nt=10, seed=self.seed_dir, root=self.data_dir)
        if ret:
            return 0
        score, _, _ = inference_Detector.inference_BiRNN(data_dir=self.data_dir, model_name=self.model_dict[self.model]['model_name'], input_size=self.model_dict[self.model]['input_size'], max_len=self.model_dict[self.model]['max_len'], hidden_size=self.model_dict[self.model]['hidden_size'], num_layers=self.model_dict[self.model]['num_layers'], num_classes=self.model_dict[self.model]['num_paths'], batch_size=self.batch_size, feature_choice=self.model_dict[self.model]['feature_choice'])
        self.score_baseline = score.mean()
        print('baseline score is {}'.format(self.score_baseline))

        # save explored injection combinations 
        self.log_file = 'results/tmp.txt'
        with open(self.log_file, 'w+') as f:
            pass
        

    def getPossibleActions(self):
        possibleActions = []
        for i, item in enumerate(self.injectedProgram):
            if item == 0:
                for can_loc in self.candidateLocations[i]:
                    action = self.injectedProgram.copy()
                    action[i] = can_loc
                    possibleActions.append(tuple(action))
        return possibleActions

    def takeAction(self, action):
        newState = deepcopy(self)
        # inject the specific malicious chunk
        newState.injectedProgram = list(action)
        return newState

    def isTerminal(self):
        return all(self.injectedProgram)
        
    def getReward(self):
        # inject chunks
        ret = parse_s.insert_malware_chunks(self.injectedProgram, self.asm, self.malware)
        if ret:
            return 0
        # collect data
        ret = capture_arm_cw.capture_all(N=NUM_PATHS, Nt=10, seed=self.seed_dir, root=self.data_dir)
        if ret:
            return 0
        # inference
        score, _, _ = inference_Detector.inference_BiRNN(data_dir=self.data_dir, model_name=self.model_dict[self.model]['model_name'], input_size=self.model_dict[self.model]['input_size'], max_len=self.model_dict[self.model]['max_len'], hidden_size=self.model_dict[self.model]['hidden_size'], num_layers=self.model_dict[self.model]['num_layers'], num_classes=self.model_dict[self.model]['num_paths'], batch_size=self.batch_size, feature_choice=self.model_dict[self.model]['feature_choice'])
        # return score[0] - 0.8
        score = score / self.score_baseline

        record = '{}: {}, {}'.format(self.injectedProgram, round(score.mean(), 2), score.std())
        # tqdm.write(record)
        with open(self.log_file, 'a') as f:
            f.write(record+'\n')
        return round(score.mean()+self.eta*score.std(), 2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='validate the detectors')
    parser.add_argument('--malware', default='data_injection', type=str, help='specify the malware to be injected')
    parser.add_argument('--checkpoint', type=str, help='checkpoint path')
    parser.add_argument('--batch-size', default=128, type=int, help='batch size')
    parser.add_argument('-e', '--epochs', default=200, type=int, help='number of epoches')
    parser.add_argument('--top', default=1, type=int, help='top n results to store')
    args = parser.parse_args()
    '''
    malwares:
     - data_injection
     - 
    '''

    initialState = EvadingSideChannelDetectorState(malware=eval('mal_list.'+args.malware), locations=eval('mal_list.'+args.malware+'_locations'), detector_checkpoint=args.checkpoint, batch_size=args.batch_size)

    mcts = mcts(iterationLimit=args.epochs)
    action = mcts.search(initialState=initialState)

    injections, scores_mean, scores_std = read_results(initialState.log_file)
    save_dir = os.path.join('results', 'birnn', initialState.model_dict[initialState.model]['feature_choice'])
    os.makedirs(save_dir, exist_ok=True)
    idx_sorted = np.argsort(scores_mean)
    with open(os.path.join(save_dir, args.malware+'.txt'), 'w+') as f:
        for idx in idx_sorted[:args.top]:
            f.write('{}: {}, {}'.format(injections[idx], scores_mean[idx], scores_std[idx])+'\n')
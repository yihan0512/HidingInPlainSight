import os 
import argparse
import json
import subprocess

from SideChannelTesting import capture_arm_cw
from SideChannelDetector import inference_Detector
from SideChannelDetector import inference_HMM

import ipdb

from utils.utils import program_reset


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='validate the detectors')
    parser.add_argument('--model', type=str, help='which model, bilstm, birnn or hmm')
    parser.add_argument('--checkpoint', type=str, help='checkpoint path')
    parser.add_argument('--collect', type=int, help='collect data or not')
    args = parser.parse_args()

    num_paths = 24
    batch_size = 128 # change based on your gpu memory
    root_folder = os.getcwd() 
    testing_folder = os.path.join(root_folder, 'SideChannelTesting')
    detector_folder = os.path.join(root_folder, 'SideChannelDetector')
    ben_test_data_folder = os.path.join(testing_folder, 'test')

    source_dir = os.path.join(root_folder, 'firmware', 'simpleserial-main')
    seed_dir = os.path.join(source_dir, 'klee_ifelse.txt')

    checkpoint_dir = args.checkpoint
    model_dict_pth = os.path.join(checkpoint_dir, 'model.json')
    with open(model_dict_pth, 'r') as f:
        model_dict = json.load(f)
    model_dict['base']['model_name'] = checkpoint_dir
    model = 'base'

    # collect data or not
    if args.collect:
        program_reset()
        capture_arm_cw.capture_all(N=num_paths, Nt=10, seed=seed_dir, root=ben_test_data_folder)

    # collect full benign data and run a validation test on the current model
    # BiLSTM
    if args.model == 'bilstm':
        score, label, predicted = inference_Detector.inference_BiLSTM(data_dir=ben_test_data_folder, model_name=model_dict[model]['model_name'], input_size=model_dict[model]['input_size'], max_len=model_dict[model]['max_len'], hidden_size=model_dict[model]['hidden_size'], num_layers=model_dict[model]['num_layers'], num_classes=model_dict[model]['num_paths'], batch_size=batch_size, feature_choice=model_dict[model]['feature_choice'])
    # BiRNN
    elif args.model == 'birnn':
        score, label, predicted = inference_Detector.inference_BiRNN(data_dir=ben_test_data_folder, model_name=model_dict[model]['model_name'], input_size=model_dict[model]['input_size'], max_len=model_dict[model]['max_len'], hidden_size=model_dict[model]['hidden_size'], num_layers=model_dict[model]['num_layers'], num_classes=model_dict[model]['num_paths'], batch_size=8, feature_choice=model_dict[model]['feature_choice'])
    # HMM
    elif args.model == 'hmm':
        score, label, predicted = inference_HMM.inference_HMM(data_dir=ben_test_data_folder, model_name=model_dict[model]['model_name'], win_size=model_dict[model]['win_size'], feature_choice=model_dict[model]['feature_choice'])
    
    print('classification accuracy of {} is {}%'.format(model_dict[model]['model_name'], sum(label==predicted)/len(label)*100))
    print('mean: {}, std: {}'.format(score.mean(), score.std()))
    
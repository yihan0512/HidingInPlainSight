import os 
import sys
import argparse
import json
import subprocess

from SideChannelTesting import capture_arm_cw, NUM_PATHS
from SideChannelDetector import inference_Detector, parse_s, mal_list
from SideChannelDetector import inference_HMM

from utils.utils import program_reset, read_results


import ipdb


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='validate the detectors')
    parser.add_argument('--model', type=str, help='source model')
    parser.add_argument('--target-model', type=str, help='target model')
    parser.add_argument('--checkpoint', type=str, help='model checkpoint path')
    parser.add_argument('--collect', type=bool, help='collect data or not')
    parser.add_argument('--malware', type=str, help='specify which malware')
    args = parser.parse_args()


    num_paths = NUM_PATHS
    batch_size = 128 # change based on your gpu memory
    root_folder = os.getcwd() 
    testing_folder = os.path.join(root_folder, 'SideChannelTesting')
    detector_folder = os.path.join(root_folder, 'SideChannelDetector')
    data_folder = os.path.join(testing_folder, 'attack')

    source_dir = os.path.join(root_folder, 'firmware', 'simpleserial-main')
    seed_dir = os.path.join(source_dir, 'klee_ifelse.txt')

    checkpoint_dir = args.checkpoint
    model_dict_pth = os.path.join(checkpoint_dir, 'model.json')
    with open(model_dict_pth, 'r') as f:
        model_dict = json.load(f)
    model_dict['base']['model_name'] = checkpoint_dir
    model = 'base'

    # baseline score
    program_reset()
    ret = capture_arm_cw.capture_all(N=24, Nt=10, seed=seed_dir, root=data_folder, device_id=0)
    if ret:
        sys.exit()
    # BiLSTM
    if args.target_model == 'bilstm':
        score, label, predicted = inference_Detector.inference_BiLSTM(data_dir=data_folder, model_name=model_dict[model]['model_name'], input_size=model_dict[model]['input_size'], max_len=model_dict[model]['max_len'], hidden_size=model_dict[model]['hidden_size'], num_layers=model_dict[model]['num_layers'], num_classes=model_dict[model]['num_paths'], batch_size=batch_size, feature_choice=model_dict[model]['feature_choice'])
    # BiRNN
    elif args.target_model == 'birnn':
        score, label, predicted = inference_Detector.inference_BiRNN(data_dir=data_folder, model_name=model_dict[model]['model_name'], input_size=model_dict[model]['input_size'], max_len=model_dict[model]['max_len'], hidden_size=model_dict[model]['hidden_size'], num_layers=model_dict[model]['num_layers'], num_classes=model_dict[model]['num_paths'], batch_size=8, feature_choice=model_dict[model]['feature_choice'])
    # HMM
    elif args.target_model == 'hmm':
        score, label, predicted = inference_HMM.inference_HMM(data_dir=data_folder, model_name=model_dict[model]['model_name'], win_size=model_dict[model]['win_size'], feature_choice=model_dict[model]['feature_choice'])
    score_baseline = score.mean()
    print('baseline score is {}'.format(score_baseline))

    # inject the malware and collect data
    comb, _, _ = read_results(os.path.join('results', 'top1_'+args.model, model_dict[model]['feature_choice'], args.malware+'.txt'))
    asm = 'simpleserial-main.s'
    ret = parse_s.insert_malware_chunks(comb[0], asm, eval('mal_list.'+args.malware))
    if ret:
        print('failed to replace!')
        sys.exit()
    ret = capture_arm_cw.capture_all(N=num_paths, Nt=10, seed=seed_dir, root=data_folder, device_id=0)
    if ret:
        print('trigger missed!')
        sys.exit()
    

    # BiLSTM
    if args.target_model == 'bilstm':
        score, label, predicted = inference_Detector.inference_BiLSTM(data_dir=data_folder, model_name=model_dict[model]['model_name'], input_size=model_dict[model]['input_size'], max_len=model_dict[model]['max_len'], hidden_size=model_dict[model]['hidden_size'], num_layers=model_dict[model]['num_layers'], num_classes=model_dict[model]['num_paths'], batch_size=batch_size, feature_choice=model_dict[model]['feature_choice'])
    # BiRNN
    elif args.target_model == 'birnn':
        score, label, predicted = inference_Detector.inference_BiRNN(data_dir=data_folder, model_name=model_dict[model]['model_name'], input_size=model_dict[model]['input_size'], max_len=model_dict[model]['max_len'], hidden_size=model_dict[model]['hidden_size'], num_layers=model_dict[model]['num_layers'], num_classes=model_dict[model]['num_paths'], batch_size=8, feature_choice=model_dict[model]['feature_choice'])
    # HMM
    elif args.target_model == 'hmm':
        score, label, predicted = inference_HMM.inference_HMM(data_dir=data_folder, model_name=model_dict[model]['model_name'], win_size=model_dict[model]['win_size'], feature_choice=model_dict[model]['feature_choice'])
    
    print('normalized score: mean: {}, std: {}'.format((score/score_baseline).mean(), (score/score_baseline).std()))
    
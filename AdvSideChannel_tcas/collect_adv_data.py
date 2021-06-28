import os
from SideChannelDetector import mal_list, parse_s
from SideChannelTesting import capture_arm_cw, NUM_PATHS
from utils.utils import read_results

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='collect data for adversarial training purpose')
    parser.add_argument('--feature', default='time', type=str, help='which feature')
    args = parser.parse_args()

    root_folder = os.getcwd() 
    testing_folder = os.path.join(root_folder, 'SideChannelTesting')
    source_dir = os.path.join(root_folder, 'firmware', 'simpleserial-main')
    seed_dir = os.path.join(source_dir, 'klee_ifelse.txt')
    
    evading_samples_path = os.path.join('results', 'bilstm', args.feature)
    files = os.listdir(evading_samples_path)
    evading_samples = []
    for name in files:
        injections, _, _ = read_results(os.path.join(evading_samples_path, name))
        evading_samples += injections
        

    for i, comb in enumerate(evading_samples):
        save_path = os.path.join(testing_folder, 'adv_'+args.feature, str(i))
        os.makedirs(save_path, exist_ok=True)

        malware = mal_list.data_injection
        print(comb)
        # inject the chunks
        asm = 'simpleserial-main.s'
        ret = parse_s.insert_malware_chunks(comb, asm, malware)
        if ret:
            print("failed to replace!")
            # sys.exit()
            continue

        # capture signals
        ret = capture_arm_cw.capture_all(N=NUM_PATHS, Nt=10, seed=seed_dir, root=save_path, device_id=0)
        if ret:
            # print('{} not working!'.format(comb_name))
            print('trigger missed!')
            # sys.exit()
            continue
'''
split training and testing data for the adversarial class
'''
import os
import shutil
from random import shuffle
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='validate the detectors')
    parser.add_argument('--source', default='adv_time', type=str, help='source dir')
    args = parser.parse_args()

    source_dir = args.source
    dest_dir = 'dataset_'+args.source
    dest_train_dir = os.path.join(dest_dir, 'train')
    dest_test_dir = os.path.join(dest_dir, 'test')
    
    # first move benign samples
    os.makedirs(dest_dir, exist_ok=True)
    shutil.copytree('train', dest_train_dir)
    shutil.copytree('test', dest_test_dir)

    dataset_names = os.listdir(source_dir)
    ratio = 0.8

    samples = []
    for dataset in dataset_names:
        path_names = os.listdir(os.path.join(source_dir, dataset))
        for path in path_names:
            filenames = os.listdir(os.path.join(source_dir, dataset, path))
            if filenames:
                samples.append(os.path.join(source_dir, dataset, path, filenames[0]))


    num_train = round(ratio*len(samples))
    shuffle(samples)

    # move to train dataset
    os.makedirs(os.path.join(dest_train_dir, 'adv'), exist_ok=True)
    count = 0
    for sample in samples[:num_train]:
        # print('copying {}...'.format(sample))
        shutil.copyfile(sample, os.path.join(dest_train_dir, 'adv', 'adv_'+str(count)+'.npy'))
        count += 1

    # move to test dataset
    os.makedirs(os.path.join(dest_test_dir, 'adv'), exist_ok=True)
    count = 0
    for sample in samples[num_train:]:
        # print('copying {}...'.format(sample))
        shutil.copyfile(sample, os.path.join(dest_test_dir, 'adv', 'adv_'+str(count)+'.npy'))
        count += 1

        
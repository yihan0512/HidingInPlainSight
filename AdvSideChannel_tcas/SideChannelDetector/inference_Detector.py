import os
import glob
import argparse

import torch
import torch.nn as nn

from .CustomDataset.CustomDataset import SideChannelDetector 
from .CustomDataset import CustomDataset
from .model import BiLSTM, BiRNN

import ipdb

def inference_BiLSTM(data_dir, model_name, input_size, max_len, hidden_size, num_layers, num_classes, batch_size, feature_choice='time'):
    # os.chdir('/home/cspl/Documents/projects/HidingInPlainSight/AdvSideChannel_tcas/SideChannelDetector/')
    # device configuration
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # load model
    if feature_choice == 'time':
        model = BiLSTM(input_size, hidden_size, num_layers, num_classes).to(device)
    elif feature_choice == 'fft':
        model = BiLSTM(input_size//2+1, hidden_size, num_layers, num_classes).to(device)

    try:
        checkpoint = torch.load(glob.glob(os.path.join(model_name, 'best_val_snapshot*'))[0])
    except:
        ipdb.set_trace()
    # checkpoint = torch.load(model_name+'.ckpt', map_location='cpu')
    model.load_state_dict(checkpoint['model_state_dict'])

    # load data
    inference_dataset = SideChannelDetector(root=data_dir, max_len=max_len, win_size=input_size, feature_choice=feature_choice)
    inference_loader = torch.utils.data.DataLoader(dataset=inference_dataset, batch_size=batch_size, shuffle=False, collate_fn=CustomDataset.custom_collate)

    # evaluate model
    model.eval()
    with torch.no_grad():
        accu = [] 
        predicted_all = []
        labels_all = []
        output_all = []
        for images, labels in inference_loader:
            images_sorted, perm_idx = CustomDataset.sort_batch(images)
            images_packed = nn.utils.rnn.pack_padded_sequence(nn.utils.rnn.pad_sequence(images_sorted, batch_first=True), [v.size(0) for v in images_sorted], batch_first=True)
            images_packed = images_packed.to(device)
            labels_sorted = labels[perm_idx]
            labels_sorted = labels_sorted.to(device)
            # images = images.to(device)
            # labels = labels.to(device)
            output = model(images_packed, len(images))
            _, predicted = torch.max(output.softmax(dim=1), 1)
            predicted_all.append(predicted)
            labels_all.append(labels_sorted)
            output_all.append(output)
        predicted_all = torch.cat(predicted_all)
        labels_all = torch.cat(labels_all)
        output_all = torch.cat(output_all)
        # print('Overall accuracy: {:.2f}%'.format(accu*100))
        score = output_all.softmax(dim=1).max(dim=1)[0].cpu().numpy()

    return score, labels_all, predicted_all

def inference_BiLSTMAdv(data_dir, model_name, input_size, max_len, hidden_size, num_layers, num_classes, batch_size, feature_choice='time'):
    # os.chdir('/home/cspl/Documents/projects/HidingInPlainSight/AdvSideChannel_tcas/SideChannelDetector/')
    # device configuration
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # load model
    if feature_choice == 'time':
        model = BiLSTM(input_size, hidden_size, num_layers, num_classes).to(device)
    elif feature_choice == 'fft':
        model = BiLSTM(input_size//2+1, hidden_size, num_layers, num_classes).to(device)

    try:
        checkpoint = torch.load(glob.glob(os.path.join(model_name, 'best_val_snapshot*'))[0])
    except:
        ipdb.set_trace()
    # checkpoint = torch.load(model_name+'.ckpt', map_location='cpu')
    model.load_state_dict(checkpoint['model_state_dict'])

    # load data
    inference_dataset = SideChannelDetector(root=data_dir, max_len=max_len, win_size=input_size, feature_choice=feature_choice)
    inference_loader = torch.utils.data.DataLoader(dataset=inference_dataset, batch_size=batch_size, shuffle=False, collate_fn=CustomDataset.custom_collate)

    # ipdb.set_trace()


    # evaluate model
    model.eval()
    with torch.no_grad():
        accu = [] 
        predicted_all = []
        labels_all = []
        output_all = []
        for images, labels in inference_loader:
            images_sorted, perm_idx = CustomDataset.sort_batch(images)
            images_packed = nn.utils.rnn.pack_padded_sequence(nn.utils.rnn.pad_sequence(images_sorted, batch_first=True), [v.size(0) for v in images_sorted], batch_first=True)
            images_packed = images_packed.to(device)
            labels_sorted = labels[perm_idx]
            labels_sorted = labels_sorted.to(device)
            # images = images.to(device)
            # labels = labels.to(device)
            output = model(images_packed, len(images))
            _, predicted = torch.max(output.softmax(dim=1), 1)
            predicted_all.append(predicted)
            labels_all.append(labels_sorted)
            output_all.append(output)
        predicted_all = torch.cat(predicted_all)
        labels_all = torch.cat(labels_all)
        output_all = torch.cat(output_all)
        # print('Overall accuracy: {:.2f}%'.format(accu*100))
        score = -output_all.softmax(dim=1)[:, 0].log().cpu().numpy() # cross-entropy loss w.r.t. the adv class

    return score, labels_all, predicted_all

def inference_BiRNN(data_dir, model_name, input_size, max_len, hidden_size, num_layers, num_classes, batch_size, feature_choice='time'):
    # os.chdir('/home/cspl/Documents/projects/HidingInPlainSight/AdvSideChannel_tcas/SideChannelDetector/')
    # device configuration
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # load model
    if feature_choice == 'time':
        model = BiRNN(input_size, hidden_size, num_layers, num_classes).to(device)
    elif feature_choice == 'fft':
        model = BiRNN(input_size//2+1, hidden_size, num_layers, num_classes).to(device)

    try:
        checkpoint = torch.load(glob.glob(os.path.join(model_name, 'best_val_snapshot*'))[0])
    except:
        ipdb.set_trace()
    # checkpoint = torch.load(model_name+'.ckpt', map_location='cpu')
    model.load_state_dict(checkpoint['model_state_dict'])

    # load data
    inference_dataset = SideChannelDetector(root=data_dir, max_len=max_len, win_size=input_size, feature_choice=feature_choice)
    inference_loader = torch.utils.data.DataLoader(dataset=inference_dataset, batch_size=batch_size, shuffle=False, collate_fn=CustomDataset.custom_collate)


    # evaluate model
    model.eval()
    with torch.no_grad():
        accu = [] 
        predicted_all = []
        labels_all = []
        output_all = []
        for images, labels in inference_loader:
            images_sorted, perm_idx = CustomDataset.sort_batch(images)
            images_packed = nn.utils.rnn.pack_padded_sequence(nn.utils.rnn.pad_sequence(images_sorted, batch_first=True), [v.size(0) for v in images_sorted], batch_first=True)
            images_packed = images_packed.to(device)
            labels_sorted = labels[perm_idx]
            labels_sorted = labels_sorted.to(device)
            # images = images.to(device)
            # labels = labels.to(device)
            output = model(images_packed, len(images))
            _, predicted = torch.max(output.softmax(dim=1), 1)
            predicted_all.append(predicted)
            labels_all.append(labels_sorted)
            output_all.append(output)
        predicted_all = torch.cat(predicted_all)
        labels_all = torch.cat(labels_all)
        output_all = torch.cat(output_all)
        # print('Overall accuracy: {:.2f}%'.format(accu*100))
        score = output_all.softmax(dim=1).max(dim=1)[0].cpu().numpy()

    return score, labels_all, predicted_all


if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser(description='training BiRNNattn')
    parser.add_argument('--testing', type=str, help='Specify data dir')
    parser.add_argument('--nc', '--num-classes', default=50, type=int, help='Specify number of classes')
    parser.add_argument('--hs', '--hidden-size', default=128, type=int, help='Specify hidden size')
    parser.add_argument('--nl', '--num-layers', default=2, type=int, help='Specify number of layers')
    parser.add_argument('-b', '--batch-size', default=8, type=int, help='Specify number of layers')
    parser.add_argument('-i', '--input-size', default=4, type=int, help='Specify input size')
    parser.add_argument('--ml', '--max-len', default=900, type=int, help='Specify total sample length')
    arg = parser.parse_args()

    # inference_detector(arg.testing, arg.input_size, arg.ml, arg.hs, arg.nl, arg.nc, arg.batch_size) 

import os
import sys
sys.path.append(os.getcwd())

import torch
import torch.nn as nn
from torch.utils.data.dataset import Dataset
from torch.utils.tensorboard import SummaryWriter

from CustomDataset.CustomDataset import SideChannelDetector 
from CustomDataset import CustomDataset
from CheckpointWriter.CheckpointWriter import CheckpointWriter

import numpy as np
import argparse
from collections import Counter

from tqdm import trange
from tqdm import tqdm 

import ipdb

from model import BiLSTM

# # Bidirectional recurrent neural network (many-to-one)
# class BiRNN(nn.Module):
#     def __init__(self, input_size, hidden_size, num_layers, num_classes):
#         super(BiRNN, self).__init__()
#         self.hidden_size = hidden_size
#         self.num_layers = num_layers
#         self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, bidirectional=True, dropout=0.4)
#         # self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, bidirectional=True)
#         self.fc1 = nn.Linear(hidden_size*2, 128)  # 2 for bidirection
#         self.fc2 = nn.Linear(128, num_classes)
    
#     def forward(self, x, batch_size): #
#         # Set initial states
#         h0 = torch.zeros(self.num_layers*2, batch_size, self.hidden_size).to(torch.device('cuda' if torch.cuda.is_available() else 'cpu')) # 2 for bidirection 
#         c0 = torch.zeros(self.num_layers*2, batch_size, self.hidden_size).to(torch.device('cuda' if torch.cuda.is_available() else 'cpu'))

#         # pass to the blstm layer to get last hidden state
#         _, (hn, _) = self.lstm(x, (h0, c0)) # output size: tensor of shape (batch_size, seq_length, hidden_size&*2)

#         # concate final states
#         out = torch.cat((hn.view(self.num_layers, 2, batch_size, self.hidden_size)[1][0], hn.view(self.num_layers, 2, batch_size, self.hidden_size)[1][1]), 1)

#         # Decode the hidden state of the last time step
#         out = self.fc1(out)
#         out = self.fc2(out)
#         return out

if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser(description='training BiRNNattn')
    parser.add_argument('--lr', '--learning-rate', default=0.03, type=float, help='initial learning rate')
    parser.add_argument('-e', '--epochs', default=100, type=int, help='Specify number of epochs')
    parser.add_argument('-b', '--batch-size', default=128, type=int, help='Specify batch size')
    parser.add_argument('--wd', '--weight-decay', default=1e-5, type=int, help='Specify L2 norm coefficient')
    parser.add_argument('--training', default='data/train', type=str, help='Specify training dir')
    parser.add_argument('--testing', default='data/test', type=str, help='Specify testing dir')
    parser.add_argument('--nl', '--num-layers', default=2, type=int, help='Specify number of layers')
    parser.add_argument('--hs', '--hidden-size', default=128, type=int, help='Specify hidden size')
    parser.add_argument('-i', '--input-size', default=4, type=int, help='Specify input size')
    parser.add_argument('--ml', '--max-len', default=1200, type=int, help='Specify total sample length')
    parser.add_argument('-l', '--log', type=str, help='Specify expr dir')
    parser.add_argument('-f', '--feature', default='time', type=str, help='Specify feature choice')
    arg = parser.parse_args()

    # Device configuration
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    torch.manual_seed(99)

    # Hyper-parameters
    input_size = arg.input_size
    max_len = arg.ml
    hidden_size = arg.hs 
    num_layers = arg.nl
    batch_size = arg.batch_size
    num_epochs = arg.epochs
    learning_rate = arg.lr
    weight_decay = arg.wd
    train_folder = arg.training
    test_folder = arg.testing
    expr_log = arg.log
    feature_choice = arg.feature

    # print('Batch size: {}, Learning rate: {}'.format(batch_size, learning_rate))

    # load data
    train_dataset = SideChannelDetector(root=train_folder, max_len=max_len, win_size=input_size, feature_choice=feature_choice)
    train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True, collate_fn=CustomDataset.custom_collate)
    test_dataset = SideChannelDetector(root=test_folder, max_len=max_len, win_size=input_size, feature_choice=feature_choice)
    test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=False, collate_fn=CustomDataset.custom_collate)
    # Tensorboard
    writer = SummaryWriter(os.path.join('runs', expr_log))

    num_classes = len(train_dataset.classes)

    # checkpoint
    model_specs = {}
    model_specs['base'] = {}
    model_specs['base']['input_size'] = input_size
    model_specs['base']['max_len'] = max_len 
    model_specs['base']['hidden_size'] = hidden_size
    model_specs['base']['num_layers'] = num_layers
    model_specs['base']['num_paths'] = num_classes
    model_specs['base']['feature_choice'] = feature_choice
    checkpoint = CheckpointWriter(os.path.join('checkpoints', expr_log), model_specs)

    # create model
    if feature_choice == 'time':
        model = BiLSTM(input_size, hidden_size, num_layers, num_classes).to(device)
    elif feature_choice == 'fft':
        model = BiLSTM(input_size//2+1, hidden_size, num_layers, num_classes).to(device)
    else:
        print('wrong feature choice specified!')
        sys.exit()
        
    print(model)

    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate, weight_decay=weight_decay)
    # optimizer = torch.optim.SGD(model.parameters(), momentum=0.9, lr=learning_rate, weight_decay=1e-5)

    # Learning rate scheduler
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', verbose=True, patience=100)

    # Load snapshot model if available
    model, optimizer = checkpoint.load(model, optimizer)

    # if multiple GPUs
    if torch.cuda.device_count() > 1:
        print('Using {} GPUs!'.format(torch.cuda.device_count()))
        model = nn.DataParallel(model)

    # Train the model
    total_step = len(train_loader)
    best_val_accu = -1
    best_loss_val = 100
    loss_val = 100
    accuracy_val = 0
    t = trange(num_epochs, desc='{}, {}%'.format(loss_val, accuracy_val))
    for epoch in t:
        model.train()
        correct = 0
        for i, (images, labels) in enumerate(train_loader):
            images_sorted, perm_idx = CustomDataset.sort_batch(images)
            images_packed = nn.utils.rnn.pack_padded_sequence(nn.utils.rnn.pad_sequence(images_sorted, batch_first=True), [v.size(0) for v in images_sorted], batch_first=True)
            images_packed = images_packed.to(device)
            labels_sorted = labels[perm_idx]
            labels_sorted = labels_sorted.to(device)


            # images = images.to(device)
            # labels = labels.to(device)

            # Forward pass
            outputs = model(images_packed, len(images))
            loss = criterion(outputs, labels_sorted)
            
            # Backward and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()


            # calculate training accuracy
            _, predicted = torch.max(outputs.softmax(dim=1), dim=1)
            correct += (predicted == labels_sorted).sum()
        accuracy = 100 * torch.true_divide(correct, train_dataset.__len__()) 

        # Validate the model
        model.eval()
        with torch.no_grad():
            correct_val = 0
            for images, labels in test_loader:
                images_sorted, perm_idx = CustomDataset.sort_batch(images)
                images_packed = nn.utils.rnn.pack_padded_sequence(nn.utils.rnn.pad_sequence(images_sorted, batch_first=True), [v.size(0) for v in images_sorted], batch_first=True)
                images_packed = images_packed.to(device)
                labels_sorted = labels[perm_idx]
                labels_sorted = labels_sorted.to(device)
                # images = images.to(device)
                # labels = labels.to(device)
                outputs= model(images_packed, len(images))
                loss_val = criterion(outputs, labels_sorted)
                _, predicted = torch.max(outputs.softmax(dim=1), 1)
                correct_val += (predicted == labels_sorted).sum()
            accuracy_val = 100 * torch.true_divide(correct_val, test_dataset.__len__())

        # Learning rate adjustment
        scheduler.step(loss_val)

        # Report training status
        # print ('Epoch [{}/{}], Training Loss: {:.4f}, Training Accu: {:.2f}%, Validation Loss: {:.4f}, Validation Accu: {:.2f}%, LR: {:.6f}'.format(epoch+1, num_epochs, loss.item(), accuracy, loss_val.item(), accuracy_val, optimizer.param_groups[0]['lr']))

        # Tensorboard update
        writer.add_scalar('loss/train', loss.item(), epoch+1)
        writer.add_scalar('accuracy/train', accuracy, epoch+1)
        writer.add_scalar('loss/validation', loss_val.item(), epoch+1)
        writer.add_scalar('accuracy/validation', accuracy_val, epoch+1)
        writer.add_scalar('Learning rate', optimizer.param_groups[0]['lr'], epoch+1)

        # tqdm update
        t.set_description('{:.4f}, {:.2f}%'.format(loss_val.item(), accuracy_val))

        # Update model with best validation accuracy
        if loss_val < best_loss_val:
            best_loss_val = loss_val
            checkpoint.save(model, optimizer, accuracy_val, loss_val, epoch, loss)


        # # if accuracy_val > best_val_accu:
        # #     best_val_accu = accuracy_val
        #     snapshot_path = 'best_val_snapshot' + '_valacc_{}_valloss_{}_model.ckpt'.format(accuracy_val, loss_val)
        #     torch.save({
        #                 'epoch': epoch,
        #                 'model_state_dict': model.state_dict(),
        #                 'optimizer_state_dict': optimizer.state_dict(),
        #                 'loss': loss,
        #                 }, snapshot_path)
        #     for f in glob.glob('best_val_snapshot*'):
        #         if f != snapshot_path:
        #             os.remove(f)

    # close tensorboard
    writer.close()

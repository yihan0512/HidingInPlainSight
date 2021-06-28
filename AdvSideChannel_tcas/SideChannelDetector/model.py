import torch
import torch.nn as nn


# Bidirectional recurrent neural network (many-to-one)
class BiLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes):
        super(BiLSTM, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, bidirectional=True, dropout=0.4)
        # self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, bidirectional=True)
        self.fc1 = nn.Linear(hidden_size*2, 128)  # 2 for bidirection
        self.fc2 = nn.Linear(128, num_classes)
    
    def forward(self, x, batch_size): #
        # Set initial states
        h0 = torch.zeros(self.num_layers*2, batch_size, self.hidden_size).to(torch.device('cuda' if torch.cuda.is_available() else 'cpu')) # 2 for bidirection 
        c0 = torch.zeros(self.num_layers*2, batch_size, self.hidden_size).to(torch.device('cuda' if torch.cuda.is_available() else 'cpu'))

        # pass to the blstm layer to get last hidden state
        _, (hn, _) = self.lstm(x, (h0, c0)) # output size: tensor of shape (batch_size, seq_length, hidden_size&*2)

        # concate final states
        out = torch.cat((hn.view(self.num_layers, 2, batch_size, self.hidden_size)[1][0], hn.view(self.num_layers, 2, batch_size, self.hidden_size)[1][1]), 1)

        # Decode the hidden state of the last time step
        out = self.fc1(out)
        out = self.fc2(out)
        return out


class BiRNN(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes):
        super(BiRNN, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.rnn = nn.RNN(input_size, hidden_size, num_layers, batch_first=True, bidirectional=True, dropout=0.4)
        self.fc1 = nn.Linear(hidden_size*2, 128)  # 2 for bidirection
        self.fc2 = nn.Linear(128, num_classes)
    
    def forward(self, x, batch_size): #
        # Set initial states
        h0 = torch.zeros(self.num_layers*2, batch_size, self.hidden_size).to(torch.device('cuda' if torch.cuda.is_available() else 'cpu')) # 2 for bidirection 

        # pass to the blstm layer to get last hidden state
        _, hn = self.rnn(x, h0) # output size: tensor of shape (batch_size, seq_length, hidden_size&*2)

        # concate final states
        out = torch.cat((hn.view(self.num_layers, 2, batch_size, self.hidden_size)[1][0], hn.view(self.num_layers, 2, batch_size, self.hidden_size)[1][1]), 1)

        # Decode the hidden state of the last time step
        out = self.fc1(out)
        out = self.fc2(out)
        return out
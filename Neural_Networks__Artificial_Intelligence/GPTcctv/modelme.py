import math
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
from torch.nn.utils.rnn import pack_padded_sequence
from torch.nn.utils.rnn import pad_packed_sequence

class EncoderCNN(nn.Module):
    def __init__(self, embed_size):
        """Load the pretrained ResNet-152 and replace top fc layer."""
        super(EncoderCNN, self).__init__()
        resnet = models.resnet152(pretrained=True)
        modules = list(resnet.children())[:-1]      # delete the last fc layer.
        self.resnet = nn.Sequential(*modules)
        self.linear = nn.Linear(resnet.fc.in_features, embed_size)
        self.bn = nn.BatchNorm1d(embed_size, momentum=0.01)
        
    def forward(self, images):
        """Extract feature vectors from input images."""
        with torch.no_grad():
            features = self.resnet(images)
        features = features.reshape(features.size(0), -1)
        features = self.bn(self.linear(features))
        return features

class Attention(nn.Module):
    def __init__(self, encoder_dim, decoder_dim, attention_dim):
        super(Attention, self).__init__()
        self.encoder_att = nn.Linear(encoder_dim, attention_dim)
        self.decoder_att = nn.Linear(decoder_dim, attention_dim)
        self.full_att = nn.Linear(attention_dim, 1)
        self.relu = nn.ReLU()
        self.softmax = nn.Softmax(dim=2)

    def forward(self, encoder_out, decoder_hidden):
        att1 = self.encoder_att(encoder_out)  # (batch_size, 1, attention_dim)
        att2 = self.decoder_att(decoder_hidden)  # (batch_size, seq_len, attention_dim)
        att = self.full_att(self.relu(att1 + att2)).squeeze(2)  # (batch_size, seq_len)
        alpha = self.softmax(att)  # (batch_size, seq_len)
        attention_weighted_encoding = (encoder_out.unsqueeze(1) * alpha.unsqueeze(2)).sum(dim=1)  # (batch_size, encoder_dim)

        return attention_weighted_encoding, alpha

class DecoderRNN(nn.Module):
    def __init__(self, embed_size, hidden_size, vocab_size, num_layers, max_seq_length=20):
        super(DecoderRNN, self).__init__()
        self.embed = nn.Embedding(vocab_size, embed_size)
        self.lstm = nn.LSTM(embed_size, hidden_size, num_layers, batch_first=True)  # change here
        self.linear = nn.Linear(hidden_size, vocab_size)
        self.max_seg_length = max_seq_length
        self.attention = Attention(hidden_size, hidden_size, hidden_size)  # add attention here

    def forward(self, features, captions, lengths):
        embeddings = self.embed(captions)
        hiddens, _ = self.lstm(embeddings)
        hiddens = hiddens.unsqueeze(1)
        #new_hiddens = hiddens.resize(128, 256)
        #print("Shape of new hiddens: ", new_hiddens.shape)
        print("Shape of features: ", features.shape)
        print("Shape of hiddens: ", hiddens.shape)
        attn_weights = self.attention(features, hiddens)
        context = attn_weights.bmm(features.unsqueeze(1))  # (b, 1, n)
        hiddens = hiddens + context
        outputs = self.linear(hiddens.squeeze(1))
        return outputs
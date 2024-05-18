import os
import pickle
import argparse
import torch
from torch import nn 
from torchvision import models, transforms
from torch.utils.data import DataLoader, Dataset
from PIL import Image
from build_vocab import Vocabulary
from model import EncoderCNN, DecoderRNN


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model_path = 'models/'
fine_path = 'finetuning/models/'
another_path = 'finetuning/models/load'
with open('data/vocab.pkl', 'rb') as f:
    vocab = pickle.load(f)
vocab_size = len(vocab)
caption = 'a women in a white shirt defending from a man'


EPOCHS = 1
embed_size = 256
hidden_size = 512
num_layers = 1


class CustomDataset(Dataset):
    def __init__(self, image_folder, caption_folder, transform=None):
        self.image_folder = image_folder
        self.caption_folder = caption_folder
        self.transform = transform

    def __len__(self):
        return len(os.listdir(self.image_folder))
        #return 256

    def __getitem__(self, idx):
        img_name = os.path.join(self.image_folder, str(idx) + '.jpg')
        #img_name = os.path.join(self.image_folder, imagename + '.jpg')
        img = Image.open(img_name)

        transform = transforms.Compose([ 
            transforms.Resize((256,256)),
            #transforms.Grayscale(num_output_channels=1),
            #transforms.RandomHorizontalFlip(), 
            transforms.ToTensor(), 
            transforms.Normalize((0.485, 0.456, 0.406), 
                                (0.229, 0.224, 0.225))])

        img = transform(img)

        """img = torch.randn(256, 256)
        img.unsqueeze_(0)
        img = img.repeat(3, 1, 1)
        """
        def tokenize(caption, vocabulary):
            words = caption.split()
            tokens = [vocabulary(word) for word in words]
            return tokens
        tokenized_captions = tokenize(caption, vocab)

        #print("Image shape:", img.shape)
        return img, torch.tensor(tokenized_captions)

class FineTuneModel(nn.Module):
    def __init__(self, embed_size, hidden_size, vocab_size, num_layers):
        super(FineTuneModel, self).__init__()
        self.encoder = EncoderCNN(embed_size)
        self.decoder = DecoderRNN(embed_size,
                                  hidden_size,
                                  vocab_size,
                                  num_layers)

    def forward(self, images, captions, lengths):
        features = self.encoder(images)
        outputs = self.decoder(features, captions, lengths)
        return outputs


dataset = CustomDataset(image_folder='finetuning/images/',
                        caption_folder='finetuning/captions/',
                        transform=transforms.ToTensor())
dataloader = DataLoader(dataset, batch_size=1, shuffle=True, drop_last=False)

model = FineTuneModel(embed_size, hidden_size, vocab_size, num_layers)
model = model.to(device)

"""
encoder_path = os.path.join(model_path, 'encoder-5-3000.pkl'.format(3+1, 3+1))
decoder_path = os.path.join(model_path, 'decoder-5-3000.pkl'.format(3+1, 3+1))
#encoder_path = os.path.join(fine_path, 'encoder-1-1.ckpt'.format(3+1, 3+1))
#decoder_path = os.path.join(fine_path, 'decoder-1-1.ckpt'.format(3+1, 3+1))
encoder_path = os.path.join(another_path, 'encoder-1-1.ckpt'.format(3+1, 3+1))
decoder_path = os.path.join(another_path, 'decoder-1-1.ckpt'.format(3+1, 3+1))
assert os.path.exists(encoder_path), "Encoder model not found"
assert os.path.exists(decoder_path), "Decoder model not found"
model.encoder.load_state_dict(torch.load(encoder_path), strict=False)
model.decoder.load_state_dict(torch.load(decoder_path), strict=False)
"""

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)


for epoch in range(EPOCHS):
    model.train()
    total_loss = 0
    #model.eval()
    #torch.no_grad()

    for i, (images, captions) in enumerate(dataloader):
        images = images.to(device)
        captions = captions.to(device)

        lengths = [len(cap) for cap in captions]
        outputs = model(images, captions, lengths)
        
        loss = criterion(outputs.squeeze(0), captions.flatten())
        model.zero_grad()
        loss.backward()
        
        optimizer.step()

        total_loss += loss.item()
        print(f'Epoch [{epoch+1}/{EPOCHS}], Loss: {total_loss/len(dataloader)}')
        #print(f'Epoch [{epoch+1}/{EPOCHS}], Loss: {loss.item():.4f}')

    torch.save(model.decoder.state_dict(),
               os.path.join(fine_path,
                            'decoder-1-1.ckpt'))

    torch.save(model.encoder.state_dict(),
               os.path.join(fine_path,
                            'encoder-1-1.ckpt'))


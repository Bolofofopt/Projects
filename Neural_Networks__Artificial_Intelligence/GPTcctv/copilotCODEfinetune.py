import os
import torch
import pickle

from torch import nn 
from torchvision import models, transforms
from torch.utils.data import DataLoader, Dataset
from PIL import Image
from model import EncoderCNN, DecoderRNN
from build_vocab import Vocabulary
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model_path = 'models/'

EPOCHS = 1
embed_size = 256
hidden_size = 512 
num_layers = 1
captions = ["a women in a white shirt defending from a man"]
with open('data/vocab.pkl', 'rb') as f:
    vocab = pickle.load(f)
vocab_size = len(vocab)

"""
class CustomDataset(Dataset):
    def __init__(self, image_folder, caption_folder, transform=None):
        self.image_folder = image_folder
        self.caption_folder = caption_folder
        self.transofrm = transform

    def __len__(self):
        return len(os.listdir(self.image_folder))
    
    def __getitem__(self, idx):
        img_name = os.path.join(self.image_folder, str(idx) + '.jpg')
        img = Image.open(img_name)
        transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
            #FOR_NORMAL_IMAGES 
            #transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.255]),
            #Gray_Scale
            transforms.Normalize(mean=[0.5], std=[0.5]),
        ])
        img = transform(img)

        cap_name = os.path.join(self.caption_folder, str(idx) + '.txt')
        with open(cap_name, 'r') as f:
            caption = f.read()
        print("Image shape:", img.shape)
        print("Caption length:", len(caption))


        def tokenize(caption, vocabulary):
            words = caption.lower().split()
            tokens = [vocabulary(word) for word in words]
            return tokens
        
        tokenized_captions = [tokenize(caption, vocab) for caption in captions]

        return img, torch.tensor(tokenized_captions)
"""

class CustomDataset(Dataset):
    def __init__(self, image_folder, caption_folder, transform=None):
        self.image_folder = image_folder
        self.caption_folder = caption_folder
        self.transform = transform

    def __len__(self):
        return len(os.listdir(self.image_folder))
    
    def __getitem__(self, idx):
        img_name = os.path.join(self.image_folder, str(idx) + '.jpg')
        img = Image.open(img_name)
        if self.transform:
            img = self.transform(img)

        cap_name = os.path.join(self.caption_folder, str(idx) + '.txt')
        with open(cap_name, 'r') as f:
            caption = f.read().strip().lower().split()

        tokens = [vocab(word) for word in caption]
        print("Image shape:", img.shape)
        return img, torch.tensor(tokens).unsqueeze(0)

class FineTuneModel(nn.Module):
    def __init__(self, embed_size, hidden_size, vocab_size, num_layers):
        super(FineTuneModel, self). __init__()
        self.encoder = EncoderCNN(embed_size)
        self.decoder = DecoderRNN(embed_size, hidden_size, vocab_size, num_layers)

    def forward(self, images, captions, lengths):
        features = self.encoder(images)
        outputs = self.decoder(features, captions, lengths)
        return outputs




dataset = CustomDataset(image_folder='finetuning/images/', caption_folder='finetuning/captions/', transform=transforms.ToTensor())
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

model = FineTuneModel(embed_size, hidden_size, vocab_size, num_layers)
# model.
model = model.to(device)

encoder_path = os.path.join(model_path, 'encoder-5-3000.pkl'.format(3+1, 3+1))
decoder_path = os.path.join(model_path, 'decoder-5-3000.pkl'.format(3+1, 3+1))
assert os.path.exists(encoder_path), "Encoder model not found"
assert os.path.exists(decoder_path), "Decoder model not found"
model.encoder.load_state_dict(torch.load(encoder_path))
model.decoder.load_state_dict(torch.load(decoder_path))

model.train()
model.eval()


for param in model.parameters():
    param.requires_grad = True


criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)


for epoch in range(EPOCHS):
    for i, (images, captions) in enumerate(dataloader):
        images = images.to(device)
        captions = captions.to(device)
        print("Captions shape: ", captions.shape)

        lengths = [len(cap) for cap in captions]
        outputs = model(images, captions, lengths)

        captions = captions.view(-1)
        outputs = outputs.view(-1, outputs.size(-1))
        print("Reshaped captions shape: ", captions.shape)
        print("Reshaped outputs shape: ", outputs.shape)


        if outputs.size(0) != captions.size(0):
            outputs = outputs[:captions.size(0), :]
            print("Trimmed outputs shape: ", outputs.shape)


        loss = criterion(outputs.squeeze(0), captions.flatten())

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    print(f'Epoch [{epoch+1}/{EPOCHS}], Loss: {loss.item():.4f}')
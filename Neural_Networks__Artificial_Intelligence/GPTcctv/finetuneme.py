import os
import pickle
import argparse
import torch
from torch import nn 
from torchvision import models, transforms
from torch.utils.data import DataLoader, Dataset
from torch.nn.utils.rnn import pad_sequence
from torch.nn.utils.rnn import pack_padded_sequence
#from torch.nn.utils.rnn import pack_padded_sequence
from PIL import Image
from build_vocab import Vocabulary
from modelfinetune import EncoderCNN, DecoderRNN
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 0 e 1 são os nomes das imagens
image_to_caption = {
    '0': ['a women in a white shirt fighting a man',
            'a man touching a women',
            'a man assaulting a women'],
    #'1': ['asd', 'asd']
}


def main(args):
    with open(args.vocab_path, 'rb') as f:
        vocab = pickle.load(f)
    vocab_size = len(vocab) #buscar o vocabulario

    transform = transforms.Compose([ 
                transforms.Resize((args.crop_size)),
                transforms.Grayscale(num_output_channels=3),
                transforms.RandomHorizontalFlip(), 
                transforms.ToTensor(), 
                transforms.Normalize((0.485, 0.456, 0.406),
                                     (0.229, 0.224, 0.225))])
    #transformar a imagem e também transformar em RBG através do transforms.Grayscale

    #Buscar as imagens, transforma-las e vetorizar as legendas
    class CustomDataset(Dataset):
        def __init__(self, image_folder, image_to_caption):
            self.image_folder = image_folder
            self.image_to_captions = image_to_caption
            self.transform = transform
            self.images_names = sorted(os.listdir(self.image_folder))

        def __len__(self):
            return len(os.listdir(self.image_folder))

        def __getitem__(self, idx):
            img_name = os.path.join(self.image_folder, self.images_names[idx])
            img = Image.open(img_name)
            img = transform(img)

            def tokenize(caption, Vocabulary):
                words = caption.split()
                tokens = []
                for word in words:
                    if word in Vocabulary.word2idx: # Adiciona a palavra ao vocabulário
                        tokens.append(Vocabulary(word))
                return tokens

            captions = self.image_to_captions[str(idx)]
            tokenized_captions = [torch.tensor(tokenize(caption, vocab)) for caption in captions]
            tokenized_captions = pad_sequence(tokenized_captions, batch_first=True)

            return img, tokenized_captions

    #Load do modelo localizado no outro ficheiro
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


    dataset = CustomDataset(image_folder=args.image_folder,
                            image_to_caption=image_to_caption)

    dataloader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True, drop_last=False)

    model = FineTuneModel(args.embed_size, args.hidden_size, vocab_size, args.num_layers)
    model = model.to(device)

    """
    encoder_path = os.path.join(args.model_path, 'encoder-5-3000.pkl'.format(3+1, 3+1))
    decoder_path = os.path.join(args.model_path, 'decoder-5-3000.pkl'.format(3+1, 3+1))
    #encoder_path = os.path.join(fine_path, 'encoder-1-1.ckpt'.format(3+1, 3+1))
    #decoder_path = os.path.join(fine_path, 'decoder-1-1.ckpt'.format(3+1, 3+1))
    #encoder_path = os.path.join(args.another_path, 'encoder-1-1.ckpt'.format(3+1, 3+1))
    #decoder_path = os.path.join(args.another_path, 'decoder-1-1.ckpt'.format(3+1, 3+1))
    assert os.path.exists(encoder_path), "Encoder model not found"
    assert os.path.exists(decoder_path), "Decoder model not found"
    model.encoder.load_state_dict(torch.load(encoder_path), strict=False)
    model.decoder.load_state_dict(torch.load(decoder_path), strict=False)
    """

    # Preparação para o treino
    criterion = nn.CrossEntropyLoss()

    optimizer = torch.optim.Adam(model.parameters(), lr=args.learning_rate)

    # Começo do treino
    for epoch in range(args.num_epochs):
        model.train()
        total_loss = 0
        for i, (images, captions) in enumerate(dataloader):
            images = images.to(device)
            captions = captions.to(device)

            lengths = [len(cap) for cap in captions]
            outputs = model(images, captions, lengths)

            print("\nBefore Outputs size: ", outputs.size(),
                  "\nBefore Captions size: ", captions.size())

            linear = nn.Linear(9948, 9).to(device)
            outputs = linear(outputs)

            outputs = outputs.unsqueeze(0)
            #captions = captions.view(3, 9)
            #outputs = outputs.view(3, 9)
            print("\nAfter Outputs size: ", outputs.size(),
                  "\nAfter Captions size: ", captions.size(),
                  "\nAfter Outputs shape: ", outputs.shape,
                  "\nAfter Captions shape: ", captions.shape,
                  "\n")

            captions = captions.to(dtype=torch.float32)
            loss = criterion(outputs, captions)

            print("\nLast Outputs size: ", outputs.size(),
                  "\nLast Captions size: ", captions.size(),
                  "\n \n")

            #outputs = outputs.unsqueeze(0)
            model.zero_grad()
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            print(f'Epoch [{epoch+1}/{args.num_epochs}], Loss: {total_loss/len(dataloader)}')

        torch.save(model.decoder.state_dict(),
                os.path.join(args.fine_path,
                             'decoder-1-1.ckpt'))

        torch.save(model.encoder.state_dict(),
                os.path.join(args.fine_path,
                             'encoder-1-1.ckpt'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', type=str, default='models/' ,
                        help='path for saving loading coco trainedmodels')
    parser.add_argument('--fine_path', type=str, default='finetuning/models/' ,
                        help='path for saving trained fine-tuned models')
    parser.add_argument('--load_path', type=str, default='finetuning/models/load/' ,
                        help='path for loading trained fine-tuned models')

    parser.add_argument('--image_folder', type=str, default='finetuning/images/' ,
                        help='path for loading images for training purposes')

    parser.add_argument('--crop_size', type=int, default=224 , help='size for randomly cropping images')
    parser.add_argument('--embed_size', type=int , default=256, help='dimension of word embedding vectors')
    parser.add_argument('--hidden_size', type=int , default=512, help='dimension of lstm hidden states')
    parser.add_argument('--num_layers', type=int , default=1, help='number of layers in lstm')
    parser.add_argument('--batch_size', type=int, default=1, help='batch size')
    parser.add_argument('--learning_rate', type=float, default=0.001)

    parser.add_argument('--vocab_path', type=str, default='data/vocab.pkl', help='path for vocabulary wrapper')
    parser.add_argument('--encoder_path', type=str, default='finetuning/models/encoder-1-1.ckpt', help='path for trained encoder')
    parser.add_argument('--decoder_path', type=str, default='finetuning/models/decoder-1-1.ckpt', help='path for trained decoder')

    parser.add_argument('--num_epochs', type=int, default=5)

    args = parser.parse_args()
    print(args)
    main(args)



#params = list(decoder.parameters()) + list(encoder.linear.parameters()) + list(encoder.bn.parameters())

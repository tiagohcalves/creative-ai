import os

from autoencoder.batchify import get_batches
from autoencoder.model import *
from autoencoder.utils import *
from autoencoder.vocab import Vocab


class TrainedAutoEncoder:
    def __init__(self, checkpoint_path, seed=42):
        set_seed(seed)

        self.device = torch.device("cpu")
        self.vocab = Vocab(os.path.join(checkpoint_path, 'vocab.txt'))
        self.model = self.get_model(os.path.join(checkpoint_path, 'model.pt'))

    def get_model(self, path):
        ckpt = torch.load(path, map_location="cpu")
        print("Model loaded.")

        train_args = ckpt['args']
        model = {
            'dae': DAE, 'vae': VAE, 'aae': AAE
        }[train_args.model](self.vocab, train_args)

        model.load_state_dict(ckpt['model'])
        model.flatten()
        model.eval()
        return model

    def calc_ppl(self, sents, m, batch_size=256):
        batches, _ = get_batches(sents, self.vocab, batch_size, self.device)
        total_nll = 0
        with torch.no_grad():
            for inputs, targets in batches:
                total_nll += self.model.nll_is(inputs, targets, m).sum().item()
        n_words = sum(len(s) + 1 for s in sents)  # include <eos>
        return total_nll / len(sents), np.exp(total_nll / n_words)

    def encode(self, sents, enc="mu", batch_size=256):
        batches, order = get_batches(sents, self.vocab, batch_size, self.device)
        z = []
        for inputs, _ in batches:
            mu, logvar = self.model.encode(inputs)
            if enc == 'mu':
                zi = mu
            else:
                zi = reparameterize(mu, logvar)
            z.append(zi.detach().cpu().numpy())
        z = np.concatenate(z, axis=0)
        z_ = np.zeros_like(z)
        z_[np.array(order)] = z
        return z_

    def decode(self, z, dec="greedy", max_len=35, batch_size=256):
        sents = []
        i = 0
        while i < len(z):
            zi = torch.tensor(z[i: i+batch_size])
            outputs = self.model.generate(zi, max_len, dec).t()
            for s in outputs:
                sents.append([self.vocab.idx2word[i] for i in s[1:]])  # skip <go>
            i += batch_size
        return strip_eos(sents)

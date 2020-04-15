"""Download and pre-process GloVe.

Author:
    Chris Chute (chute@stanford.edu)
    Ashwin Paranjape (ashwinp@cs.stanford.edu)
"""

import numpy as np
import os
import urllib.request

from codecs import open
from collections import Counter
from tqdm import tqdm
from zipfile import ZipFile

def download_url(url, output_path, show_progress=True):
    class DownloadProgressBar(tqdm):
        def update_to(self, b=1, bsize=1, tsize=None):
            if tsize is not None:
                self.total = tsize
            self.update(b * bsize - self.n)

    if show_progress:
        # Download with a progress bar
        with DownloadProgressBar(unit='B', unit_scale=True,
                                 miniters=1, desc=url.split('/')[-1]) as t:
            urllib.request.urlretrieve(url,
                                       filename=output_path,
                                       reporthook=t.update_to)
    else:
        # Simple download with no progress bar
        urllib.request.urlretrieve(url, output_path)

def url_to_data_path(url):
    return os.path.join('./data/', )

class Embedding():
    def __init__(self, url, dim, vocab=None):
        """
        Initialize the Embedding class.

        Arguments
        ---------
        url: str
            Url to download the Embeddings file from

        vocab: Set[str]
            Set of tokens specifying the subset of embeddings to keep in memory

        Supports reading from glove-like file format and keeps a subset of embeddings in memory for fast-access
        """

        self.url = url
        if vocab is not None:
            self.vocab = set(vocab)
        else:
            self.vocab = None
        self.OOV = "--OOV--"
        self.dim = dim
        self.download()
        self.load()

    def download(self):
        """Download the embeddings file and extract it
        """

        url = self.url
        output_path = url.split('/')[-1]
        if not os.path.exists(output_path):
            print('Downloading {}...'.format(output_path))
            download_url(url, output_path)

        if os.path.exists(output_path) and output_path.endswith('.zip'):
            extracted_path = output_path.replace('.zip', '')
            if not os.path.exists(extracted_path):
                print('Unzipping {}...'.format(output_path))
                with ZipFile(output_path, 'r') as zip_fh:
                    zip_fh.extractall(extracted_path)
        self.emb_folder = extracted_path
        self.emb_file = os.path.join(self.emb_folder,self.emb_folder+"."+str(self.dim)+"d.txt")

    def load(self):
        """Load a subset (self.vocab) of embeddings into memory"""
        print("Pre-processing {} vectors...".format(self.emb_file))

        embedding_dict = {}
        with open(self.emb_file, "r") as fh:
            for line in fh:
                array = line.split()
                word = array[0]
                vector = np.array(list(map(float, array[1:])))
                if self.vocab is not None:
                    if word in self.vocab:
                        embedding_dict[word] = vector
                else:
                    embedding_dict[word] = vector
            if self.vocab is not None:
                print("{} / {} tokens have corresponding embedding vector".format(len(embedding_dict), len(self.vocab)))
            else:
                print("{} tokens have corresponding embedding vector".format(len(embedding_dict)))
        embedding_dict[self.OOV] = np.array([0. for _ in range(self.dim)])

        self.embeddings = embedding_dict

    def __getitem__(self, token):
        if token in self.embeddings:
            return self.embeddings[token]
        else:
            return self.embeddings[self.OOV]

if __name__ == '__main__':
    # Get command-line args
    glove_url = 'http://nlp.stanford.edu/data/glove.6B.zip'
    embedding = Embedding(glove_url, 100, vocab=set(['a', 'an']))
    print(embedding['a'])
    print(embedding['an'])
    print(embedding['the'])
    print(embedding['laksdjflaskfdjalskdfj'])

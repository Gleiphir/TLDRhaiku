import torchtext
import torch
from torchtext.data.utils import get_tokenizer
from collections import Counter
from torchtext.vocab import Vocab
from torchtext.utils import download_from_url, extract_archive
import io
import numpy as np
from tqdm import tqdm

import random

from torch.utils.data.dataset import Dataset

"""
L and R

A. vital elements - noun
B. connection - in pretrained BERT
entailment: should be same in both,  loss =  Entropy
controversial: should be differed in both,loss = -Entropy
neutral : loss =  Entropy

loss = loss / ( num_of_vital_elements_over_P  /  num_of_tokens_in_s)
*more vitals got = better

"""

P = 0.7 # confirm line


TEXTSEQLEN = 80
NUM_TOKENS = 65536




def fixlen(orig:list):
    fix = np.vectorize(lambda n: n if n != NUM_TOKENS else 0)
    lens = [len(l) for l in orig]
    data = np.full( (len(orig),TEXTSEQLEN),NUM_TOKENS )
    Mask = np.arange(TEXTSEQLEN) < np.array(lens)[:, None]
    data[Mask] = np.concatenate(orig)
    return torch.LongTensor(fix(data)),torch.BoolTensor(Mask)



dataset_path = r"merged.txt"

class token_dataset:
    def __init__(self,filepath):
        self.ja_tokenizer = get_tokenizer('spacy', language='ja_core_news_sm')
        self.dataset_fp = filepath

        self.jp_vocab = self.build_vocab(filepath, self.ja_tokenizer)

        print("Num of tokens:",len(self.jp_vocab))
        self.data = {}
        self.read_fp()
        print(len(self.data.keys()))
        print("Missing Keys:",[key for key in range(len(self.data.keys())) if key not in self.data.keys()])


    def read_fp(self):
        with open(self.dataset_fp,encoding='utf-8') as Fp:
            for ln in Fp.readlines():
                idx_, text = ln.split('|')
                idx = int(idx_)
                if not idx in self.data:
                    self.data[idx] = []
                self.data[idx].append(text)

    def build_vocab(self,filepath, tokenizer):
        counter = Counter()
        with io.open(filepath, encoding="utf8") as f:
          for string_ in f:
            counter.update(tokenizer(string_))
        return Vocab(counter, specials=['<unk>', '<BOS>', '<EOS>', '<PAD>'])

    def getRand(self, idx):
        raw = random.choice(self.data[idx])
        return [self.jp_vocab[token] for token in self.ja_tokenizer(raw)]

    def getAll(self,idx):
        return [[self.jp_vocab[token] for token in self.ja_tokenizer(s)] for s in self.data[idx] ]

    def maxLen(self):
        Max = 0
        tokens = None
        for key in self.data:
            for s in self.data[key]:
                if len(self.ja_tokenizer(s)) > Max:
                    Max = len(self.ja_tokenizer(s))
                    tokens = [token for token in self.ja_tokenizer(s)]
        print(tokens)
        return Max

    def tokenizeList(self,raw:str):
        return [self.jp_vocab['<BOS>']] + [self.jp_vocab[token] for token in self.ja_tokenizer(raw)] + [self.jp_vocab['<EOS>']]



if __name__ =='__main__':
    tokenDset = token_dataset('./merged-smallsample.txt')
    test_text = ["犬が地面に寝そべっている写真","白い犬が道路と自転車で寝ている"]
    print(tokenDset.tokenizeList(test_text[0]))
    textToken, mask = fixlen( [ tokenDset.tokenizeList(test_text[0]) ] )
    print(textToken)
    print(mask)
    textToken, mask = fixlen([tokenDset.tokenizeList(test_text[1])])
    print(textToken)
    print(mask)

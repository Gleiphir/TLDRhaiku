from pathlib import Path

import numpy as np
import torch
from transformers import BertTokenizer, BertModel
from pyknp import Juman
import csv

bert_model_path = "/mnt/Pretrained/jacobzh/Japanese_L-12_H-768_A-12_E-30_BPE_transformers"

tsv_file = open(r"jsnli_1.1/dev.tsv",encoding='utf-8')
read_tsv = csv.reader(tsv_file, delimiter="\t")
i = 0
L= [ [],[] ]
for row in read_tsv:
    if row[0] != 'entailment': continue
    for i in (0,1):
        L[i].extend( [ w for w in row[i+1].split(" ") if w != '' ] )
    i+=1
    if i> 10:
        break
tsv_file.close()

token_text = " ".join(L[0]+L[1])

class JumanTokenizer():
    def __init__(self):
        self.juman = Juman()

    def tokenize(self, text):
        result = self.juman.analysis(text)
        return [mrph.midasi for mrph in result.mrph_list()]


class BertWithJumanModel():
    def __init__(self, bert_path, vocab_file_name="vocab.txt", use_cuda=True):
        #self.juman_tokenizer = JumanTokenizer()
        self.model = BertModel.from_pretrained(bert_path)
        self.bert_tokenizer = BertTokenizer.from_pretrained(bert_path)
        """
        self.bert_tokenizer = BertTokenizer(Path(bert_path) / vocab_file_name,
                                            do_lower_case=False, do_basic_tokenize=False)
        """
        self.use_cuda = use_cuda

    def _preprocess_text(self, text):
        return text.replace(" ", "")  # for Juman

    def get_sentence_embedding(self, text, pooling_layer=-2, pooling_strategy="REDUCE_MEAN"):
        #preprocessed_text = self._preprocess_text(text)
        #tokens = self.juman_tokenizer.tokenize(preprocessed_text)
        #bert_tokens = self.bert_tokenizer.tokenize(" ".join(tokens))
        bert_tokens = self.bert_tokenizer.tokenize(text, return_tensors="pt")
        ids = self.bert_tokenizer.convert_tokens_to_ids(["[CLS]"] + bert_tokens[:126] + ["[SEP]"]) # max_seq_len-2
        tokens_tensor = torch.tensor(ids).reshape(1, -1)
        print(tokens_tensor)
        if self.use_cuda:
            tokens_tensor = tokens_tensor.to('cuda')
            self.model.to('cuda')

        self.model.eval()
        with torch.no_grad():
            output = self.model(tokens_tensor)
            #all_encoder_layers, _ = self.model(tokens_tensor)
        print(output.last_hidden_state.size())

        #embedding = all_encoder_layers[pooling_layer].cpu().numpy()[0]
        embedding = output.last_hidden_state.cpu().numpy()[0]
        if pooling_strategy == "REDUCE_MEAN":
            return np.mean(embedding, axis=0)
        elif pooling_strategy == "REDUCE_MAX":
            return np.max(embedding, axis=0)
        elif pooling_strategy == "REDUCE_MEAN_MAX":
            return np.r_[np.max(embedding, axis=0), np.mean(embedding, axis=0)]
        elif pooling_strategy == "CLS_TOKEN":
            return embedding[0]
        else:
            raise ValueError("specify valid pooling_strategy: {REDUCE_MEAN, REDUCE_MAX, REDUCE_MEAN_MAX, CLS_TOKEN}")


if __name__ == "__main__":
    mdl = BertWithJumanModel(bert_model_path)
    print(mdl.get_sentence_embedding("二 人 の 男 が 家 の 列 の 後ろ に いる 見物人 の グループ に 話し かけて い ます",pooling_strategy="CLS_TOKEN").shape)
    print(mdl.get_sentence_embedding("２ 匹 の 犬 が 店 の 外 で 縛ら れて おり 、 自転車 が 店 の 壁 に もたれ かかって い ます ",pooling_strategy="CLS_TOKEN").shape)
import csv
import collections
from pyknp import KNP
knp = KNP(jumanpp=False)     # Default is JUMAN++. If you use JUMAN, use KNP(jumanpp=False)

import time

def similarity(a:list,b:list):
    A = set(a)
    B = set(b)
    return len(A & B) / len( A | B)

tsv_file = open(r"jsnli_1.1/train_wo_filtering.tsv",encoding='utf-8')
read_tsv = csv.reader(tsv_file, delimiter="\t")
out_file = open(r"jsnli_1.1/out_train_wo_filtering.tsv","w",encoding='utf-8')
writer = csv.writer(out_file, delimiter="\t")
text = []
parts_original = []
parts_resplit = []

def reparse(S:str):
    global knp
    result = knp.parse(S.replace(" ",""))
    tags = [tag for tag in result.tag_list()]
    L = []
    for tag in tags:
        L.extend([mrph.midasi for mrph in tag.mrph_list()])
    return " ".join(L)
start_t = time.time()

i =0
for row in read_tsv:
    #if row[0] == 'contradiction':continue
    writer.writerow([row[0][0],reparse(row[1]),reparse(row[2])])
    #result = knp.parse(row.replace)
    #parts = [mrph.midasi for mrph in tag.mrph_list() for tag in result.tag_list()]
    i+=1
    if i%10 == 9:
        print("# {} - {}".format(i,time.time() -start_t))

out_file.close()

tsv_file.close()



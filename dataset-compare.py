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
text = []
parts_original = []
parts_resplit = []
i=0
for row in read_tsv:
    if row[0] == 'contradiction':continue
    text.append(row[1].replace(" ", ""))
    parts_original.append(row[1].split(' '))
    text.append(row[2].replace(" ", ""))
    parts_original.append(row[2].split(' '))
    #result = knp.parse(row.replace)
    #parts = [mrph.midasi for mrph in tag.mrph_list() for tag in result.tag_list()]
    i = i+1
    #print(row)
    #if i>350:break
print(len(text))
start = time.time()
for i,row in enumerate(text):
    if i % 100 == 0:
        now = time.time()
        print(" {} / {}, time used:{} ".format(i,len(text),now - start))
    parts = []

    result = knp.parse(row)
    """
    except Exception as e:
        print(e)
        print(row)
        input()
    """
    tags = [tag for tag in result.tag_list()]
    for tag in tags:
        parts.extend([mrph.midasi for mrph in tag.mrph_list() ])

    parts_resplit.append(parts)

tsv_file.close()

print("read")

simS = []

for j in range(i):
    X = similarity(parts_original[j], parts_resplit[j])
    simS.append(X)
    if X < 1:
        print(text[j])
        print(parts_original[j])
        print(parts_resplit[j])

print(sum(simS) / len(simS))


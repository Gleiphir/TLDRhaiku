import csv

tsv_file = open(r"jsnli_1.1/dev.tsv",encoding='utf-8')
read_tsv = csv.reader(tsv_file, delimiter="\t")
i = 0
for row in read_tsv:
    print(row)
    i = i+1
    if i>1000:break
tsv_file.close()
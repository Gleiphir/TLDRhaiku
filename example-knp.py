
from __future__ import unicode_literals # It is not necessary when you use python3.
from pyknp import KNP
knp = KNP(jumanpp=False)     # Default is JUMAN++. If you use JUMAN, use KNP(jumanpp=False)
result = knp.parse("閉鎖された場所にいるキリンを見ている人がいる")

print("文節")
for bnst in result.bnst_list(): # 各文節へのアクセス
    print("\tID:%d, 見出し:%s, 係り受けタイプ:%s, 親文節ID:%d, 素性:%s" \
            % (bnst.bnst_id, "".join(mrph.midasi for mrph in bnst.mrph_list()), bnst.dpndtype, bnst.parent_id, bnst.fstring))

print("基本句")
for tag in result.tag_list(): # 各基本句へのアクセス
    print("\tID:%d, 見出し:%s, 係り受けタイプ:%s, 親基本句ID:%d, 素性:%s" \
            % (tag.tag_id, "".join(mrph.midasi for mrph in tag.mrph_list()), tag.dpndtype, tag.parent_id, tag.fstring))

print("形態素")
for mrph in result.mrph_list(): # 各形態素へのアクセス
    print("\tID:%d, 見出し:%s, 読み:%s, 原形:%s, 品詞:%s, 品詞細分類:%s, 活用型:%s, 活用形:%s, 意味情報:%s, 代表表記:%s" \
            % (mrph.mrph_id, mrph.midasi, mrph.yomi, mrph.genkei, mrph.hinsi, mrph.bunrui, mrph.katuyou1, mrph.katuyou2, mrph.imis, mrph.repname))
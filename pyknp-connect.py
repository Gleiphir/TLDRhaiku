from pyknp import KNP

def select_normalization_representative_notation(fstring):
    """ 正規化代表表記を抽出します
    """
    begin = fstring.find('正規化代表表記:')
    end = fstring.find('/', begin + 1)
    return fstring[begin + len('正規化代表表記:') : end]

def select_dependency_structure(line):
    """係り受け構造を抽出します
    """

    # KNP
    knp = KNP(option = '-tab -anaphora',jumanpp=False)

    # 解析
    result = knp.parse(line)
    print("#")
    # 文節リスト
    bnst_list = result.bnst_list()

    # 文節リストをidによるディクショナリ化する
    bnst_dic = dict((x.bnst_id, x) for x in bnst_list)
    tuples = []
    for bnst in bnst_list:

        if bnst.parent_id != -1:
            print(bnst_dic[bnst.parent_id].fstring)
            # (from, to)
            tuples.append((select_normalization_representative_notation(bnst.fstring), select_normalization_representative_notation(bnst_dic[bnst.parent_id].fstring)))

    return tuples


if __name__ == '__main__' :
    line = '太郎は花子が読んでいる本を次郎に渡した'
    tuples = select_dependency_structure(line)

    for t in tuples:
        print(t[0] + ' => ' + t[1])
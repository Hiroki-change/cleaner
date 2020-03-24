import MeCab
import pandas as pd
import re
import os
import glob

base = os.path.dirname(os.path.abspath(__file__))#現在のディレクトリ
file_path = os.path.normpath(os.path.join(base, '../work/fin/*-m.txt'))
pkl_path1 = os.path.normpath(os.path.join(base, '../pkl/add_noun.pkl'))
pkl_path2 = os.path.normpath(os.path.join(base, '../pkl/add_one.pkl'))
add_word = pd.read_pickle(pkl_path1)
add_one = pd.read_pickle(pkl_path2)


def wakati(s): #分かち書き、形態素解析
    m = MeCab.Tagger ("-Owakati")
    mecab = MeCab.Tagger()
    m.parse("")
    wt = m.parse(s)
    parse = mecab.parse(s)
    lines = parse.split('\n')
    wt = wt.split(" ")
    #助詞を除く
    items = (re.split('[\t,]', line) for line in lines)

    # 名詞をリストに格納
    words = [item[0]
         for item in items
         if (item[0] not in ('EOS', '', 't', 'ー') and
             item[1] == '名詞')]
    words = set(words)

    return wt, words

files =glob.glob(file_path)
add_word = []
add_one = []

for file in files:
    with open (file, 'r') as f: #作業テキスト読み込み
        txt = f.read()

    ss, words = wakati(txt)

    bd_word = [i for i in words if not i.isdecimal() and len(i) >= 2]#数字と一文字を抜く
    add = [(ss[i-1] + x) for i,x in enumerate(ss) if ((i != 0) and ((len(x) + len(ss[i-1])) == len(x)+1))]
    add_word = add_word + bd_word
    add_one = add_one + add

add_word = set(add_word)
add_one = set(add_one)
pd.to_pickle(add_word, pkl_path1)
pd.to_pickle(add_one, pkl_path2)

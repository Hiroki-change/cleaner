import sys
import os
import glob
import jaconv
import pandas as pd
import re
import MeCab
import logging
import time
import cgitb
import csv
import html
import chardet

####################################################################
base = os.path.dirname(os.path.abspath(__file__))#現在のディレクトリ
file_path = os.path.normpath(os.path.join(base, '../work/pre_work/*.txt'))
working_path = os.path.normpath(os.path.join(base, '../work/working/*.txt'))

########################################################################
#pklファイル
#pkl_path1 = os.path.normpath(os.path.join(base, '../pkl/char.pkl'))
pkl_path2 = os.path.normpath(os.path.join(base, '../pkl/TANGO1000.pkl'))
pkl_path3 = os.path.normpath(os.path.join(base, '../pkl/word.pkl'))
pkl_path4 = os.path.normpath(os.path.join(base, '../pkl/add_noun.pkl'))
pkl_path5 = os.path.normpath(os.path.join(base, '../pkl/add_one.pkl'))
pkl_path6 = os.path.normpath(os.path.join(base, '../pkl/trues_list.pkl'))
#set_char = pd.read_pickle(pkl_path1)
seikai_tango =  pd.read_pickle(pkl_path2)
seikai_word =  pd.read_pickle(pkl_path3)
add_word = pd.read_pickle(pkl_path4)
add_one = pd.read_pickle(pkl_path5)
trues_list = pd.read_pickle(pkl_path6)
csv_path = os.path.normpath(os.path.join(base, '../pkl/pea.csv'))

#####################################################################
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

def found_bd(gs):
    #全角とタブを消す
    work_text = gs.replace("\u3000","").replace("\t","")#スペース消去
    work_text = jaconv.z2h(work_text, kana=False, digit=True, ascii=True)#半角変換
    ################################################################
    #改行を入れる
    spl = work_text.split("\n")

    lis = []
    fst = ["・","[","{","【","<","*","("]
    end = ["。", "]","}","】",">","*",")"]

    for i in spl:
        if i[-1:] in end and i[:1] in fst:
            i = ("\n" + i +"\n")
            lis.append(i)
        elif i[-1:] in end:
            i = i +"\n"
            lis.append(i)
        elif i[:1] in fst:
            i = ("\n" + i)
            lis.append(i)
        elif len(i) < 20:
            i = (i + "\n")
            lis.append(i)
        else:
            lis.append(i)

    lis = "".join(lis)
    work_text = lis.replace("\n\n", "\n")
    ###########################################################################
    #csv
    fix_dic = {}
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        for i in reader:
            fix_dic[i[0]] = i[1]
    for i,j in fix_dic.items():
        if i in work_text:
            work_text = work_text.replace(i,j)
    ############################################################################
    ss,words = wakati(work_text)
    #名詞のみを出す
    bd_word = [i for i in words if not i.isdecimal() and len(i) >= 2]#数字と一文字を抜く
    m_ls = [(ss[i-1] + x) for i,x in enumerate(ss) if ((i != 0) and ((len(x) + len(ss[i-1])) == len(x)+1))]
    ############################################################################
    #絞り込み
    bd_word = set(bd_word) - set(seikai_word)
    bd_word = set(bd_word) - set(add_word)
    bd_word = set(bd_word) - set(trues_list)
    m_ls = set(m_ls) - set(seikai_tango)
    m_ls = set(m_ls) - set(add_one)

    w_list = list(bd_word) + list(m_ls)
    w_list = list(set(w_list))

    pattern = r"%s" % "|".join(map(re.escape, w_list))
    work_text=re.sub(pattern, lambda m: (m.group()[0:-1] + "<span class='mstake'>" + m.group()[-1:] + "</span>") ,html.escape(work_text))
    ############################################################################
    #work_text = work_text.replace("\n", "<br>")


    return work_text


def open_file(file): #ファイル読み込み、移動
    with open(file,'rb') as f:
        bn = chardet.detect(f.read())
        if bn['encoding'] == 'utf-8':
            with open(file, 'r',encoding='utf-8') as r:
                orig_txt = r.read()
        else:
            with open(file, 'r') as r:
                orig_txt = r.read()

    # with open (file, 'r') as f: #作業テキスト読み込み
    #     orig_txt = f.read()

    return orig_txt

def main():
    cgitb.enable(display=0, logdir="")
    ############################################################################
    files =glob.glob(file_path) #ファイル読み込み
    if len(files) == 0:
        return None, None
    filename = os.path.splitext(os.path.basename(files[0]))#ファイルの名前(拡張子無し)
    w_path = os.path.normpath(os.path.join(base, '../work/working/' + filename[0] + ".txt"))
    ############################################################################
    #作業中のファイルがある場合そこから始める
    working_file =glob.glob(working_path)
    if len(working_file) != 0:#len()できく-ok
        tyud_txt = open_file(working_file[0])
        # with open (working_file[0], 'r') as f: #作業テキスト読み込み
        #     tyud_txt = f.read()
        work_name = os.path.splitext(os.path.basename(working_file[0]))
        os.remove(working_file[0])

        return work_name[0],tyud_txt
    ############################################################################
    ############################################################################
    orig_txt = open_file(files[0])
    html_txt = found_bd(orig_txt)

    return filename[0], html_txt

if __name__ == '__main__':
   main()

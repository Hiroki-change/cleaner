#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi, cgitb
import sys,io,os
import json
import index
import openpyxl
import csv
import shutil
import MeCab
import pandas as pd
import re
import logging

################################################################################
#jsからの戻り値受け取り
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8') # UTF-8に
cgitb.enable(display=0, logdir="")

form = cgi.FieldStorage()
ret_text = form.getfirst("text")
ret_title = form.getfirst("title")
word_pea = form.getfirst("pea")
trues_list = form.getlist("trues[]")
b_list = form.getlist("b[]")
t_list = form.getlist("t[]")
################################################################################

base = os.path.dirname(os.path.abspath(__file__))
fin_path = os.path.normpath(os.path.join(base, '../work/fin/'))
pkl_path = os.path.normpath(os.path.join(base, '../pkl/trues_list.pkl'))
f_path = os.path.normpath(os.path.join(base, '../work/fin/' + ret_title + '-m.txt'))
w_csv = os.path.normpath(os.path.join(base, '../pkl/pea.csv'))
text_pre_path = os.path.normpath(os.path.join(base, '../work/pre_work/' + ret_title + '.txt'))
pdf_pre_path =os.path.normpath(os.path.join(base, '../work/pre_work/' + ret_title + '.pdf'))
add_trues_list = pd.read_pickle(pkl_path)

##################################################################################
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

#############################################################################
#第一引数に移動させたいファイルやディレクトリのパス、第二引数に移動先のディレクトリのパスを指定する。
#textのmove
shutil.move(text_pre_path,fin_path)
#pdfのmove
shutil.move(pdf_pre_path,fin_path)
################################################################################
#修正前、後単語の辞書(csv)への登録
if (b_list and t_list) is not None:
    list_pea = []
    b_list = [i for i in b_list if i is not ""]
    t_list = [i for i in t_list if i is not ""]
    for (a,b) in zip(b_list,t_list):
        c = [a,b]
        list_pea.append(c)
    with open(w_csv, 'a')as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(list_pea)

# if(word_pea is not None):
#     list_pea = []
#     word_pea = word_pea.split("\n")
#     word_pea = [i for i in word_pea if i]
#     #jsからlistを返して保存
#     #jsonでそのまま保存
#     for i in word_pea:
#         c = i.split(" ")
#         list_pea.append(c)
#
#     with open(w_csv, 'a')as f:
#         writer = csv.writer(f, lineterminator='\n')
#         writer.writerows(list_pea)
################################################################################
add_trues_list = trues_list + add_trues_list
add_trues_list = list(set(add_trues_list))
pd.to_pickle(add_trues_list, pkl_path)
################################################################################
#ファイル書き出し
ret_text = ret_text.replace("<br>", "\n").replace('<span class="mstake">',"").replace("</span>", "").replace("&lt;","<").replace("&gt;",">")

with open(f_path, 'w') as f:
    f.write(ret_text)

################################################################################
#次のファイル読込
tit, txt = index.main()

if txt is None:
    response = {
        "txtx": "すべてのファイルが終了しました。",
        "title": "end"
    }
else:
    response = {
        "txtx": txt,
        "title": tit
    }

print('Content-type: text/html\nAccess-Control-Allow-Origin: *;charset=UTF-8\n')
print(json.JSONEncoder().encode(response))

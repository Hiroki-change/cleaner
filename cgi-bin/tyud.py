#!/usr/bin/env pythonpy
# -*- coding: utf-8 -*-

import cgi, cgitb
import sys,io
import json
import os
import csv
import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8') # UTF-8に

#エラーの内容をブラウザに送信
cgitb.enable(display=0, logdir="")
form = cgi.FieldStorage()
ret_text = form.getfirst("text")
ret_title = form.getfirst("title")
b_list = form.getlist("b[]")
t_list = form.getlist("t[]")
trues_list = form.getlist("trues[]")

base = os.path.dirname(os.path.abspath(__file__))
text_path = os.path.normpath(os.path.join(base, '../work/working/' + ret_title + '.txt'))
pkl_path = os.path.normpath(os.path.join(base, '../pkl/trues_list.pkl'))
w_csv = os.path.normpath(os.path.join(base, '../pkl/pea.csv'))
add_trues_list = pd.read_pickle(pkl_path)

############################################################
add_trues_list = trues_list + add_trues_list
add_trues_list = list(set(add_trues_list))
pd.to_pickle(add_trues_list, pkl_path)
############################################################
#csvで訂正箇所を保存する
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

# if (word_pea is not None):
#     list_pea = []
#     word_pea = word_pea.split("\n")
#     word_pea = [i for i in word_pea if i]
#
#     for i in word_pea:
#         c = i.split(" ")
#         list_pea.append(c)
#
#     with open(w_csv, 'a')as f:
#         writer = csv.writer(f, lineterminator='\n')
#         writer.writerows(list_pea)
############################################################
with open(text_path, 'w') as f:
    f.write(ret_text)
############################################################

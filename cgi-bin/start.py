#!/usr/bin/env pythonpy
# -*- coding: utf-8 -*-

import cgi, cgitb
import sys,io
import json
import index
import logging

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8') # UTF-8に

#エラーの内容をブラウザに送信
cgitb.enable()
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

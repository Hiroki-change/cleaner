# cleaner
OCRcleanerマニュアル<br>
# このソフトについて
OCR処理などで誤字脱字がテキストファイル中に存在し、それを修正するためのソフトウェアです。<br>
左側に変換元のPDFを表示し、右側に修正をするテキストを表示します。<br>
テキスト中の誤字と思われる箇所を赤字で強調します。<br>
誤りである可能性もありますが、赤字を中心に見て作業をすることにより作業スピードが向上すると考えます。<br>
# 操作方法
左右のPDFとテキストを見比べ、修正箇所を見つけた場合その箇所をマウスで範囲選択します。<br>
範囲選択後画面上部にテキストボックスが表示されるので、テキストを入力してください。<br>
範囲選択されたテキストがファイル中に複数存在する場合、同時に修正されます。<br>
作業終了後は画面最下部にある終了ボタンを押してください。自動的に次のファイルが表示されます。<br>

# 環境設定
動作環境
・windows10<br>
・JupiterNoteBookインストール<br>
　未インストールの場合以下からDL<br>
　https://jupyter.org/<br>
・形態素解析エンジン　MeCabを使用可能にすること<br>
　　以下を参考に導入<br>
　　https://qiita.com/menon/items/f041b7c46543f38f78f7<br>
・Chormeブラウザ<br>
<br>
 このソフトはローカルサーバを建てそこで動作するものです。<br>
 １．そのためまずはサーバを建てるためのBatファイルを編集します。<br>
 　 「pkl」フォルダ内の「server.bat」をメモ帳などで編集可能な状態にしてください。<br>
 　　1行目の「call C:\\ProgramData\\Anaconda3\\Scripts\\activate.bat」を<br>
 　　お使いのpcに導入されているAnaconda3フォルダ内のactivate.batまでのフルパスをコピーし貼り付けしてください。<br>
   
 ２．anaconda promptにおいて本ソフトで使うモジュールのインストールを行います<br>
 　  anaconda promptを起動し、<br>
　　「pip install -U pip」 pipのupdate<br>
　　「pip install chardet」chardet install<br>
　　「pip install pandas」 pandas install<br>
　　「pip install jaconv」jaconv install<br>
　　「pip install html」html install<br>
     <br>
  ３．work/pre_workフォルダに作業をしたいテキストとPDFのペアを入れる<br>
  　　この時、テキストとPDFは拡張子を除き同名としてください。<br>
  ４. 起動<br>
    １．で編集した「server.bat」をダブルクリックしてchorme起動後画面に表示されましたら成功です。<br>
 

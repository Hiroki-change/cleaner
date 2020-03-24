$(function(){

  //Class_Stack
  class Stack {
    constructor() {
      this._array = [];
    }
    push(val) {
      this._array.push(val);
    }
    pop() {
      //FILO
      return this._array.pop();
    }
    shift() {
      //FIFO
      this._array.shift();
    }
  }

  //Stackクラスの初期化
  const txt_stk = new Stack();
  const pea_stk = new Stack();
  const t_stk = new Stack();//辞書の正解を保存するもの
  const b_stk = new Stack();//辞書の間違いを保存するもの
  const del_stk = new Stack();
  const tru_stk = new Stack();
//ページが表示されたタイミングでテキストのロード

  function replaceText(preText, aftText) {
    let httxt = $("#txt").html();
    txt_stk.push(httxt);
    if(isNaN(preText)){
      b_stk.push(preText);
      t_stk.push(aftText);
      console.log(b_stk._array);
      console.log(t_stk._array);
    }else{
      b_stk.push("");
      t_stk.push("");
      console.log(b_stk._array);
      console.log(t_stk._array);
    }


    del_stk.push($("#delete").html());
    preText.replace(/<("[^"]*"|'[^']*'|[^'">])*>/g,'');
    var reRegExp = /[\\^$.*+?()[\]{}|]/g;
    httxt = httxt.replace(new RegExp(preText.replace(reRegExp, '\\$&'),'g'), aftText);
    $("#txt").html(httxt);

    let okikae = $("#pea").html();

    okikae = okikae + (preText + " " + aftText + "<br>\n");

    $("#pea").html(okikae);

  };

  function repOneWord(preText, aftText,sel){

    var range = sel.getRangeAt(0);
    var newNode = document.createElement('p');
    newNode.innerHTML = sel.toString();
    range.deleteContents();    // 範囲選択箇所を一旦削除
    range.insertNode(newNode); // 範囲選択箇所の先頭から、修飾したspanを挿入

    let httxt = $("#txt").html();
    //let sel = window.getSelection();

    pea_stk.push($("#pea").html());

    b_stk.push("");
    t_stk.push("");
    console.log(b_stk._array);
    console.log(t_stk._array);

    del_stk.push($("#delete").html());

    preText.replace(/<("[^"]*"|'[^']*'|[^'">])*>/g,'');
    var reRegExp = /[\\^$.*+?()[\]{}|]/g;
    httxt = httxt.replace(new RegExp(preText.replace(reRegExp, '\\$&'),'g'), aftText);
    $("#txt").html(httxt);
  };

  function delText(text) {
    let httxt = $("#txt").html();
    txt_stk.push(httxt);

    pea_stk.push($("#pea").html());

    b_stk.push("");
    t_stk.push("");

    console.log(b_stk._array);
    console.log(t_stk._array);

    del_stk.push($("#delete").html());

    tru_stk.push("");
    text.replace(/<("[^"]*"|'[^']*'|[^'">])*>/g,'');
    var reRegExp = /[\\^$.*+?()[\]{}|]/g;
    httxt = httxt.replace(new RegExp(text.replace(reRegExp, '\\$&'),'g'), "");
    $("#txt").html(httxt);
    let okikae = $("#delete").html();
    okikae = okikae + ( "<br>" + text );
    $("#delete").html(okikae);
  };

$(document).ready(function() {
    $.post({
      url: './cgi-bin/start.py',
    })
    .done(function(response) {
      obj = JSON.parse(response || "null");
      $('#txt').html(obj.txtx);
      $('#title').html(obj.title);
      $('#pdf_left').before('<object type="application/pdf" id="pdfLeft" data="/work/pre_work/' + obj.title + '.pdf"></object>');
    })
    .fail(function() {
      $('#txt').html('Failed.');
    });
});

//終了ボタンが押された
$('#end').on('click', function() {
  event.preventDefault();
  var $form = $(this);
  $('#pdfLeft').remove();
  console.log(tru_stk);
  $.ajax({
    url: './cgi-bin/end.py',
    type: 'post',
    dataType: 'text',
    data: {
      title: $('#title').html(),
      text: $('#txt').html(),
      "b[]": b_stk._array,
      "t[]": t_stk._array,
      "trues[]": tru_stk._array
    },
  })
  .done(function(response) {
    obj = JSON.parse(response);
    $('#txt').html(obj.txtx);
    $('#title').html(obj.title);

    $("#pea").html("");

    $("#delete").html("");
    $('#pdf_left').before('<object type="application/pdf" id="pdfLeft" data="/work/pre_work/' + obj.title + '.pdf"></object>');
    $('.split-box').scrollTop(0); //左のテキストを最上位まで移動
  })
  .fail(function() {
    $('#result').html('Failed.');
  });
});

$('#check').click(function() {
  $('#pea').focus();
});

//中断ボタンが押された
$('#tyud').on('click', function() {
  event.preventDefault();
  var $form = $(this);
  $.ajax({
    url: './cgi-bin/tyud.py',
    type: 'post',
    dataType: 'text',
    data: {
      title: $('#title').html(),
      text: $('#txt').html(),
      "b[]": b_stk._array,
      "t[]": t_stk._array,
      "trues[]": tru_stk._array
    },
  })
  .done(function() {
    $('#txt').html('Save');
    $('#pdf_left').html("");
    $('#button').html("");
    $("#pea").html("");
    $("#delete").html("");
  })
  .fail(function() {
    $('#result').html('Failed.');
  });
});

$('#check').click(function() {
  $('#pea').focus();
});

//ctl+zで一回分操作を戻す
Mousetrap.bind('ctrl+z', function () {
    $("#txt").html(txt_stk.pop());

    $("#pea").html(pea_stk.pop());
    let b_poped = b_stk.pop();
    let t_poped = t_stk.pop();
    console.log(b_stk._array);
    console.log(t_stk._array);

    $("#delete").html(del_stk.pop());
    let poped = tru_stk.pop();
});

//dragで選択した
$("#txt").mouseup(function(){
  let selctText = ($.selection('Text'));
  if(selctText.length == 0){
    let sel_win = window.getSelection();
    sel_win.removeAllRanges();
    return;
  }
  let selct = ($.selection('html'));
  console.log(selct);
  console.log(selctText);
  let sel_win = window.getSelection();
  let sel = window.getSelection();
  let x = $("<div></div>").dialog({autoOpen:false, modal:true,resizable: false,draggable: false});
  x.html("");
  x.dialog("option", {
    title: "選択してください",
    width:400,
    height:100,
    modal: true,
    buttons: {
        "訂正入力": function() {
          let result = window.prompt("置換前文字 : " + selctText);
          if(result != null && result != ""){
            if(selct.length == 1 || selct == "&gt;" || selct == "&lt;"){
              txt_stk.push($("#txt").html());
              tru_stk.push("");
              repOneWord('<p>' + selct + '</p>',result,sel);
            }else{
              tru_stk.push("");
              replaceText(selct,result);
            }
          }
          sel_win.removeAllRanges();
          $(this).dialog("destroy");
        },
        "削除": function() {
          if(selct.length == 1 || selct == "&gt;" || selct == "&lt;"){
            txt_stk.push($("#txt").html());
            tru_stk.push("");
            repOneWord('<p>' + selct + '</p>',"",sel);
          }else{
            delText(selct);
          }
          sel_win.removeAllRanges();
          $(this).dialog("destroy");
         },
        "正解": function() {

          let httxt = $("#txt").html();
          pea_stk.push($("#pea").html());

          b_stk.push("");
          t_stk.push("");
          console.log(b_stk._array);
          console.log(t_stk._array);

          del_stk.push($("#delete").html());

          selct.replace(/<("[^"]*"|'[^']*'|[^'">])*>/g,'');
          var reRegExp = /[\\^$.*+?()[\]{}|]/g;
          httxt = httxt.replace(new RegExp(selct.replace(reRegExp, '\\$&'),'g'), selctText);
          $("#txt").html(httxt);

          tru_stk.push(selctText);
          sel_win.removeAllRanges();
          $(this).dialog("destroy");
         },
        "キャンセル": function() {
          sel_win.removeAllRanges();
          $(this).dialog("destroy");
         },
        "訂正 With def": function() {
          let result = window.prompt("置換前文字 : " + selctText,selctText);
          if(result != null && result != ""){
            if(selct.length == 1 || selct == "&gt;" || selct == "&lt;"){
              txt_stk.push($("#txt").html());
              tru_stk.push("");
              repOneWord('<p>' + selct + '</p>',result,sel);
            }else{
              tru_stk.push("");
              replaceText(selct,result);
            }
          }
          sel_win.removeAllRanges();
          $(this).dialog("destroy");
         }
    }
  });
  x.dialog("open");
});
});

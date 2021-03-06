# Summalize_Qiita_Trends
# 概要
Qiitaのトレンドを取得して記事の要約を行う。

Qiitaの1日のトレンドをPythonのライブラリBeautifulSoupでスクレイピングしてきて、タイトルとURL、タグと本文の要約を[summalize_text.md](summalize_text.md)に吐き出します。

## 動かし方
依存ライブラリダウンロード
```
pip install -r requirements.txt
```
実行
```
python main.py
```

## Mecab(形態素解析)
要約するために、まずMecabというライブラリを用いて形態素解析を行います。Mecabの導入は、下記コマンドで行い、
```
pip install mecab-python3
```
追加辞書(mecab-ipadic-neologd)の導入を[MecabをPythonで使うまで](https://qiita.com/Sak1361/items/47e9ec464ccc770cd65c)を参考に行いました。

追加辞書のインストール先を忘れた場合は以下のコマンドで出てきます。
```
echo `mecab-config --dicdir`"/mecab-ipadic-neologd"
```

## 要約
要約は[sumy](https://github.com/miso-belica/sumy)というライブラリのLexRankを用いて行いました。

- Automatic text summarizer [miso-belica/sumy](https://github.com/miso-belica/sumy)

### LexRank
LexRankとは、PageRankに着想を得た要約アルゴリズムです。

PageRankはWebページの重要度を決定するためのアルゴリズムで、リンク構造をWebページをノード、リンクをエッジとして捉えて下記の項目で重要度を決めていました。
1. 多くのページからリンクされているページは重要なページ
2. 重要なページからリンクされているページは重要なページ

LexRankでは、文章をノード、文章の類似度(0/1)をエッジとし、下記の項目で重要度を決めています。
1. 多くの文と類似する文は重要な文
2. 重要な文と類似する文は重要な文

文章の類似度はTF-IDFからcos類似度を計算することで得ます。
つながっているエッジが太く、かつ数の多いノード(文章)が重要な文章として要約文の候補となります。

---

# おまけ(感想)
## 感想
今回文章の要約というものをやってみたかったので、普段よく見るQiitaのトレンド記事を要約できれば便利かなと思いコードを書いてみましたが、後述する理由から、Qiitaの記事は文章の要約にはあまり向いておらず、上手い要約文が作れなかったように思います。また、基本、Qiita記事は技術的な文書の構造に乗っ取っている(ことが望ましい)ため、大体はじめに概要が書いてあります。そのため、文章の要約せずとも最初の数文を読めば十分という結果が正直多かったです。
つまり、企画選びからしてちょっと失敗だったかなという印象です。

今回前々からやりたいと思っていた文章の要約を実際に試してみて、要約に向くものとそうでないものがあることがわかりました。もし次やるならWikipediaのデータセットを使うなど、もう少し要約しやすそうなものを選びます。また、LexRankという手法も2004年に提案された手法と、古めなのでBERTを用いてみたりと、もう少し良い要約手法を考えてみたいと思います。

## Qiitaの記事が要約に向かない理由
- コードが多く文章中に含まれる点
- 文章に句読点をつけない輩がいる点
- 箇条書きでかかれたりするため、やはり文末に句点がつかないことが多々ある点
- 絵文字を大量に使う輩が時たまいる点
- 同様に顔文字が存在する点
- 数式が入る点

などなどが難点として挙げられました。特に、いいエンジニアはコードで語ると言わんばかりに、ほぼコードしか書いてないものは要約する文章がなく困りました。数式メインのも同様です。

## 要約文の数
要約文の数を2~5まで試してみましたが、数が多くても情報が増えていい要約になるとは限らず、意味が通らない文章になることが多かったので今回は文章数は2にしました。興味がある人はコードをみていじってみてください。

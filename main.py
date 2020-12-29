import json
import MeCab
import requests
from bs4 import BeautifulSoup

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer


res = requests.get("https://qiita.com/")

# htmlをBeautifulSoupで扱う
soup = BeautifulSoup(res.text, "html.parser")

# トレンドのタイトルとURLを取得
urls, titles = [], []
for item in soup.select('.css-qrra2n'):
    urls.append(item.attrs['href'])
    titles.append(item.text)

print(urls)
print(titles)
print(len(urls), len(titles))
print('')

for url, title in zip(urls, titles):
    print(title)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    tag = [a.text for a in soup.select_one('.it-Tags').select('a')] # 記事のタグ
    print(tag)
    sentences = soup.select_one('.it-MdContent').text # 記事の本文
    sentences = [s for s in sentences.split('\n')]

    wakati = MeCab.Tagger('-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd') #追加辞書を適用 # echo `mecab-config --dicdir`"/mecab-ipadic-neologd" で辞書のインストール先を特定
    corpus = [wakati.parse(sentence).strip() for sentence in sentences if len(sentence)!=0]
    corpus = ' '.join(corpus) # センテンスのリストだったものを全てくっつけて一つの文にする
    
    parser = PlaintextParser.from_string(''.join(corpus),Tokenizer("japanese"))

    # 要約
    #Lex-Rank
    summarizer = LexRankSummarizer()
    # #Text-Rank
    # summarizer = TextRankSummarizer()
    # #LSA
    # summarizer = LsaSummarizer()
    summarizer.stop_words = [' ']  # スペースも1単語として認識されるため、ストップワードにすることで除外する
    summary = summarizer(document=parser.document, sentences_count=2)

    summary = [str(s) for s in summary]
    summary = ''.join(summary).replace(' ', '') # 要約した各文のリストをくっつけて、スペースを削除する
    print(summary)

    print('')

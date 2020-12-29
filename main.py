import json
import MeCab
import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer


res = requests.get('https://qiita.com/')

# htmlをBeautifulSoupで扱う
soup = BeautifulSoup(res.text, 'html.parser')

# トレンドのタイトルとURLを取得
urls, titles = [], []
for item in soup.select('.css-qrra2n'):
    urls.append(item.attrs['href'])
    titles.append(item.text)

output_text = f'# {dt.now().year}-{dt.now().month}-{dt.now().day} {dt.now().hour}時の[Qiita１日のトレンド](https://qiita.com/)\n'
for url, title in zip(urls, titles):
    output_text += f'# [{title}]({url})\n'

    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    # 記事のタグの取得
    tag = [a.text for a in soup.select_one('.it-Tags').select('a')] # 記事のタグ
    output_text += f'## Tags\n{tag}\n'

    # 記事本文の内容取得
    sentences = soup.select_one('.it-MdContent').text # 記事の本文
    sentences = [s for s in sentences.split('\n')]
    # 文末に'。'つけない人がいるのでそのための処理
    for i in range(len(sentences)):
        if len(sentences[i])!=0:
            if sentences[i][-1]!='。' and sentences[i][-1]!='、' and sentences[i][-1]!='.' and sentences[i][-1]!=',':
                sentences[i]+='。'

    wakati = MeCab.Tagger('-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd') #追加辞書を適用 # echo `mecab-config --dicdir`"/mecab-ipadic-neologd" で辞書のインストール先を特定
    corpus = [wakati.parse(sentence).strip() for sentence in sentences if len(sentence)!=0]
    corpus = ' '.join(corpus) # センテンスのリストだったものを全てくっつけて一つの文にする
    
    parser = PlaintextParser.from_string(''.join(corpus),Tokenizer("japanese"))

    # 要約
    summarizer = LexRankSummarizer() # Lex-Rank
    # summarizer = TextRankSummarizer() # Text-Rank
    # summarizer = LsaSummarizer() # LSA
    summarizer.stop_words = [' ']  # スペースも1単語として認識されるため、ストップワードにすることで除外する
    summary = summarizer(document=parser.document, sentences_count=2)

    summary = [str(s) for s in summary]
    summary = ''.join(summary).replace(' ', '') # 要約した各文のリストをくっつけて、スペースを削除する
    output_text += '## Summary\n'
    output_text += summary+'\n'

with open('./summalize_text.md', mode='w') as f:
    f.write(output_text)

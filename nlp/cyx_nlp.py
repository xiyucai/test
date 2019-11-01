# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 10:30:41 2019

@author: Yuxi Cai
"""

import nltk

# 下载示例推文
#nltk.download('twitter_samples')
# 下载punkt
'''
预先训练好的模型,帮助您标记解析单词和句子。例如，这个模型知道一个名称可能包含一个句点(比如“S. Daityari”)，
并且这个句点出现在一个句子里并不一定就表示到此结束了
'''
#nltk.download('punkt')
# 英语词汇数据库
#nltk.download('wordnet')
# 确定一个句子中单词的上下文
#nltk.download('averaged_perceptron_tagger')

# 标记解析器:对数据进行词性标记
# 导入数据
from nltk.corpus import twitter_samples

# 正面情感推文 5000
positive_tweets = twitter_samples.strings('positive_tweets.json')
# 负面情感推文 5000
negative_tweets = twitter_samples.strings('negative_tweets.json')
# 没有情感推文 20000
text = twitter_samples.strings('tweets.20150430-223406.json')
# 标记解析
tweet_tokens = twitter_samples.tokenized('positive_tweets.json')

# 规范化数据
from nltk.tag import pos_tag

print(pos_tag(tweet_tokens[0]))


##############################################################################
import nltk

nltk.down('book')
from nltk.book import *

# 搜索文本搜索文本
# 会显示20个包含former的语句上下文
text1.concordance('former')

# 搜索相关词
# 输入了ship，查找了boat，都是近义词
text1.similar('ship')

# 查看某个词在文章里出现的位置
text4.dispersion_plot(["citizens", "democracy", "freedom", "duties", "America"])

# 词频统计
'''
len(text1)：返回总字数
set(text1)：返回文本的所有词集合
len(set(text4))：返回文本总词数
text4.count("is")：返回“is”这个词出现的总次数
FreqDist(text1)：统计文章的词频并按从大到小排序存到一个列表里
fdist1.hapaxes()：返回只出现一次的词
text4.collocations()：频繁的双联词
'''
# ：统计词频，并输出累计图像
# 纵轴表示累加了横轴里的词之后总词数是多少
fdist1 = FreqDist(text1)
fdist1.plot(50, cumulative=True)

#------------语料与词汇资源------------------------------#

# Gutenberg语料库
nltk.corpus.gutenberg.fileids()
'''
nltk.corpus.gutenberg就是gutenberg语料库的阅读器，它有很多实用的方法，比如：
nltk.corpus.gutenberg.raw('chesterton-brown.txt')：输出chesterton-brown.txt文章的原始内容
nltk.corpus.gutenberg.words('chesterton-brown.txt')：输出chesterton-brown.txt文章的单词列表
nltk.corpus.gutenberg.sents('chesterton-brown.txt')：输出chesterton-brown.txt文章的句子列表

类似的语料库还有：

from nltk.corpus import webtext：网络文本语料库，网络和聊天文本
from nltk.corpus import brown：布朗语料库，按照文本分类好的500个不同来源的文本
from nltk.corpus import reuters：路透社语料库，1万多个新闻文档
from nltk.corpus import inaugural：就职演说语料库，55个总统的演说
'''


# 语料库的通用接口
'''
fileids()：返回语料库中的文件
categories()：返回语料库中的分类
raw()：返回语料库的原始内容
words()：返回语料库中的词汇
sents()：返回语料库句子
abspath()：指定文件在磁盘上的位置
open()：打开语料库的文件流
'''

# 加载自己的语料库
# 也可以使用如wordlists.sents('a.txt')和wordlists.words('a.txt')等方法来获取句子和词信息
from nltk.corpus import PlaintextCorpusReader
corpus_root = '/tmp'
wordlists = PlaintextCorpusReader(corpus_root, '.*')
wordlists.fileids()

# 条件频率分布
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

from nltk.corpus import brown

# 链表推导式，genre是brown语料库里的所有类别列表，word是这个类别中的词汇列表
# (genre, word)就是类别加词汇对
genre_word = [(genre, word)
        for genre in brown.categories()
        for word in brown.words(categories=genre)
        ]

# 创建条件频率分布
cfd = nltk.ConditionalFreqDist(genre_word)

# 指定条件和样本作图
cfd.plot(conditions=['news','adventure'], 
         samples=[u'stock', u'sunbonnet', u'Elevated', u'narcotic', u'four', u'woods', u'railing', u'Until', u'aggression', u'marching', u'looking', u'eligible', u'electricity', u'$25-a-plate', u'consulate', u'Casey', u'all-county', u'Belgians', u'Western', u'1959-60', u'Duhagon', u'sinking', u'1,119', u'co-operation', u'Famed', u'regional', u'Charitable', u'appropriation', u'yellow', u'uncertain', u'Heights', u'bringing', u'prize', u'Loen', u'Publique', u'wooden', u'Loeb', u'963', u'specialties', u'Sands', u'succession', u'Paul', u'Phyfe'])



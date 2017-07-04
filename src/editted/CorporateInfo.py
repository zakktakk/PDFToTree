# -*- coding: utf-8 -*-

import json

from segment import SegmentAnalysis
from future import FutureAnalysis
from reason import ReasonAnalysis

#jsonファイルを作る
#セグメント情報、将来の文章、理由の文章を抽出し、jsonファイルに挿入
class CorporateAnalysis(object):
    def __init__(self,raw_text):
        self.raw_text=raw_text
        self.sentences=make_sentences(raw_text)
        self.keywords=keywords_open()
        self.single_segment_word=single_segment_open()
        self.SA = SegmentAnalysis()
        self.FA = FutureAnalysis()
        self.RA = ReasonAnalysis()
        self.data={}

    def write_json(self,savepath):
        data=self.make_json()

        with open(savepath, 'w') as outfile:
            json.dump(data, outfile,ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

    def make_json(self):

        #########セグメント、将来、理由の抽出部分###########
        self.segment()
        self.future()
        self.reason()
        ###############################################

        print(self.data)
        return self.data


    def segment(self):
        if self.singlecheck():    #単一のセグメントの場合
            self.data["segment"]="単一の事業"
        else:                        #セグメント情報がある場合
            return self.segment_detail()

    def singlecheck(self):
        #単一のセグメントであるかチェック(single_segment.txtによる条件分岐)
        flag=False
        for sentence in self.sentences:
            if flag:
                break

            else:
                for ll in self.single_segment_word:
                    miniflag=False
                    for l in ll:
                        word  = list(l.keys())[0]
                        point = list(l.values())[0]
                        if point>0:
                            if word in sentence:
                                miniflag=True
                            else:
                                miniflag=False
                                break
                        elif point<0:
                            if word not in sentence:
                                miniflag=True
                            else:
                                miniflag=False
                                break
                    if miniflag:
                        flag=True
        return flag

    def segment_detail(self):
        #segment.py内から呼び出し
        self.data["segment"] = self.SA.segment_name(self.sentences)


    def future(self):
        #将来の予測に関する文章をfuture.py内から呼び出し
        self.data["圧縮前_将来の文章"] = self.FA.extract_future_sentences(self.sentences)

        #対象の文章が多いものに関しては6文までスコアが高い順番に抽出
        import summarize
        self.data["future_sentences"] = summarize.compression(self.data["圧縮前_将来の文章"],6)

    def reason(self):
        #理由部分の抽出をreason.pyから呼び出し
        self.data["reason"] = self.RA.reason_sentences(self.sentences)



def single_segment_open():
    f = open('./txt/single_segment.txt', 'r')
    single_segment_word=[]
    for line in f:
        tmp=[]
        for l in line.split(","):
            d={}
            word  = l.split(":")[0]
            point = float(l.split(":")[1].replace("\n",""))
            d[word]=point
            tmp.append(d)
        single_segment_word.append(tmp)
    f.close()
    return single_segment_word

def keywords_open():
    f = open('./txt/keywords.txt', 'r')
    keywords={}
    for line in f:
        word  = line.split(",")[0]
        point = float(line.split(",")[1].replace("\n",""))
        keywords[word]=point
    f.close()
    return keywords


def make_sentences(texts):
    ans=[]
    texts=texts.replace("｡","｡PERIODDAYO")
    for text in texts.split("\n"):
        for sentence in text.split('PERIODDAYO'):
            if len(sentence)>1:
                ans.append(sentence)
    return ans

# -*- coding: utf-8 -*-

import zenhan

#将来の予測に関する文章を抽出
class FutureAnalysis(object):
    def __init__(self):
        self.future_sentences=[]  #最終的にreturnするもの
        self.ok_keywords,self.ng_keywords=_future_keyword()  #okは含まれてほしい単語、ngは含まれて欲しくない単語

    def extract_future_sentences(self,sentences):
        #CorporateInfo.pyから呼び出される

        self.sentences = sentences
        self.find_future_sentences()

        return self.future_sentences

    def find_future_sentences(self):
        keywords,ngwords,headers,ngheaders = _future_find_section()
        #将来の予測に関する手がかり語のリスト

        flag=False
        for sentence in self.sentences:
            sentence=sentence.replace(" ","")
            #文章について
            if "｡" in sentence:
                if flag:  #将来の予測に関するパラグラフ内
                    self.future_sentences.append(sentence)

                else:    #将来の予測に関するパラグラフ内でない
                    for kw in keywords:
                        for nw in ngwords:
                            if kw in sentence and nw not in sentence:
                                self.future_sentences.append(sentence)

            #見出しについて
            else:
                for h in headers:
                    if h in sentence:
                        flag=True
                for nh in ngheaders:
                    if nh in sentence:
                        flag=False

    def find_future_sentence_using_keyword(self,sentence):
        oks=self.ok_keywords
        ngs=self.ng_keywords
        for ok in oks:
            if ok in sentence:
                for ng in ngs:
                    if ng not in sentence:
                        self.future_sentences.append(sentence)




def _future_find_section():
    f = open('./txt/find_future.txt', 'r')
    keywords=[]  #セグメントの開始が見出しで始まる
    ngwords=[]    #セグメントの終わりが見出しで終わる
    headers=[]
    ngheaders=[]

    for line in f:
        line=line.replace("\n","")
        if line.split(",")[1] == "OK":
            keywords.append(zh(line.split(",")[0]))
        elif line.split(",")[1] == "NG":
            ngwords.append(zh(line.split(",")[0]))
        elif line.split(",")[1] == "header":
            headers.append(zh(line.split(",")[0]))
        elif line.split(",")[1] == "ngheader":
            ngheaders.append(zh(line.split(",")[0]))

    f.close()
    return keywords,ngwords,headers,ngheaders


def _future_keyword():
    f = open('./txt/find_future_keyword.txt', 'r')
    ok_keywords=[]
    ng_keywords=[]

    for line in f:
        line=line.replace("\n","").replace("、","､")
        word=zh(line.split(",")[0])
        if line.split(",")[1] == "OK":
            ok_keywords.append(word)
        elif line.split(",")[1] == "NG":
            ng_keywords.append(word)
    f.close()
    return ok_keywords,ng_keywords

def zh(text):
    text = str(zenhan.z2h(text))
    text=text.replace("〜","~").replace("ー","-")
    return text

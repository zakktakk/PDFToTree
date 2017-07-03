import zenhan
import CaboCha


class ReasonAnalysis(object):
  def __init__(self):
    self.reason_dict={}

  def reason_sentences(self,sentences):
    self.sentences = sentences
    self.find_reason_sentences()
    return self.reason_dict

  def find_reason_sentences(self):
    items = find_reason_items()
    keywords=find_reason_keyword()
    
    first_paragraph=first_paragraph_words()
    second_paragraph=second_paragraph_words()

    flag=False
    
    tmp_label=""
    prev_label=""

    for sentence in self.sentences:
        sentence=sentence.replace(" ","")
        flag2=True
        tmp_label=""  #tmplabelの初期化 

        for s in second_paragraph:
            if s in sentence:
                flag=False
        if flag:
            #営業利益などの単語が含まれていたら、ラベルをふる
                       
            for item in items:      
                if item in sentence:
                    # print("###")
                    # print(sentence)
                    tmp_label=item   #tmplabelに営業利益などをふる

                    #さらに理由を示す単語が入っていた場合は理由部分を抜き出し
                    
                    for kw in keywords:
                        if kw in sentence:
                            reason_=reason_part(sentence)

                            # print("!!!!!!!!!!!")
                            # print(item)
                            # print(kw)
                            # print(sentence)
                            # print(reason_part(sentence))
                                                   
                            flag3=True      
                            for item2 in items:
                                if item != item2:
                                    if item2 in reason_:
                                        flag3=False 
                            if flag3:
                                try:
                                    if reason_ not in self.reason_dict[tmp_label] and len(reason_)>0:
                                        self.reason_dict[tmp_label].append(reason_)
                                except KeyError:
                                    if len(reason_)>0:
                                        self.reason_dict[tmp_label]=[reason_]

                            flag2=False
            if flag2:    
                for kw in keywords:
                    if kw in sentence:
                        # print("-----------")
                        # print(kw)
                        # print(sentence)
                        if ("､" in sentence or "｡" in sentence) and len(prev_label)>0:
                            try:
                                self.reason_dict[prev_label].append(sentence)
                            except KeyError:
                                self.reason_dict[prev_label]=[sentence]
                            except UnboundLocalError:
                                pass

        for f in first_paragraph:
            if f in sentence:
               
                flag=True
        
        prev_label=tmp_label #tmp_labelを一つ昔のprev_labelにする


def first_paragraph_words():
  f = open('./txt/first_paragraph.txt', 'r')
  items=[]
  for line in f:
    line=line.replace("\n","")
    items.append(line)
  f.close()
  return items

def second_paragraph_words():
  f = open('./txt/second_paragraph.txt', 'r')
  items=[]
  for line in f:
    line=line.replace("\n","")
    items.append(line)
  f.close()
  return items


def find_reason_items():
  f = open('./txt/find_items.txt', 'r')
  items=[]
  for line in f:
    line=line.replace("\n","")
    items.append(line)
  f.close()
  return items


def find_reason_keyword():
  f = open('./txt/find_reason.txt', 'r')
  keywords=[]
  for line in f:
    line=line.replace("\n","").replace("、","､")
    keywords.append(line)
  f.close()
  return keywords

def zh(text):
  text = str(zenhan.z2h(text))
  text=text.replace("〜","~").replace("ー","-")
  return text


def reason_part(sentence):
    #係り受け解析して、理由を示す単語を含む文節以上の文を抽出

    sentence=sentence.replace("､","、")

    c = CaboCha.Parser()
    tree =  c.parse(sentence)
    #print(tree.toString(CaboCha.FORMAT_TREE))
    keywords=find_reason_keyword()
    
    d={}
    kakariuke_list=[]

    for line in tree.toString(CaboCha.FORMAT_LATTICE).split("\n"):
        tmp_dict={}
        if line.split(" ")[0] == "*":
            tag   = int(line.split(" ")[1])
            desti = int(line.split(" ")[2].replace("D",""))
            
            flag=True
            for l in kakariuke_list:
                if tag in l:
                    l.append(desti)
                    flag=False
            if flag:
                kakariuke_list.append([tag,desti])

        else:
            try:
                d[tag]+=line.split("\t")[0]
            except:
                d[tag]=line.split("\t")[0]
    
    
    indexes=_findstart(keywords,d,sentence)
    #print(indexes)
    nans=[]
    for index in indexes:
        #print(index)
        for nl in kakariuke_list:
            if index in nl:
                #print(nl)
                for l in nl:
                    if 0<l<=index :
                        nans.append(l)



    ans=""
    for key in list(set(nans)):
        ans+=d[key]
    ans=ans.replace("、","､")
    
    return ans

def _findstart(keywords,d,sentence):
    indexes=[]
    #print(sentence)
    #print(len(sentence))
    for kw in keywords:
        kw=kw.replace("､","、")
        if kw in sentence:
            length=len(sentence[:sentence.index(kw)+len(kw)])
            #print(sentence[:sentence.index(kw)+len(kw)])
            #print(length)
            x=0
            for k,v in d.items():
                if x>=length:
                    break
                else:
                    x+=len(v)
            index=k-1
            indexes.append(index)
    return indexes

if __name__ == '__main__':
    sentence = "営業経費は、株式会社ＳＭＢＣ信託銀行等において、トップライン収益強化に向け経費投入を行ったことを主因に、前年同期比 595 億円増加の１兆 3,452 億円となりました。"
    sentence="ｾｸﾞﾒﾝﾄ別営業利益につきましては､お客さまのﾆｰｽﾞやﾗｲﾌｽﾀｲﾙの変化に対応して過年度より事業ﾎﾟｰﾄﾌｫﾘｵの多様化を推進してきたことが奏功し､8事業中6事業(SM･DS(ｽｰﾊﾟｰﾏｰｹｯﾄ･ﾃﾞｨｽｶｳﾝﾄｽﾄｱ)事業､総合金融事業､ﾄﾞﾗｯｸﾞ･ﾌｧｰﾏｼｰ事業､ｻｰﾋﾞｽ･専門店事業､小型店事業､ﾃﾞｨﾍﾞﾛｯﾊﾟｰ事業)が増益となり､連結業績に寄与しました｡"
    
    ans=reason_part(sentence)    
    print(ans)






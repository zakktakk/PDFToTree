import zenhan
import re
import CaboCha

class SegmentAnalysis(object):
  def __init__(self):
    self.segment_dict={}

  def segment_name(self,sentences):
    self.sentences = sentences
    self.paragraph = paragraph(sentences)
    self.find_seg_section()
    return self.segment_dict

  def find_seg_value(self,sentences):
    ##売上高とかの値の収集

    items=find_reason_items()

    #####文の整形#######
    sentences=sentences.replace(" ","")
    sentences=sentences.replace("なったことから､","なったことから")
    sentences=sentences.replace("円減少し､","円減少し")


    for item in items:
      sentences=sentences.replace(item+"は､", item+"は")
      sentences=sentences.replace("%)"+item, "%)､"+item)  

    ####################
    
    ans={}
    t=""
    # print("########sentence################")    
    # print(sentences)
    for sentence in sentences.split("｡"):
      sentence=sentence.replace(" ","")
      phrases=sentence.split("､")

      for i, phrase in enumerate(phrases):
        pre_p  = pre_phrase(phrases,i)
        post_p = post_phrase(phrases,i)

        for item in items:
          flag=False

          if item in phrase:
            print(phrase)
            ###################数字の取得#####################
            try:
              value = extract_value(phrase,item)
              ans[item] = value

              float_value=float(kanji_to_num(value))
              ans["calc"+item] = debt_check(phrase,float_value)   #赤字や営業損失な場合はマイナスの符号をつける
              
              flag=True        
            except AttributeError:
              pass
            ################################################
            if flag:   #valueの抽出がうまく言った場合に行われる
              try:
                # print(phrase)
                # print(item)
                # print("!!!!!!!!!!!!")
                prev = extract_pre_value(phrase,item)

                if prev != "prev" and len(prev)>0:
                  ans[item+"の変化量"] = prev
                  float_prev = calc_pre_value(debt_check(phrase,float_value),prev)
                  ans["calc_prev"+item] = float_prev

                else:
                  
                  prev = around_extract_pre_value(pre_p,phrase,post_p)
                  # print("JKKKKKKKKKK")
                  # print(prev)
                  if prev != "prev" and len(prev)>0:
                    ans[item+"の変化量"] = prev
                    float_prev = calc_pre_value(debt_check(phrase,float_value),prev)
                    ans["calc_prev"+item] = float_prev

              except AttributeError:
              

                pass
            ################################################
    
    return ans

  def find_seg_section(self):
    
    ###########開始と終わりの手がかり語がある場合#####################
    seg_counter=0
    start_header, end_header, start_keyword, end_keyword,start_suddenly = _seg_find_keyword()
    #print([start_header, end_header, start_keyword, end_keyword,start_suddenly])
    flag=False
    for index,sentence in enumerate(self.sentences):
      ##キーワードが含まれているか flag→False
      for w in end_header:
        if w in sentence:
          flag=False

      if flag:
        if "｡" not in sentence and "､" not in sentence and len(sentence)>1:
          segment_name=sentence
          _dict =self.find_seg_value(self.paragraph[index])
          if len(_dict)>0:
            self.segment_dict[segment_name]=_dict
          seg_counter+=1

      ##キーワードが含まれているか flag→True
      for w in start_header:
        if w in sentence:
          flag=True
      for w in start_keyword:
        if w in sentence:
          flag=True
    #######################################################
    
    ###########開始の手がかり語がない場合#####################
    if seg_counter == 0:
      flag=False
      flag2=True
      for index,sentence in enumerate(self.sentences):  

        if flag2:  #一度endwordが来たらbreak
          ##キーワードが含まれているか flag→True
          if "｡" not in sentence and "､" not in sentence:
            for sudden in start_suddenly:
              if sudden in sentence:
                print(sudden)
                print("SUDDENNNNN")
                flag=True

            
        
          if flag:  
            ##キーワードが含まれているか flag→False
            for w in end_header:
              if w in sentence:
                flag2=False
          
            if flag2 and "｡" not in sentence and "､" not in sentence:
              segment_name=sentence
              print("!!!!!!!!!!!!!!!!!")
              print(segment_name)
              print("!!!!!!!!!!!!!!!!!")
              _dict=self.find_seg_value(self.paragraph[index])
              if len(_dict)>0:
                self.segment_dict[segment_name]=_dict
          
           
          
            
    #######################################################

    


def _seg_find_keyword():
  f = open('./txt/find_seg.txt', 'r')
  start_header=[]  #セグメントの開始が見出しで始まる
  end_header=[]    #セグメントの終わりが見出しで終わる
  start_keyword=[] #セグメントの開始がキーワードベース
  end_keyword=[]   #セグメントの終わりがキーワードベース
  start_suddenly=[] #突然セグメントの説明が始まる

  for line in f:
    line=line.replace("\n","")
    word = zh(line.split(",")[0])
    hk=line.split(",")[1]
    se=line.split(",")[2]
    if hk == "header":
      if se == "start":
        start_header.append(word)
      elif se == "end":
        end_header.append(word)
    elif hk== "keyword":
      if se == "start":
        start_keyword.append(word)
      elif se == "end":
        end_keyword.append(word)
      elif se == "suddenly":
        start_suddenly.append(word)

  f.close()
  return start_header, end_header, start_keyword, end_keyword,start_suddenly

def paragraph(sentences):
  ans={}
  key_index=0
  for index,sentence in enumerate(sentences):
    if "｡" not in sentence and "､" not in sentence and len(sentence)>1:
        key_index=index
        ans[key_index]=""
    else:
      ans[key_index]+=sentence
      
  return ans
def zh(text):
  text = str(zenhan.z2h(text))
  text=text.replace("〜","~").replace("ー","-")
  return text
 
def extract_value(sentence,item):
  sentence=sentence.replace("､","、")
  sentence=sentence.replace("円で前期比","円で、前期比")


  if len(re.findall("[\d,０１２３４５６７８９百千万億兆]+円",sentence)) > 1:
    if re.search("[\d,０１２３４５６７８９百千万億兆]+円の損失となりました",sentence):
      new_sentence=re.search("[\d,０１２３４５６７８９百千万億兆]+円の損失となりました",sentence).group()
    
    else:
      c = CaboCha.Parser()
      tree =  c.parse(sentence)
      #print(tree.toString(CaboCha.FORMAT_TREE))

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
      # print(d)
      # print(kakariuke_list)

      new_sentence=make_newsentence(d,kakariuke_list,item)
      #print(new_sentence)
  else:
    new_sentence=sentence

  if re.search("[\d,０１２３４５６７８９百千万億兆]+円の損失となりました",new_sentence):
    value=re.search("[\d,０１２３４５６７８９百千万億兆]+円の損失",new_sentence).group()
  else:
    value=re.search("[\d,０１２３４５６７８９百千万億兆]+円",new_sentence).group()
  

  # new_sentence=make_newsentence(d,kakariuke_list,"前期比")
  # if "増" in new_sentence:
  #   value=re.search("[\d,０１２３４５６７８９百千万億]+円",new_sentence).group()
  # elif "減" in new_sentence:
  #   value=re.search("[\d,０１２３４５６７８９百千万億]+円",new_sentence).group()
  #   value

  return value
def make_newsentence(d,kakariuke_list,item):
  ###itemが入っている文節とつながっている文章をつくる####
  for k,v in d.items():
    if item in v:
      index=k
      break

  nlist=[]
  for li in kakariuke_list:
    if index in li:
      for l in li:
        nlist.append(l)
  nlist=list(set(nlist))

  new_sentence=""
  for nl in nlist:
    if nl>=0:
      new_sentence += d[nl]

  #print(new_sentence)
  return new_sentence

def extract_pre_value(phrase,item):
  phrase=phrase.replace(" ","")
  phrase=zh(phrase)
  #print(phrase)
  prev_re = find_prev_re()
  
  for p in phrase.split("､"):
    if item in p:
      for pre in prev_re:
        if re.search(pre,p):
          value=re.search(pre,p).group()


  try:
    return value
  except UnboundLocalError:
    return "prev"

def calc_pre_value(float_value,_re):
  
  pencent_re = "[\d.]+%"
  value_re   = "[\d.,百千万億兆]+円"
  """
  _value = kanji_to_num(_value)

  value = kanji_to_num(_value)
  value = float(value)
  """
  if "%" in _re:
    X=re.search(pencent_re,_re).group().replace("%","")
    X=float(X)
    if "増" in _re:
      return float_value*100/(100+X)
    elif "減" in _re:
      return float_value*100/(100-X)
    else:
      return float_value*(100/X)

  elif "円" in _re:
    X=re.search(value_re,_re).group().replace("円","")
    X=float(kanji_to_num(X))
    if "増" in _re:
      return float_value-X
    elif "減" in _re:
      return float_value+X
    else:
      return 0
  else:
    return 0

def kanji_to_num(value):
      value=value.replace(",","")
      sep=True
      """漢数字をアラビア数字に変換"""
      tt_ksuji = str.maketrans('一二三四五六七八九〇壱弐参', '1234567890123')
      re_suji = re.compile(r'[十拾百千万億兆\d]+')
      re_kunit = re.compile(r'[十拾百千]|\d+')
      re_manshin = re.compile(r'[万億兆]|[^万億兆]+')
      TRANSUNIT = {'十': 10,
                   '拾': 10,
                   '百': 100,
                   '千': 1000}
      TRANSMANS = {'万': 10000,
                   '億': 100000000,
                   '兆': 1000000000000}
    
      def _transvalue(sj, re_obj=re_kunit, transdic=TRANSUNIT):
          unit = 1
          result = 0
          for piece in reversed(re_obj.findall(sj)):
              if piece in transdic:
                  if unit > 1:
                      result += unit
                  unit = transdic[piece]
              else:
                  val = int(piece) if piece.isdecimal() else _transvalue(piece)
                  result += val * unit
                  unit = 1
          if unit > 1:
              result += unit
          return result

      transuji = value.translate(tt_ksuji)
      for suji in sorted(set(re_suji.findall(transuji)), key=lambda s: len(s),reverse=True):
          if not suji.isdecimal():
              arabic = _transvalue(suji, re_manshin, TRANSMANS)
              arabic = '{:,}'.format(arabic) if sep else str(arabic)
              transuji = transuji.replace(suji, arabic)
      
      return transuji.replace("円","").replace(",","").replace("の損失","")

  

def find_reason_items():
  f = open('./txt/find_items.txt', 'r')
  items=[]
  for line in f:
    line=line.replace("\n","")
    items.append(line)
  f.close()
  return items

def find_prev_re():
  f = open('./txt/find_prev.txt', 'r')
  items=[]
  for line in f:
    line=zh(line.replace("\n","").replace("(","\(").replace(")","\)"))
    re = line.replace("dd","+[\d.,百千万億兆]+")
    items.append(re)
  f.close()
  return items

def debt_check(phrase,float_num):
  if "赤字" in phrase or "営業損失" in phrase or "の損失となりました" in phrase:
    return float_num * -1
  else:
    return float_num

def pre_phrase(phrases,i):
  #iの一個前のphrase
  if i>0:
    return phrases[i-1]
  else:
    return ""

def post_phrase(phrases,i):
  #iの一個後のphrase
  try:
    return phrases[i+1]
  except IndexError:
    return ""

def around_extract_pre_value(pre_p,phrase,post_p):
  prev_re = find_prev_re()
  
  pre=""
  for _re in prev_re:
    if re.search(_re,pre_p):
      pre=re.search(_re,pre_p).group()
  post=""
  for _re in prev_re:
    if re.search(_re,post_p):
      post=re.search(_re,post_p).group()

  # print("------------")
  # print(phrase)
  # print(pre_p)
  # print(post_p)
  # print("hh")
  # print(pre)
  # print(post)
  if len(pre)==0 and len(post)==0:
    #print("TYPE1")
    return ""
  elif len(pre) ==0 and len(post)>0:
    #print("TYPE2")
    return post
  elif len(pre) >0 and len(post)==0:
    #print("TYPE3")
    return pre
  else:
    #print("TYPE4")

    if "ました" in post_p:
      return post
    else:
      return ""



if __name__ == '__main__':
    #sentence="ドラッグ・ファーマシー事業は、営業収益6,236 億31 百万円（前期比105.3％）、営業利益220億53百万円（同118.6％）となりました。"
    sentence="営業利益は前連結会計年度に比べて846億円減少し122億円の損失となりました"
    item="営業利益"
    print(kanji_to_num("2兆8,902億32百万円"))
    # ans=extract_value(sentence,item)    
    # print(ans)
    # print("----------")
    # prev=extract_pre_value(sentence,item)
    # print(prev)
    # print("----------")
    # print(kanji_to_num(ans))
    # print("----------")
    # prev="前期比23億円(59.8%)の増益"
    # print(calc_pre_value(ans,prev))















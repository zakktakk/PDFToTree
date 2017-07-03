# -*- coding: utf-8 -*-

def compression(sentences,sent_limit=5):
  keywords_dict=keywords_open()
  score_dict={}
  for sentence in sentences:
    score=0
    for k,v in keywords_dict.items():
        if k in sentence:
            score+=v
    score_dict[sentence]=score

  mini_sentences=[]
  i=0
  for k, v in sorted(score_dict.items(), key=lambda x:x[1], reverse=True):
    if i < sent_limit and v>=0:
        mini_sentences.append(k)
        i+=1

  #順番並び替え
  ans=[]
  for sentence in sentences:
    if sentence in mini_sentences:
      ans.append(sentence)

  return ans

def keywords_open():
    f = open('./txt/keywords.txt', 'r')
    keywords={}
    for line in f:
        word  = line.split(",")[0]
        point = float(line.split(",")[1].replace("\n",""))
        keywords[word]=point
    f.close()
    return keywords

if __name__ == '__main__':
    sentence = "こんにちは。今日はいい天気ですね。朝からいい気分です。ガブリエルは最高のダンスを踊るわ。"
    sentence = "次期の当社ｸﾞﾙｰﾌﾟの連結業績における売上高､営業利益は増収･増益となる見通しです｡各ｾｸﾞﾒﾝﾄごとの概要は以下のとおりです｡繊維事業では､ｽﾊﾟﾝﾎﾞﾝﾄﾞ不織布や､ﾅｲﾛﾝ66繊維｢ﾚｵﾅ™｣を中心に販売数量の増加を見込むことなどから､増収･増益となる見通しです｡ｹﾐｶﾙ事業では､低燃費ﾀｲﾔ向け合成ｺﾞﾑやｴﾝｼﾞﾆｱﾘﾝｸﾞ樹脂､電子材料製品などで販売数量の増加を見込むものの､ｴﾁﾚﾝｾﾝﾀｰ(三菱ｹﾐｶﾙ旭化成ｴﾁﾚﾝ㈱)の定期修理による影響や原燃料価格の変動によって発生した総平均差の影響などにより､増収･減益となる見通しです｡ｴﾚｸﾄﾛﾆｸｽ事業では､ｾﾊﾟﾚｰﾀ事業の各製品で販売数量の増加を見込むことや､電子部品事業ではｵｰﾃﾞｨｵﾃﾞﾊﾞｲｽやｶﾒﾗﾓｼﾞｭｰﾙ向けなどｽﾏｰﾄﾌｫﾝ向け電子部品の販売が堅調に推移することなどから､増収･増益となる見通しです｡以上により､ｾｸﾞﾒﾝﾄ全体では増収･増益となる見通しです｡住宅事業では､建築請負部門において､労務費などの販管費が増加するものの､引渡棟数が増加することや､不動産部門の賃貸管理事業が順調に推移することなどから､増収･増益となる見通しです｡建材事業では､ﾌｪﾉｰﾙﾌｫｰﾑ断熱材｢ﾈｵﾏ™ﾌｫｰﾑ｣を中心に販売数量の増加を見込むものの､原材料費などの上昇を見込むことなどから､売上高は増収､営業利益は前期並みとなる見通しです｡以上により､ｾｸﾞﾒﾝﾄ全体では増収･増益となる見通しです｡医薬事業では､骨粗鬆症治療剤｢ﾃﾘﾎﾞﾝ™｣などの販売数量の増加を見込むものの､｢ﾃﾘﾎﾞﾝ™｣の自己投与製剤の開発に伴う研究開発費などが増加する見通しです｡医療事業では､ｳｲﾙｽ除去ﾌｨﾙﾀｰ｢ﾌﾟﾗﾉﾊﾞ™｣を中心に販売が堅調に推移する見通しです｡ｸﾘﾃｨｶﾙｹｱ事業では､営業活動強化に伴う販管費が増加するものの､着用型自動除細動器｢LifeVest™｣を中心に引き続き業績が拡大する見通しです｡以上により､ｾｸﾞﾒﾝﾄ全体では増収･増益となる見通しです｡"
    sentence = sentence.replace("､","、").replace("｡","。")
    sentences =compression(sentence.split("。"),6)
    for s in sentences:
        print(s)
        print("----------")

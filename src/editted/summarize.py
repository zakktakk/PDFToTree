# -*- coding: utf-8 -*-

import pandas as pd
from typing import Dict, List
import numpy as np

def summarize(sentences:List[str], max_sentences:int=5) -> List[str]:
    """
    @description extract high scored sentences from original sentences
    @param sentences sentence list
    @param max_sentences max extracting sentences num
    @return summarized sentences
    """
    sentences = np.array(sentences)
    keywd = read_keys()
    scores = []

    # 文ごとにスコアを計算
    for i, s in enumerate(sentences):
        score = 0
        for k, v in keywd.items():
            if k in s: score += v
        scores.append(score)

    # スコア順に抽出
    summarized_sentences = []

    for i in np.argsort(scores)[::-1][:max_sentences]:
        if scores[i] < 0: break
        summarized_sentences.append(i)

    # :thinking: listにcastする必要ないのでは
    summarized_sentences = list(sentences[np.sort(summarized_sentences)])

    return summarized_sentences


def read_keys() -> Dict[str, float]:
    """
    @description read keywords and scores
    @return keyword dict
    """
    INPUT_DIR = "../../inputs/"

    df_keywd = pd.read_csv(INPUT_DIR+'txt/keywords.txt', header=None, index_col=0)
    keywd = {k: float(v) for k, v in df_keywd.iterrows()}

    return keywd


if __name__ == '__main__':
    passage = "次期の当社ｸﾞﾙｰﾌﾟの連結業績における売上高､営業利益は増収･増益となる見通しです｡各ｾｸﾞﾒﾝﾄごとの概要は以下のとおりです｡繊維事業では､ｽﾊﾟﾝﾎﾞﾝﾄﾞ不織布や､ﾅｲﾛﾝ66繊維｢ﾚｵﾅ™｣を中心に販売数量の増加を見込むことなどから､増収･増益となる見通しです｡ｹﾐｶﾙ事業では､低燃費ﾀｲﾔ向け合成ｺﾞﾑやｴﾝｼﾞﾆｱﾘﾝｸﾞ樹脂､電子材料製品などで販売数量の増加を見込むものの､ｴﾁﾚﾝｾﾝﾀｰ(三菱ｹﾐｶﾙ旭化成ｴﾁﾚﾝ㈱)の定期修理による影響や原燃料価格の変動によって発生した総平均差の影響などにより､増収･減益となる見通しです｡ｴﾚｸﾄﾛﾆｸｽ事業では､ｾﾊﾟﾚｰﾀ事業の各製品で販売数量の増加を見込むことや､電子部品事業ではｵｰﾃﾞｨｵﾃﾞﾊﾞｲｽやｶﾒﾗﾓｼﾞｭｰﾙ向けなどｽﾏｰﾄﾌｫﾝ向け電子部品の販売が堅調に推移することなどから､増収･増益となる見通しです｡以上により､ｾｸﾞﾒﾝﾄ全体では増収･増益となる見通しです｡住宅事業では､建築請負部門において､労務費などの販管費が増加するものの､引渡棟数が増加することや､不動産部門の賃貸管理事業が順調に推移することなどから､増収･増益となる見通しです｡建材事業では､ﾌｪﾉｰﾙﾌｫｰﾑ断熱材｢ﾈｵﾏ™ﾌｫｰﾑ｣を中心に販売数量の増加を見込むものの､原材料費などの上昇を見込むことなどから､売上高は増収､営業利益は前期並みとなる見通しです｡以上により､ｾｸﾞﾒﾝﾄ全体では増収･増益となる見通しです｡医薬事業では､骨粗鬆症治療剤｢ﾃﾘﾎﾞﾝ™｣などの販売数量の増加を見込むものの､｢ﾃﾘﾎﾞﾝ™｣の自己投与製剤の開発に伴う研究開発費などが増加する見通しです｡医療事業では､ｳｲﾙｽ除去ﾌｨﾙﾀｰ｢ﾌﾟﾗﾉﾊﾞ™｣を中心に販売が堅調に推移する見通しです｡ｸﾘﾃｨｶﾙｹｱ事業では､営業活動強化に伴う販管費が増加するものの､着用型自動除細動器｢LifeVest™｣を中心に引き続き業績が拡大する見通しです｡以上により､ｾｸﾞﾒﾝﾄ全体では増収･増益となる見通しです｡"
    passage = passage.replace("､", "、").replace("｡", "。") #  この行何してるん
    result = summarize(passage.split("。"), 6)

    for r in result:
        print(r)
        print("----------")

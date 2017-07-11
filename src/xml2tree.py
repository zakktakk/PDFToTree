# author : Takuro Yamazak
# TODO 結果の外部出力, treeのママで

import mojimoji
import re
import pickle

import xml.etree.ElementTree as ET

from scipy.stats import mode
from typing import List
from anytree import Node, RenderTree

circle_num_dict = {"①":1,"②":2,"③":3,"④":4,"⑤":5,"⑥":6,"⑦":7,"⑧":8,"⑨":9,"⑩":10}

class XMLParse(object):
    def __init__(self, xml_path:str) -> None:
        """initialize
        """
        self.xml_path = xml_path
        self.tree = ET.parse(xml_path)
        self.root = self.tree.getroot()
        self.set_mokuji_page() # 目次ページを設定
        self._set_topic_param() # トピックのパラメータ設定
        # topicのみ格納する
        self.tree_dict = {"0":{"lst_pos":0, "format":None, "leftpos":None, "fontsize":None}}
        self.tree_lst = [Node("0")]
        self.tree_depth = 0
        self.is_only_pth = False
        self.is_only_rect = False
        self._make_tree() # make tree

    def set_mokuji_page(self) -> int:
        """添付資料の目次を取得, 3~5ページ目のいずれかにあるという仮説
        """
        self.mokuji = 3
        mokuji_word = "添付資料の目次"
        for i in range(3, 6):
            p = self._get_page_elm(i)[0]
            text_box_elm = p.findall("./textbox")

            for box in text_box_elm:
                text = self._get_text(box.findall(".//text"))
                if mokuji_word in text:
                    self.mokuji = i
                    return 0

    def _get_page_elm(self, page_num:int):
        """get page by index
        """
        page_num = str(page_num)
        page_elm = self.root.findall("./page[@id='"+page_num+"']")
        return page_elm

    def _get_all_page_elm(self):
        """get all xml page
        """
        all_page_elm = self.root.findall("./page[@id]")
        return all_page_elm

    def _after_mokuji_elm(self):
        """get after mokuji page
        """
        after_mokuji_page_elm = self._get_all_page_elm()[self.mokuji:]
        return after_mokuji_page_elm

    def _get_text(self, text_elm) -> str:
        """get text line
        """
        text = ""
        for t in text_elm: text += t.text
        return mojimoji.zen_to_han(text).strip() # 最後に空白と改行を削除

    def _get_text_fontsize(self, text_elm) -> float:
        """get font size
        """
        fontsize = [float(p.attrib["size"]) for p in text_elm if "size" in p.attrib]
        return mode(fontsize).mode[0]

    def _get_text_line_left(self, text_elm) -> List[float]:
        """get text line left position, [左端から, 下から]
        """
        return [float(f) for f in text_elm[0].attrib["bbox"].split(',')]

    def _get_text_line_right(self, text_elm) -> List[float]:
        """get text line right position
        """
        return [float(f) for f in text_elm[-2].attrib["bbox"].split(',')]

    def _set_topic_param(self) -> None:
        """get paragraph parameters for classify sentence is topic or paragraph
        """
        fontsize = []
        leftpos = []

        after_mokuji_page = self._get_page_elm(self.mokuji+1) # 目次の次のページ
        for page in after_mokuji_page: # pageごとに処理
            text_box_elm = page.findall("./textbox")

            for box in text_box_elm: # 1行ごとに処理
                text_elm = box.findall(".//text")
                text = self._get_text(text_elm)

                if "､" in text or "｡" in text:
                    fontsize.append(self._get_text_fontsize(text_elm))
                    lp = self._get_text_line_left(text_elm)[0]
                    leftpos.append(lp)

        self.default_fontsize = mode(fontsize).mode[0]
        self.default_left_pos = mode(leftpos).mode[0] # この指定方法がよくない？

    def _is_topic(self, text:str, leftpos:float, fontsize:float) -> str:
        """topic or notを判定する, 暫定版
        """
        if not text: # textが空行
            return ""

        elif len(text) > 30:
            return ""

        elif "｡" in text: # 丸が含まれる
            return ""

        elif re.match(r'[0-9]+ ', text): # 数字 で始まる
            t = re.search(r'[0-9]+ ', text).group().rstrip()
            return "space_num,"+t

        elif re.match(r'[0-9]+\. ', text): # 数字. で始まる
            t = re.search(r'[0-9]+\.', text).group()[:-1]
            return "dot_num,"+t

        elif re.match(r'\([0-9]+?\)', text): # (数字)で始まる
            t = re.search(r'\([0-9]+?\)', text).group().replace("(", "").replace(")", "")
            return "par_num,"+t

        elif re.match(r'[①-⑩]', text): # 丸数字で始まる
            t = re.search(r'[①-⑩]', text).group().rstrip()
            return "cir_num,"+str(circle_num_dict[t])

        elif "､" in text: # 点が含まれる
            return ""

        elif re.match(r'<.+?>', text): return "toge_pth" # <>

        elif re.match(r'\[.+?\]', text): return "dai_pth" # []

        elif re.match(r'【.+?】', text): return "chu_pth" # 【】

        elif re.match(r'「.+?」', text): return "kagi_pth" # 「」

        elif re.match(r'『.+?』', text): return "d_kagi_pth" # 『』

        elif re.match(r'[◇]', text): return "dia_rect" # ダイヤ

        elif re.match(r'[･]', text): return "dot_rect" # ドット

        elif re.match(r'[]', text): return "defdot_rect" # wordデフォダイヤ

        elif fontsize > self.default_fontsize: return "big" # 文字が大きい

        elif leftpos < self.default_left_pos - self.default_fontsize: return "left" # 通常行より左に位置する

        elif "､" not in text and "｡" not in text and len(text) < 30:
            return "mukosei"

        else: return ""

    def _is_needless(self, leftpos:float, text:str) -> bool:
        """いらない文か -> ページ番号や右上文字の除去 or 数字だけの行 or 空行
        """
        return leftpos[0] > 150 or text.replace(",", "").replace(".", "", 1).isdigit() or len(text) <= 1

    def _is_same_param(self, form1:str, fontsize1:float, form2:str, fontsize2:float) -> bool:
        """入力1と入力2が同じパラグラフか, leftpos見るとおかしくなるから無視
        """
        if form1 is not None and form2 is not None:
            return form1.split(',')[0] == form2.split(',')[0]
        return False

    def _estimate_tree_pos(self, form:str, leftpos:float, fontsize:float) -> None:
        """topicが木でどの階層に属するか
        """
        current_dict = self.tree_dict[str(self.tree_depth)]
        # 今の階層と同じparam形式
        if self._is_same_param(form, fontsize, current_dict['format'], current_dict['fontsize']): # 1個上と形式が一緒
            pass

        elif (len(form.split(',')) > 1 and form.split(',')[1] == '1'): # 数字が1 -> 階層のorigin
            self.is_only_pth = False
            self.is_only_rect = False
            self.tree_depth += 1

        elif "pth" in form: # かっこである
            self.is_only_rect = False

            if self.is_only_pth: # もしかっこかrectだけなら対応するかっこの階層に行く
                self.tree_depth = self._find_depth(form)
            else: # 新たに階層を作る
                self.tree_depth += 1
                self.is_only_pth = True

        elif "rect" in form: # unordered listである
            if self.is_only_rect: # rectだけなら対応するrectの階層に行く
                self.tree_depth = self._find_depth(form)
            else: # 新たに階層を作る
                self.tree_depth += 1
                self.is_only_rect = True

        else: # 数字
            self.is_only_rect = False
            self.is_only_pth = False
            self.tree_depth  = self._find_depth(form)

        self.tree_dict[str(self.tree_depth)] = {"lst_pos":len(self.tree_lst), "format":form, "leftpos":leftpos, "fontsize":fontsize}

    def _find_depth(self, form:str) -> int:
        """対応する階層を探す
        """
        if "," in form: # もし番号付きなら
            form  = form.split(',')
            for p in range(self.tree_depth-1, 0, -1):
                p = str(p)
                ll = self.tree_dict[p]["format"].split(',')
                if len(ll) > 1:
                    if ll[0] == form[0] and int(ll[1]) == int(form[1])-1:
                        return int(p)
        else:
            for p in range(self.tree_depth-1, 0, -1):
                p = str(p)
                if form == self.tree_dict[p]["format"]:
                    return int(p)
        return self.tree_depth + 1

    def _make_tree(self) -> None:
        """xmlからanytreeを作成する
        """
        after_mokuji_page = self._after_mokuji_elm() #目次ページ以降を読み込み
        paragraph = ""

        for page in after_mokuji_page: # pageごとに処理
            text_box_elm = page.findall("./textbox")

            for box in text_box_elm: # 1行ごとに処理
                text = box.findall(".//text")

                leftpos = self._get_text_line_left(text)
                fontsize = self._get_text_fontsize(text)
                tt = self._get_text(text).split('\n')

                for t in tt: # なんか間に改行が含まれることがある
                    # もし不要行でなければ処理
                    if not self._is_needless(leftpos, t):
                        form = self._is_topic(t, leftpos[0], fontsize)
                        if form: # もしトピックならば
                            if paragraph: # もしparagraphにテキストが溜まってたら
                                splitted_p = paragraph.split("｡")
                                for p in splitted_p:
                                    if p:
                                        p = p + "｡"
                                        self.tree_lst.append(Node(p, parent=self.tree_lst[self.tree_dict[str(self.tree_depth)]["lst_pos"]]))
                                paragraph = ""

                            self._estimate_tree_pos(form, leftpos, fontsize)
                            self.tree_lst.append(Node(t, parent=self.tree_lst[self.tree_dict[str(self.tree_depth-1)]["lst_pos"]]))

                        else:
                            paragraph += t.replace('\n', '').replace(' ', '')

        self.tree_lst.append(Node(paragraph, parent=self.tree_lst[self.tree_dict[str(self.tree_depth)]["lst_pos"]]))

    def save_txt(self, file_path:str) -> None:
        with open(file_path, "w") as w_f:
            for pre, fill, node in RenderTree(self.tree_lst[0]):
                w_f.write("%s%s\n" % (pre, node.name))

    def save_pickle(self, file_path:str) -> None:
        with open(file_path, "wb") as w_f:
            pickle.dump(self.tree_lst, w_f)

if __name__ == "__main__":
    tr = XMLParse("../tmp/xml/8167 Aeon.xml")
    # tr.save_txt("../outputs/txt/8167 Aeon.xml.txt")

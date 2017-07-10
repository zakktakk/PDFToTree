import xml.etree.ElementTree as ET
import mojimoji

from typing import List
from anytree import *
import statistics
import re

####
# アルゴリズム
# 残すべきものreでとった判定，ポジション，親，現在の値
# もし新しいものの
# ###

# if fontsize > self.default_fontsize:
#     print('size')
#     return True
# -> 検証したけどsizeでやるのは悪手っぽい
#
# circle_num_dict = {"①":1,"②":2,"③":3,"④":4,"⑤":5,"⑥":6,"⑦":7,"⑧":8,"⑨":9,"⑩":10}

class XMLParse(object):
    def __init__(self, xml_path:str):
        """initialize
        """
        self.xml_path = xml_path
        self.tree = ET.parse(xml_path)
        self.root = self.tree.getroot()
        self.tree_dict = {"0":{"lst_pos":0, "parent":"0", "format":None, "leftpos":0, "fontsize":0}}
        self.tree_lst = [Node("0")]
        self.tree_depth = 0
        # self.set_topic_param()

    def get_page_elm(self, page_num:int):
        """get page by index
        """
        page_num = str(page_num)
        page_elm = self.root.findall("./page[@id='"+page_num+"']")
        return page_elm

    def get_all_page_elm(self):
        """get all xml page
        """
        all_page_elm = self.root.findall("./page[@id]")
        return all_page_elm

    def after_mokuji_elm(self, mokuji=3):
        """get after mokuji page
        """
        after_mokuji_page_elm = self.get_all_page_elm()[mokuji:]
        return after_mokuji_page_elm

    def get_text(self, text_elm):
        """get text line
        """
        text = ""
        for t in text_elm: text += t.text
        return mojimoji.zen_to_han(text).strip() # 最後に空白と改行を削除

    def get_text_fontsize(self, text_elm):
        """get font size
        """
        fontsize = [float(p.attrib["size"]) for p in text_elm if "size" in p.attrib]
        return statistics.mode(fontsize)

    def get_text_line_left(self, text_elm):
        """get text line left position, [左端から, 下から]
        """
        return [float(f) for f in text_elm[0].attrib["bbox"].split(',')]

    def get_text_line_right(self, text_elm):
        """get text line right position
        """
        return [float(f) for f in text_elm[-2].attrib["bbox"].split(',')]

    # def set_topic_param(self):
    #     """get paragraph parameters for classify sentence is topic or paragraph
    #     -> いらない？
    #     """
    #     fontsize = []
    #     leftpos = []
    #     rightpos = []
    #
    #     after_mokuji_page = self.after_mokuji_elm(mokuji=3)
    #     for page in after_mokuji_page: # pageごとに処理
    #         text_box_elm = page.findall("./textbox")
    #         for box in text_box_elm: # 1行ごとに処理
    #             text = box.findall(".//text")
    #             fontsize.append(self.get_text_fontsize(text))
    #             leftpos.append(self.get_text_line_left(text)[0])
    #             rightpos.append(self.get_text_line_right(text)[0])
    #
    #     self.default_fontsize = statistics.mode(fontsize)
    #     self.default_left_pos = statistics.mode(leftpos)
    #     self.default_right_pos = statistics.mode(rightpos)


    def is_topic(self, pos, fontsize, text):
        """topic or notを判定する, 暫定版
        これtrue返す必要ないな
        """
        if not text:
            return None

        if re.match(r'[･]', text):
            return "dot"

        if re.match(r'[0-9] ', text):
            return "num"

        if re.match(r'\([0-9]+?\)', text):
            return "par_num"

        if re.match(r'<.+?>', text):
            return "toge"

        if re.match(r'\[.+?\]', text):
            return "dai"

        if re.match(r'[①-⑩]', text):
            return "cir_num"

        if re.match(r'【.+?】', text):
            return "chu"

        if re.match(r'「.+?」', text):
            return "kagi"

        if re.match(r'『.+?』', text):
            return "d_kagi"

        return None

    def is_needless(self, leftpos, text):
        """いらない文か -> ページ番号や右上文字の除去 or 数字だけの行 or 空行
        """
        return leftpos[0] > 150 or text.replace(".", "", 1).isdigit() or text == ''

    # def is_same_paragraph(self, pos1, pos2, fontsize1, fontsize2):
    # 文がtopicでなければsame paragraph!!
    #     """pos -> (leftpos, rightpos), 行の左右どちらかの位置が等しい and 文字の大きさが等しい
    #     """
    #     return (fontsize1 == fontsize2) # and (pos1[0][0] == pos2[0][0] or pos1[1][2] == pos2[1][2])

    def make_tree(self):
        after_mokuji_page = self.after_mokuji_elm(mokuji=3)
        for page in after_mokuji_page: # pageごとに処理
            text_box_elm = page.findall("./textbox")

            prev_leftpos = (0,0,0,0)
            prev_rightpos = (0,0,0,0)
            prev_fontsize = 0
            sentence = ""

            for box in text_box_elm: # 1行ごとに処理
                text = box.findall(".//text")
                leftpos = self.get_text_line_left(text)
                rightpos = self.get_text_line_right(text)
                fontsize = self.get_text_fontsize(text)
                t = self.get_text(text)

                # もし不要行でなければ処理
                if not self.is_needless(leftpos, t):
                    # もしトピックならば
                    if self.is_topic((leftpos, rightpos), fontsize, t):
                        # 同じレベルのトピックか？ -> 連続してたら少なくとも違う?
                        print(t)

                    else:
                        # もし同一パラグラフなら
                        if self.is_same_paragraph((leftpos, rightpos),\
                                                  (prev_leftpos, prev_rightpos),\
                                                  fontsize, prev_fontsize):
                            sentence += t
                        else:
                            # tree_lst.append(Node(str(len(tree_lst)), parent=tree_lst[tree_dict[tree_dict[str(tree_depth)])["parent"]]["lst_pos"]])
                            sentence = t

                    prev_leftpos = leftpos
                    prev_rightpos = rightpos
                    prev_fontsize = fontsize


a = XMLParse("./hoge.xml")
a.make_tree()

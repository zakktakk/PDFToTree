# author : Takuro Yamazaki

import mojimoji
import statistics
import re

import xml.etree.ElementTree as ET

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
        self.set_topic_param()
        # topicのみ格納する
        self.tree_dict = {"0":{"lst_pos":0, "format":None, "leftpos":None, "fontsize":None}}
        self.tree_lst = [Node("0")]
        self.tree_depth = 0

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

    def get_text(self, text_elm) -> str:
        """get text line
        """
        text = ""
        for t in text_elm: text += t.text
        return mojimoji.zen_to_han(text).strip() # 最後に空白と改行を削除

    def get_text_fontsize(self, text_elm) -> float:
        """get font size
        """
        fontsize = [float(p.attrib["size"]) for p in text_elm if "size" in p.attrib]
        return statistics.mode(fontsize)

    def get_text_line_left(self, text_elm) -> List[float]:
        """get text line left position, [左端から, 下から]
        """
        return [float(f) for f in text_elm[0].attrib["bbox"].split(',')]

    def get_text_line_right(self, text_elm) -> List[float]:
        """get text line right position
        """
        return [float(f) for f in text_elm[-2].attrib["bbox"].split(',')]

    def set_topic_param(self):
        """get paragraph parameters for classify sentence is topic or paragraph
        """
        fontsize = []
        leftpos = []

        after_mokuji_page = self.after_mokuji_elm(mokuji=3)
        for page in after_mokuji_page: # pageごとに処理
            text_box_elm = page.findall("./textbox")
            for box in text_box_elm: # 1行ごとに処理
                text = box.findall(".//text")
                fontsize.append(self.get_text_fontsize(text))
                leftpos.append(self.get_text_line_left(text)[0])

        self.default_fontsize = statistics.mode(fontsize)
        self.default_left_pos = statistics.mode(leftpos)

    def is_topic(self, text:str, leftpos) -> str:
        """topic or notを判定する, 暫定版
        これtrue返す必要ないな
        """
        if not text:
            return ""

        if re.match(r'[･]', text):
            return "dot"

        if re.match(r'[0-9]+ ', text):
            t = re.search(r'[0-9]+ ', text).group().rstrip()
            return "space_num,"+t

        if re.match(r'[0-9]+\.', text):
            t = re.search(r'[0-9]+\.', text).group()[:-1]
            return "dot_num,"+t

        if re.match(r'\([0-9]+?\)', text):
            t = re.search(r'\([0-9]+?\)', text).group().replace("(", "").replace(")", "")
            return "par_num,"+t

        if re.match(r'[①-⑩]', text):
            t = re.search(r'[①-⑩]', text).group().rstrip()
            return "cir_num,"+str(circle_num_dict[t])

        if re.match(r'<.+?>', text):
            return "toge"

        if re.match(r'\[.+?\]', text):
            return "dai"

        if re.match(r'【.+?】', text):
            return "chu"

        if re.match(r'「.+?」', text):
            return "kagi"

        if re.match(r'『.+?』', text):
            return "d_kagi"

        if re.match(r'[◇]', text):
            return "dia"

        return ""

    def is_needless(self, leftpos, text) -> bool:
        """いらない文か -> ページ番号や右上文字の除去 or 数字だけの行 or 空行
        """
        return leftpos[0] > 150 or text.replace(",", "").replace(".", "", 1).isdigit() or len(text) <= 1

    def is_same_param(self, form1, fontsize1, form2, fontsize2):
        return (fontsize1 == fontsize2) and (form1.split(',')[0] == form2.split(',')[0])

    def estimate_tree_pos(self, form, leftpos, fontsize) -> None:
        current_dict = self.tree_dict[str(self.tree_depth)]
        # 今の階層と同じparam形式
        if self.is_same_param(form, fontsize, current_dict['format'], current_dict['fontsize']):
            self.tree_dict[str(self.tree_depth)] = {"lst_pos":len(self.tree_lst), "format":form, "leftpos":leftpos, "fontsize":fontsize}

        elif (not "num" in form) or (len(form.split(',')) > 1 and form.split(',')[1] == '1'):
            self.tree_depth += 1
            self.tree_dict[str(self.tree_depth)] = {"lst_pos":len(self.tree_lst), "format":form, "leftpos":leftpos, "fontsize":fontsize}

        else:
            self.tree_depth  = self.estimate_back(form)
            self.tree_dict[str(self.tree_depth)] = {"lst_pos":len(self.tree_lst), "format":form, "leftpos":leftpos, "fontsize":fontsize}


    def estimate_back(self, form) -> int:
        # 整合性のあう数字が存在するか否か
        form  = form.split(',')
        for p in range(self.tree_depth-1, 0, -1):
            p = str(p)
            ll = self.tree_dict[p]["format"].split(',')
            if len(ll) > 1:
                if ll[0] == form[0] and int(ll[1]) == int(form[1])-1:
                    return int(p)
        return self.tree_depth + 1


    def make_tree(self):
        after_mokuji_page = self.after_mokuji_elm(mokuji=3)
        paragraph = ""

        for page in after_mokuji_page: # pageごとに処理
            text_box_elm = page.findall("./textbox")

            for box in text_box_elm: # 1行ごとに処理
                text = box.findall(".//text")

                leftpos = self.get_text_line_left(text)
                fontsize = self.get_text_fontsize(text)
                tt = self.get_text(text).split('\n')

                for t in tt # なんか間に改行が含まれることがある
                    # もし不要行でなければ処理
                    if not self.is_needless(leftpos, t):
                        form = self.is_topic(t, leftpos[0])
                        if form: # もしトピックならば
                            if paragraph: # もしparagraphにテキストが溜まってたら
                                self.tree_lst.append(Node(paragraph, parent=self.tree_lst[self.tree_dict[str(self.tree_depth)]["lst_pos"]]))
                                paragraph = ""

                            self.estimate_tree_pos(form, leftpos, fontsize)
                            self.tree_lst.append(Node(t, parent=self.tree_lst[self.tree_dict[str(self.tree_depth-1)]["lst_pos"]]))

                        else:
                            paragraph += t.replace('\n', '').replace(' ', '')

        for pre, fill, node in RenderTree(self.tree_lst[0]):
            print("%s%s" % (pre, node.name))

a = XMLParse("./smbc.xml")
a.make_tree()

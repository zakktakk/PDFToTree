import xml.etree.ElementTree as ET

from typing import List
from anytree import *

class XMLParse(object):
    def __init__(self, xml_path:str):
        """initialize
        """
        self.xml_path = xml_path
        self.tree = ET.parse(xml_path)
        self.root = self.tree.getroot()

    # def get_page_elm(self, page_num:int):
    #     """get page by index
    #     """
    #     page_num = str(page_num)
    #     page_elm = self.root.findall("./page[@id='"+page_num+"']")
    #     return page_elm

    def get_all_page_elm(self):
        """get all xml page
        """
        all_page_elm = self.root.findall("./page[@id]")
        reutn all_page_elm

    def after_mokuji_elm(self, mokuji=3):
        """get after mokuji page
        """
        after_mokuji_page_elm = self.get_all_page_elm()[mokuji:]
        return after_mokuji_page_elm

    def get_text_box_elm(self, page_elm):
        text_box_elm = page_elm.findall("./textbox")
        return text_box_elm

    def get_text_elm(self, text_box_elm):
        text_elm = page_elm.findall("./text")
        return text_elm

    def get_text(self, text_elm):
        text = ""
        for t in text_elm: text += t.text
        return text

    def get_text_fontsize(self, text_elm):
        

    def make_tree(self):
        # ページごとにvalを取得
        after_mokuji_page = after_mokuji_elm()
        for page in after_mokuji_page:
            text_box_elm = get_text_box_elm(page)
            for box in text_box_elm:
                text = get_text_elm(box)



a = XMLParse("./nakami.xml")
a.get_page_num()

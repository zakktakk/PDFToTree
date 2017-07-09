# FREEZE
# author : Takuro Yamazaki
# 結論 : anytreeはリストを使えばできる，やはり距離と文字の大きさでやったほうがいいのでは

import re
import mojimoji

from io import StringIO

from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams

def get_mokuji(pdf_path:str):
    """
    目次の数字内包を取るのが無理だわ
    @description get mokuji of object pdf file, mokuji must be at page 3
    @param pdf_path pdf file
    @return anytree format mokuji
    """
    mokuji = read_mokuji(pdf_path).strip().split("\n")

    # dict
    # {line : {"val":hoge, "parent":huga}}
    mokuji_dict = {}
    prev_line_str = None

    for line in mokuji:
        # 半角に置換し，空白削除
        line = mojimoji.zen_to_han(line).strip()

        # 文字から文字でなく，最後がページ番号で終わっていたら
        if line and line.split()[-1].isdigit():
            line = line.replace('…', ' ').replace('･', ' ').replace('.', ' ').replace(')', ') ').split()[:-1]
            # もし先頭が"数字"もしくは"(数字)"の形だったら -> この形以外あり得るのか？
            # 正規表現でうまくやりたかったけどわからんから暫定処理
            # 1.1とかあったらやばい
            if line and re.search(r"^[0-9]{1,}$", line[0].replace('(', '').replace(')', '')):
                num = int(line[0].replace('(', '').replace(')', ''))
                line_str = " ".join(line[1:])

                if prev_num + 1 == num:
                    mokuji_dict[line_str] = {"val":num, "parent":mokuji_dict[prev_line_str]['parent']}
                else:
                    mokuji_dict[line_str] = {"val":num, "parent":prev_line_str}

                prev_line_str = line_str
                prev_num = num


def read_mokuji(path:str) -> str:
    """
    @description get text on input pdf
    @param path path to pdf file
    @return text on pdf
    """

    # set option -> ここは引数に追加すべき?
    # debug option
    debug = 0

    # output option
    pagenos = set([2]) # 目次のページのみ取得
    maxpages = 0
    password = ""
    imagewriter = None
    codec = 'utf-8'
    caching = True
    laparams = LAParams()
    #

    retstr = StringIO()
    rsrcmgr = PDFResourceManager(caching=caching)
    laparams.detect_vertical = True
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams,
                               imagewriter=imagewriter)

    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for number, page in enumerate(PDFPage.get_pages(fp, pagenos,
                                    maxpages=maxpages, password=password,
                                    caching=caching, check_extractable=True)):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()

    return text

get_mokuji('../../inputs/pdf/3407Asahikasei.pdf')
print("-------------------------------------")
get_mokuji('../../inputs/pdf/8316 SMBC.pdf')
print("-------------------------------------")
get_mokuji('../../inputs/pdf/8167 Aeon.pdf')

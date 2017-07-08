# -*- coding: utf-8 -*-
# ref : http://qiita.com/korkewriya/items/72de38fc506ab37b4f2d

import sys
import os
import zenhan

from io import StringIO

from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
from pdfminer.image import ImageWriter

from subprocess import call
from tqdm import tqdm
from PyPDF2 import PdfFileWriter, PdfFileReader

def pdf_to_text(path):
    try:
        text=read(path)

    except:
        #PDFのdecrypt
        pdf_filename_decr=os.getcwd()+"/decrypted.pdf"
        command="qpdf --password='' --decrypt "+path+" "+pdf_filename_decr

        call('qpdf --password=%s --decrypt %s %s' %('', path, pdf_filename_decr), shell=True)
        os.system(command)

        text=read(pdf_filename_decr)


    text = str(zenhan.z2h(text))
    text = text.replace("〜","~").replace("ー","-").replace("\x0c","").replace("\xa0","")

    new_text=""
    for text in text.split("\n"):
        if ("株" in text or "㈱" in text) and "平成" in text and "決算短信" in text:
            for t in text.split("-"):
                if 0<len(t) \
                    and not(("株" in t or "㈱" in t) and "平成" in t and "決算短信" in t) \
                    and not(t.replace("-","").replace(" ","").isdigit()):

                    if "､" not in t and "｡" not in t and len(t)<30:
                        new_text+="\n"+t+"\n"
                    else:
                         new_text+=t

        elif 0<len(text.replace(" ","")) \
            and not(("株" in text or "㈱" in text) and "平成" in text and "決算短信" in text) \
            and not(text.replace("-","").replace(" ","").isdigit()):

            if "､" not in text and "｡" not in text and len(text)<30:
              new_text+="\n"+text+"\n"
            else:
              new_text+=text


    return new_text

def read(path, debug=0, password='', pagenos=set(), maxpages=0, outfile=None,
         outtype=None, imagewriter=None, rotation=0, stripcontrol=False,
         layoutmode='normal', codec='utf-8', pageno=1, scale=1,
         caching=True, showpageno=True, laparams=LAParams()):
    """
    @description get text on input pdf
    @param path path to pdf file
    @return text on pdf
    """
    import re
    space = re.compile(r"[ 　]+")

    retstr = StringIO()

    PDFDocument.debug = debug
    PDFParser.debug = debug
    CMapDB.debug = debug
    PDFPageInterpreter.debug = debug

    rsrcmgr = PDFResourceManager(caching=caching)
    laparams.detect_vertical = True
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams,
                               imagewriter=imagewriter)

    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pages = PdfFileReader(path, "rb").getNumPages()
    flag = True

    for number,page in enumerate(PDFPage.get_pages(fp, pagenos,
                                    maxpages=maxpages, password=password,
                                    caching=caching, check_extractable=True)):
        if "Toyota" in path:
            if number > pages-5:
                flag=False
        if flag:
            page.rotate = (page.rotate+rotation) % 360
            interpreter.process_page(page)

    text = retstr.getvalue()
    text = re.sub(space, "", text) # これが必要か要検討

    fp.close()
    device.close()

    return text

if __name__ == '__main__':
    path = "../../inputs/pdf/nakami.pdf"

    print(read(path))

# -*- coding: utf-8 -*-

from tqdm import tqdm
from io import StringIO

from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams

def read(path, debug=0, password='', pagenos=set(), maxpages=0, outfile=None,
         outtype=None, imagewriter=None, rotation=0, stripcontrol=False,
         layoutmode='normal', codec='utf-8', pageno=1, scale=1,
         caching=True, showpageno=True, laparams=LAParams()):
    """
    @description get text on input pdf
    @param path path to pdf file
    @return text on pdf
    """

        retstr = StringIO()

        PDFDocument.debug = debug
        PDFParser.debug = debug
        CMapDB.debug = debug
        PDFPageInterpreter.debug = debug

        rsrcmgr = PDFResourceManager(caching=caching)
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams,
                                   imagewriter=imagewriter)

        fp = open(path, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        pbar = tqdm(total=30)
        for number,page in enumerate(PDFPage.get_pages(fp, pagenos,
                                        maxpages=maxpages, password=password,
                                        caching=caching, check_extractable=True)):
                page.rotate = (page.rotate+rotation) % 360
                interpreter.process_page(page)
                pbar.update(1)
        text = retstr.getvalue()

        fp.close()
        device.close()

        return text


if __name__ == '__main__':
    path = "../../inputs/pdf/4503 Astellas Pharma.pdf"

    print(read(path))

# -*-coding: utf-8-*-
# author : Takuro Yamazaki
# ref : https://github.com/euske/pdfminer/blob/master/tools/pdf2txt.py

import os

from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams

from subprocess import call

def pdf2xml(pdf_path:str, xml_path:str) -> None:
    try:
        read(pdf_path, xml_path)

    except:
        #PDFのdecrypt
        decr_pdf_path = os.getcwd() + "/decrypted.pdf"
        command = "qpdf --password='' --decrypt " + pdf_path + " " + decr_pdf_path

        call('qpdf --password=%s --decrypt %s %s' %('', pdf_path, decr_pdf_path), shell=True)
        os.system(command)

        read(decr_pdf_path, xml_path)


def read(pdf_path:str, xml_path:str) -> None:
    """
    @description convert pdf file to xml file
    @param pdf_path input pdf file path
    @param xml_path output xml file path
    """

    # set option -> ここは引数に追加すべき?
    # output option
    pagenos = set()
    maxpages = 0

    password = ''
    imagewriter = None
    codec = 'utf-8'
    caching = True
    laparams = LAParams()
    #

    # open output xml file
    outfp = open(xml_path, 'wb')
    rsrcmgr = PDFResourceManager(caching=caching)
    device = XMLConverter(rsrcmgr, outfp, codec=codec, laparams=laparams,
                          imagewriter=imagewriter)

    # read pdf file and convert to xml
    fp = open(pdf_path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(fp, pagenos,
                                  maxpages=maxpages, password=password,
                                  caching=caching, check_extractable=True):
        interpreter.process_page(page)

    # file close
    fp.close()
    device.close()
    outfp.close()

#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import sys
from cStringIO import StringIO
#from io import StringIO
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
from pdfminer.image import ImageWriter
import getopt
import os
from subprocess import call
import requests
import PyPDF2
import zenhan
from tqdm import tqdm
from PyPDF2 import PdfFileWriter, PdfFileReader
def read(path):
        # debug option
        debug = 0
        # input option
        password = ''
        pagenos = set()
        maxpages = 0
        # output option
        outfile = None
        outtype = None
        imagewriter = None
        rotation = 0
        stripcontrol = False
        layoutmode = 'normal'
        codec = 'utf-8'
        pageno = 1
        scale = 1
        caching = True
        showpageno = True
        laparams = LAParams()


        retstr = StringIO()
        
        
        PDFDocument.debug = debug
        PDFParser.debug = debug
        CMapDB.debug = debug
        PDFPageInterpreter.debug = debug
    
        rsrcmgr = PDFResourceManager(caching=caching)
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams,
                                   imagewriter=imagewriter)
        #fp = file(path, 'rb')
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

def second(path):
    import PyPDF2
    pdfFileObj = open(path,'rb')     #'rb' for read binary mode
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pdfReader.numPages

    pageObj = pdfReader.getPage(9)          #'9' is the page number
    pageObj.extractText()



if __name__ == '__main__':
    #path=os.getcwd()+"/decrypted.pdf"
    path="/Users/tomoki/Downloads/TDNET/decryp.pdf"
    #path="/Users/tomoki/Downloads/TDNET/8316 SMBC.pdf"

    read(path)









# -*-coding: utf-8-*-
# author : Takuro Yamazaki
# ref : https://github.com/euske/pdfminer/blob/master/tools/pdf2txt.py

from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams

from subprocess import call

def pdf2xml(pdf_path:str, xml_path:str):
    try:
        read(pdf_path, xml_path)

    except:
        #PDFのdecrypt
        decr_pdf_path = os.getcwd() + "/decrypted.pdf"
        command = "qpdf --password='' --decrypt " + path + " " + pdf_filename_decr

        call('qpdf --password=%s --decrypt %s %s' %('', path, pdf_filename_decr), shell=True)
        os.system(command)

        read(decr_pdf_path, xml_path)
        command = "rm " + decr_pdf_path
        call('rm %s' % (decr_pdf_path), shell=True)
        os.system(command)


def read(pdf_path:str, xml_path:str, password:str='') -> None:
    """
    @description convert pdf file to xml file
    @param pdf_path input pdf file path
    @param xml_path output xml file path
    @param password optional parameter, if object pdf is locked, should be added
    """

    # set option -> ここは引数に追加すべき?
    # output option
    pagenos = set()
    maxpages = 0

    outfile = xml_path  # xml file path

    imagewriter = None
    codec = 'utf-8'
    caching = True
    laparams = LAParams()
    #

    # open output xml file
    outfp = open(outfile, 'wb')
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

if __name__ == '__main__':
    INPUT = "../../inputs/pdf/3407Asahikasei.pdf"
    OUTPUT = "./asahikasei.xml"
    read(INPUT, OUTPUT)

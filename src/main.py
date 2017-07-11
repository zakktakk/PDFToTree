# author : Takuro Yamazaki

import os
import sys
import glob
import getopt

from pdf2xml import pdf2xml # pdfをxmlに変換
from xml2tree import XMLParse # xmlをanytreeの形式に変換


def main(argv) -> None:
    def usage():
        print("usage: %s [-d dirname] [-f filename]" % argv[0])
        return 1

    try:
        (opts, args) = getopt.getopt(argv[1:], 'd:t:')
    except getopt.GetoptError:
        return usage()

    if not len(argv) == 3:
        return usage()

    opt, obj = opts[0]
    obj = os.getcwd() + "/" + obj

    if opt == "-d":
        if not os.path.isdir(obj):
            print("not exist directory")
            return 1
        pdfs = glob.glob(obj+"/*.pdf")

    elif opt == "-f":
        if not os.path.isfile(obj):
            print("not exist file!!")
            return 1

        pdfs = [obj]

    for pdf_path in pdfs:
        print("processing "+ pdf_path.split("/")[-1])
        xml_path = "../tmp/xml/" + pdf_path.split("/")[-1].replace(".pdf", ".xml")
        save_file_path = "../outputs/txt/" + pdf_path.split("/")[-1].replace(".pdf", ".txt")

        pdf2xml(pdf_path, xml_path)

        # xmlをanytreeの形式に変換
        parse = XMLParse(xml_path)
        parse.save_txt(save_file_path)

if __name__ == '__main__': sys.exit(main(sys.argv))

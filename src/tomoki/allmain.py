# -*- coding: utf-8 -*-
#実行環境anaconda3-4.2.0
import read_pdf
from CorporateInfo import CorporateAnalysis 

#pdfファイまでのパス
path1="/Users/tomoki/Downloads/TDNET/3407Asahikasei.pdf"
path2="/Users/tomoki/Downloads/TDNET/7203 Nissan.pdf"
path3="/Users/tomoki/Downloads/TDNET/4503 Astellas Pharma.pdf"
path4="/Users/tomoki/Downloads/TDNET/8167 Aeon.pdf"
path5="/Users/tomoki/Downloads/TDNET/8316 SMBC.pdf"
path6="/Users/tomoki/Downloads/TDNET/9983 Fierstretailing.pdf"
path7="/Users/tomoki/Downloads/TDNET/7203 Toyota.pdf"
#path="/Users/tomoki/Downloads/TDNET/8002 Marubeni.pdf"
#path="/Users/tomoki/Downloads/TDNET/MARU_1703_tanshin_jpn.pdf"
#path="/Users/tomoki/Downloads/TDNET/decry.pdf"
#path="/Users/tomoki/Downloads/TDNET/MARU_16123Q_tanshin_jpn.pdf"
path_list=[path1,path2,path3,path4,path5,path6,path7]


def main(path,savepath):
    raw_text = read_pdf.pdf_to_text(path)
    CA = CorporateAnalysis(raw_text)
    CA.write_json(savepath)


def allmain():
    for path in path_list:
        savepath=path.split('/')[-1][:-3]+'json'
        main(path,savepath)


if __name__ == '__main__':

    # path_list内全てのpdfに対してmainを行う。
    allmain()
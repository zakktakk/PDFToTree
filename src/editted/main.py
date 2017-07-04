# -*- coding: utf-8 -*-
# TODO INPUT_DIRとかの定義をconfigに
# TODO allmainとmainの役割のを作る(今はmainの方消しちゃった)

import glob

import read_pdf

from CorporateInfo import CorporateAnalysis
from typing import List


PDF_INPUT_DIR = "../../inputs/pdf/"
JSON_OUTPUT_DIR = "../../outputs/json/"

def pdf2json(path:str, savepath:str) -> None:
    """
    @description function for convert pdf to json file
    @param path path to pdf file
    @param savepath path for converted json file
    """
    raw_text = read_pdf.pdf_to_text(path)
    CA = CorporateAnalysis(raw_text)
    CA.write_json(savepath)

def main(pdf_paths:List[str]) -> None:
    """
    @description main function for convert pdf files to json files
    @param pdfs paths to pdf files
    """
    for p in pdf_paths:
        savepath = p.replace(PDF_INPUT_DIR, JSON_OUTPUT_DIR).replace("pdf", "json")
        pdf2json(p, savepath)

if __name__ == "__main__":
    # path to pdf
    pdfs = glob.glob(INPUT_DIR + "*.pdf")
    main(pdfs)

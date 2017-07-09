
# author : Takuro Yamazaki
# ディレクトリを指定するとその中の全てのファイルにする？
# ↑みたいなめんどいのはあとで

from pdf2xml import pdf2xml # pdfをxmlに変換
import xml_parse # xmlをanytreeの形式に変換

def main(pdf_path:str, xml_path:str=None, password:str='') -> None:
    # pdfをxmlに変換(tmpファイルに出力)
    if xml_path is None:
        xml_path = "../../tmp/tmp.xml"
    pdf2xml(pdf_path, xml_path, password)

    # xmlをanytreeの形式に変換
    huga
    return hagu

if __name__ == '__main__':
    pdf_path = "../../inputs/pdf/nakami.pdf"
    main(pdf_path)

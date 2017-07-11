# author : Takuro Yamazaki
# TODO usageとdir or fileの実装

from pdf2xml import pdf2xml # pdfをxmlに変換
from xml2tree import XMLParse # xmlをanytreeの形式に変換

def main(pdf_path:str, xml_path:str=None) -> None:
    # pdfをxmlに変換(tmpファイルに出力)
    if xml_path is None:
        xml_path = "../../tmp/" + pdf_path.split("/")[-1].replace(".pdf", ".xml")

    pdf2xml(pdf_path, xml_path, password)

    # xmlをanytreeの形式に変換
    parse = XMLParse(xml_path)
    parse.make_tree()

if __name__ == '__main__': sys.exit(main(sys.argv))

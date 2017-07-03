# -*- coding: utf-8 -*- 
from utils import *
from section import Section

class Document(object):
    def __init__(self,document_dir):
        self.document_dir = document_dir
        self.document_name = self.document_dir.split("/")[-1][:-4]
        self.process()

    def process(self):
        self.read_html()
        self.soup = BeautifulSoup(self.html,'html.parser').find("body")
        self.body = str(self.soup)
        self.soup = BeautifulSoup(self.body,'html.parser')
        self.separage_from_page2()
        self.retrive_trash()
        self.get_sections()

    def read_html(self):
        f = open(self.document_dir,"r")
        self.html = f.read().replace("\n","")
        f.close()

    def retrive_trash(self):
        for page in self.soup.findAll("a"): #remove pages
            page.parent.extract()
        for pattern in [6,7,9,10]:
            for e in self.soup.findAll("span",style=re.compile(r"font-family:.*?font-size:"+str(pattern)+"px")):
                e.extract()
        for pattern in ["span","div"]:
            for e in self.soup.findAll(pattern):
                if e.text == "":
                    e.extract()

    def separage_from_page2(self):
        for page in self.soup.findAll("a"):
            if page["name"] == "4": #page 以降のみ
                separete_flag = page.parent
        self.body = self.body.split(str(separete_flag))[1]
        self.soup = BeautifulSoup(self.body,'html.parser')

    def get_sections(self):
        self.sections = []
        # get title
        for title in self.soup.findAll("span",style=re.compile(r"font-family:.*?font-size:13px")):
            if len(title.text) > 0 and title.text[0] in tags:
                title["style"] = "font-family:MS-Mincho;font-size:12px"
                section = Section(title.text)
                self.sections.append(section)
        # get contents
        all_section_titles = [s.title for s in self.sections]
        for s in self.sections:
            s.get_contents(all_section_titles,self.soup)
            s.get_paragraph()

    def extract_topic(self,keys):
        extracted_sections = []
        for section in self.sections:
            flag = False
            for key in keys:
                if section.title.find(key) > -1:
                    flag = True
                else:
                    flag = False
            if flag == True:
                extracted_sections.append(section)
        self.sections = extracted_sections

    def get_nouns(self):
        self.nouns = []
        for section in self.sections:
            section.get_nouns()
            for noun in section.nouns:
                self.nouns.append(noun)

import io

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import markovify

class autoarticle:
    """Class to create a text from PDF(s) in a directory 
    with path(s) in listings
    """

    def __init__(self, listings):
        self.listings = listings
        self.text = ""

    def convert_pdf_to_txt(self, path):
        """Directly from stackoverflow
        """
        rsrcmgr = PDFResourceManager()
        retstr = io.StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        fp = open(path, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()

        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                                  password=password,
                                  caching=caching,
                                  check_extractable=True):
            interpreter.process_page(page)

        text = retstr.getvalue()

        fp.close()
        device.close()
        retstr.close()
        self.text = text
    
    def create_article(self):
        text_model = markovify.Text(self.text)
        
        for i in range(0, 40):
            print(text_model.make_sentence())


def main():
    aa = autoarticle("C:\\Users\\Emil\\Documents\\HeHE\\source\\2019-04_webb.pdf")
    aa.convert_pdf_to_txt("C:\\Users\\Emil\\Documents\\HeHE\\source\\2019-04_webb.pdf")
    aa.create_article()

if __name__ == "__main__":
    main()
        

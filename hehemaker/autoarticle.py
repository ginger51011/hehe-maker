import io

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import markovify

class Autoarticle:
    """Class to create a text from PDF(s) in a directory 
    with path(s) in listings
    """

    def __init__(self, listings):   # Comparable to a constructor in Java, self refers to the object
        self.listings = listings
        self.text = ""

    def convert_pdf_to_txt(self):
        """Directly from stackoverflow, some edits.
        Converts PDF(s) to text
        """
        rsrcmgr = PDFResourceManager()
        retstr = io.StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()

        for path in self.listings:
            try:
                fp = open(path, 'rb')
                for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                                      password=password,
                                      caching=caching,
                                      check_extractable=True):
                    interpreter.process_page(page)

                text = retstr.getvalue()

                fp.close()
                device.close()
                retstr.close()
                self.text = self.text + text
            except:
                print("Error encountered when trying to parse PDF as text, skipping " + path + "...")
    
    def create_article(self, length=40):
        """Creates a new article using Markov chains (via markovify) and returns a string
        of the new article with length amount of sentances (defaults to 40)
        """
        article = ""
        text_model = markovify.Text(self.text)
        
        for i in range(0, length):
            try:
                article = article + " " + text_model.make_sentence()
            except:
                pass

        return article
        

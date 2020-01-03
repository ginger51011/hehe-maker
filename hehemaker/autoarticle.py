import io

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import markovify

class Autoarticle:
    """Class to generate a text from PDF(s) and .txt-documents in a directory 
    with path(s) in listings based on Markov chains
    """

    def __init__(self, listings):   # Comparable to a constructor in Java, self refers to the object
        self.listings = listings
        self.text = ""

    def extract_text_from_txt(self):
        """Extracts text from an .txt document, if one
        is found in directory
        """
        for path in self.listings:
            try:
                if path.endswith(".txt"):   # Checks if this is a .txt document
                    text_document = open(path, "r", encoding="utf-8")
                    self.text = self.text + " " + text_document.read()
                    text_document.close()
            except:
                print("Error encountered when trying to parse .txt as text, skipping " + path + "...")

    def convert_pdf_to_txt(self):
        """Directly from stackoverflow, some edits.
        Converts PDF(s) to text if found
        """
        rsrcmgr = PDFResourceManager()
        retstr = io.StringIO()
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()

        for path in self.listings:
            try:
                if path.endswith(".pdf"):      # Cheks if this is a pdf file
                    fp = open(path, 'rb')
                    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                                        password=password,
                                        caching=caching,
                                        check_extractable=True):
                        interpreter.process_page(page)

                    text = retstr.getvalue()

                    fp.close()
                    self.text = self.text + " " + text
            except:
                print("Error encountered when trying to parse PDF as text, skipping " + path + "...")
    
        device.close()
        retstr.close()
    
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
        

from pdfrw import PdfReader, PdfWriter, PageMerge
import os

# Följande metod är från pdfrw
def fixpage(*pages):
    result = PageMerge() + (x for x in pages if x is not None)
    result[-1].x += result[0].w
    return result.render()

# Beräknar antalet sidor vi har att göra med; Är det ett tal som ej är delbart med 4 kastat exception
page_listings = os.listdir("../pages/") # Ger en lista med innehållet i pages
nbr_of_pages = len(page_listings)
if (nbr_of_pages % 4 != 0): # Om vi ej har mod 4 == 0 kan vi ej trycka på uppslag
    raise ValueError("Antalet sidor ger ej mod 4 == 0; Då kan man ej trycka på uppslag.")

# Får ut PdfReader:s för alla sidor
pdf_readers = []
for listing in page_listings:
    pdf_readers.append(PdfReader(listing))

# Skapar lista för alla sidor
pages_in = []
for reader in pdf_readers:
    pages_in.append(reader.getPage(0))

def create_print_version(pages_in):
    pages_in = pages_in.copy()
    pages_out = []

    # Vi sätter ihop sista och första elementet till en stor sida
    while len(pages_in) > 2:
        pages_out.append(fixpage(pages_in.pop(), pages_in.pop(0)))
        pages_out.append(fixpage(pages_in.pop(0), pages_in.pop()))

    PdfWriter("../papers/web").addpages(pages_out).write()

def create_web_version(pages_in):
    pages_in = pages_in.copy()
    pages_out = []

    # Vi sätter elementen en efter den andra
    while len(pages_in) > 0:
        pages_out.append(pages_in.pop(0))

    PdfWriter("../papers/print").addpages(pages_out).write()
    
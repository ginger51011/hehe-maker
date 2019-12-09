#!/usr/bin/env python
from pdfrw import PdfReader, PdfWriter, PageMerge
import os
import argparse

# Parser så att vi kan styra allt utifrån command line (smaht)
parser = argparse.ArgumentParser()
parser.add_argument("input", help="Path to pages") # Lägger till parameter till parsern
parser.add_argument("output", help="Path to where you want the papers saved")
args = parser.parse_args() # Samlar våra argument i args


# Beräknar antalet sidor vi har att göra med; Är det ett tal som ej är delbart med 4 kastat exception
page_listings = os.listdir(args.input) # Ger en lista med innehållet i pages
nbr_of_pages = len(page_listings)
if (nbr_of_pages % 4 != 0): # Om vi ej har mod 4 == 0 kan vi ej trycka på uppslag
    raise ValueError("Antalet sidor ger ej mod 4 == 0; Då kan man ej trycka på uppslag.")

# Får ut PdfReader:s för alla sidor
pdf_readers = []
for listing in page_listings:
    pdf_readers.append(PdfReader(args.input + "\\" + listing)) # args.input är här alltså C:\<blablabla>\sidorna eller motsvarande

# Skapar lista för alla sidor
pages_in = []
for reader in pdf_readers:
    pages_in.append(reader.getPage(0))

def create_print_version(pages_in):
    pages_in = pages_in.copy()
    pages_out = []

    # Vi sätter ihop sista och första elementet till en stor sida och sedan första och sista till andra
    while len(pages_in) > 2:
        pages_out.append(fixpage(pages_in.pop(), pages_in.pop(0)))
        pages_out.append(fixpage(pages_in.pop(0), pages_in.pop()))

    PdfWriter(args.output + "\\" + "print.pdf").addpages(pages_out).write()

def create_web_version(pages_in):
    pages_in = pages_in.copy()
    pages_out = []

    # Vi sätter elementen en efter den andra
    while len(pages_in) > 0:
        pages_out.append(pages_in.pop(0))

    PdfWriter(args.output + "\\" + "web.pdf").addpages(pages_out).write()

# Följande hjälpmetod är från pdfrw. Sätter ihop två sidor till en
def fixpage(*pages):
    result = PageMerge() + (x for x in pages if x is not None)
    result[-1].x += result[0].w
    return result.render()

create_print_version(pages_in)
create_web_version(pages_in)
    

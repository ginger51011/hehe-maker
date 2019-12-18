#!/usr/bin/env python
from pdfrw import PdfReader, PdfWriter, PageMerge
import os
import argparse

# Parser så att vi kan styra allt utifrån command line (smaht)
parser = argparse.ArgumentParser()
parser.add_argument("input", help="Path to pages") # Lägger till parameter till parsern
parser.add_argument("output", help="Path to where you want the papers saved")
parser.add_argument("-f", "--force", action="store_true", help="Suppresses the need for the number of pages to be = 0 (mod 4)") # Om flaggan ges sparas värdet true
parser.add_argument("-s", "--split", action="store_true", help="Will split pages in two, ordering as if this was a print file") # Flagga för att dela på filer istället
args = parser.parse_args() # Samlar våra argument i args


# Beräknar antalet sidor vi har att göra med; Är det ett tal som ej är delbart med 4 kastat exception
page_listings = os.listdir(args.input) # Ger en lista med innehållet i pages
if not (args.force or args.split):
    nbr_of_pages = len(page_listings)
    if (nbr_of_pages % 4 != 0): # Om vi ej har mod 4 == 0 kan vi ej trycka på uppslag
        raise ValueError("Antalet sidor ger ej mod 4 == 0; Då kan man ej trycka på uppslag.")

pages_in = []
if not args.split:
    pdf_readers = []
    # Får ut PdfReader:s för alla sidor
    for listing in page_listings:
        pdf_readers.append(PdfReader(args.input + "\\" + listing)) # args.input är här alltså C:\<blablabla>\sidorna eller motsvarande

    #  Skapar reader för varje sida och sparar i en list

    for reader in pdf_readers:
        pages_in.append(reader.getPage(0))
# Annars behöver vi bara en reader
else:
    pages_in = PdfReader(args.input + "\\" + page_listings[0]).pages

def create_print_version(pages_in):
    pages_in = pages_in.copy()
    pages_out = []

    # Vi sätter ihop sista och första elementet till en stor sida och sedan första och sista till andra
    while len(pages_in) > 2:
        pages_out.append(fixpage(pages_in.pop(), pages_in.pop(0)))
        pages_out.append(fixpage(pages_in.pop(0), pages_in.pop()))

    # Om vi ska ignorera att det ska gå jämnt ut lägger vi till den sista
    if args.force:
        pages_out += pages_in
    
    # Var den ska -> vilka sidor läggs till -> skriv
    PdfWriter(args.output + "\\" + "print.pdf").addpages(pages_out).write()

def create_web_version(pages_in):
    pages_in = pages_in.copy()
    pages_out = []

    # Vi sätter elementen en efter den andra
    while len(pages_in) > 0:
        pages_out.append(pages_in.pop(0))
        
    PdfWriter(args.output + "\\" + "web.pdf").addpages(pages_out).write()

def print_to_web(pages_in):
    pages_in = pages_in.copy()
    pages_out = []

    # Vi går igenom alla sidor och splittar dem
    for page in pages_in:
        # Sidan längre bak får position 0, flyttar till pages_out2
        pages_out.extend(splitpage(page)) # Extend sätter innehållet från en lista på en annan; annars har vi ett litsobjekt i listan

    # 2 håller reda på sista halvan, 1 på första
    pages_out_sorted1 = []
    pages_out_sorted2 = []
    # Flyttar rätt sidorna
    while len(pages_out) > 0:
        pages_out_sorted2.insert(0, pages_out.pop(0)) # Vänstra ska bak
        pages_out_sorted1.append(pages_out.pop(0))
        pages_out_sorted1.append(pages_out.pop(0))
        pages_out_sorted2.insert(0, pages_out.pop(0))

    pages_out_sorted1.extend(pages_out_sorted2)

    PdfWriter(args.output + "\\split.pdf").addpages(pages_out_sorted1).write()

# Följande hjälpmetod är från pdfrw. Sätter ihop två sidor till en
def fixpage(*pages):
    result = PageMerge() + (x for x in pages if x is not None)
    result[-1].x += result[0].w
    return result.render()

# Delar en sida i två
def splitpage(page):
    # Vi definierar halva sidan
    for x in (0, 0.5):
        # Vi returnerar en generator, som i sin tur generar värden senare
        yield PageMerge().add(page, viewrect=(x, 0, 0.5, 1)).render()

if args.split:
    print_to_web(pages_in)
else:
    create_print_version(pages_in)
    create_web_version(pages_in)
    

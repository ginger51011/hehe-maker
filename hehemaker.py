#!/usr/bin/env python
from pdfrw import PdfReader, PdfWriter, PageMerge
import os
import argparse

# Parser so we can control everything from the command line (smaht)
parser = argparse.ArgumentParser()
parser.add_argument("input", help="Path to pages")  # Adds parameter to parser
parser.add_argument("output", help="Path to where you want the papers saved")
parser.add_argument("-f", "--force", action="store_true", help="Suppresses the need for the number of pages to be = 0 (mod 4)")     # If flag is used saves a true value
parser.add_argument("-s", "--split", action="store_true", help="Will split pages in two, ordering as if this was a print file")     # Flag for splitting a print version
args = parser.parse_args()      # Collects our input in args

# Throws an exception if we don't force mod 4 != 0
page_listings = os.listdir(args.input)      # Returns a list with the files in the directory
if not (args.force or args.split):
    nbr_of_pages = len(page_listings)
    if (nbr_of_pages % 4 != 0):     # If we don't have mod 4 == 0 we can't create a paper
        raise ValueError("Number of pages does not give mod 4 == 0; Then you can't create a (nice) paper version")

pages_in = []
if not args.split:
    pdf_readers = []

    # Puts out a PdfReader for each PDF document (page)
    for listing in page_listings:
        pdf_readers.append(PdfReader(args.input + "\\" + listing))      # args.input är här alltså C:\<blablabla>\sidorna eller motsvarande

    # Creates a reader for every page and saves it to a list
    for reader in pdf_readers:
        pages_in.append(reader.getPage(0))

# Otherwise we only need one reader
else:
    pages_in = PdfReader(args.input + "\\" + page_listings[0]).pages

def create_print_version(pages_in):
    """Puts together the pages in pages_in to a signle PDF in
    print-format
    """
    pages_in = pages_in.copy()
    pages_out = []

    # We put the last and first element to one big page and then the first and last to the second
    while len(pages_in) > 2:
        pages_out.append(fixpage(pages_in.pop(), pages_in.pop(0)))
        pages_out.append(fixpage(pages_in.pop(0), pages_in.pop()))

    # If we force we add the leftover pages
    if args.force:
        pages_out += pages_in
    
    # Where it should be -> which pages are added -> write
    PdfWriter(args.output + "\\" + "print.pdf").addpages(pages_out).write()

def create_web_version(pages_in):
    """Puts together the pages in pages_in to a signle PDF in
    web-format
    """
    pages_in = pages_in.copy()
    pages_out = []

    # We put in the pages one after the other
    while len(pages_in) > 0:
        pages_out.append(pages_in.pop(0))
        
    PdfWriter(args.output + "\\" + "web.pdf").addpages(pages_out).write()

def print_to_web(pages_in):
    """Converts the pages in pages_in from print format to web format
    creates PDF
    """
    pages_in = pages_in.copy()
    pages_out = []

    # We go through all pages and split them, adding them to the list
    for page in pages_in:
        pages_out.extend(splitpage(page))

    # 2 keeps track of the latter half, 1 the first half
    pages_out_sorted1 = []
    pages_out_sorted2 = []
    # Moves the pages into the correct order
    while len(pages_out) > 0:
        pages_out_sorted2.insert(0, pages_out.pop(0))   # Left is going back
        pages_out_sorted1.append(pages_out.pop(0))
        pages_out_sorted1.append(pages_out.pop(0))
        pages_out_sorted2.insert(0, pages_out.pop(0))

    pages_out_sorted1.extend(pages_out_sorted2)     # The content of the second list is added to the first

    PdfWriter(args.output + "\\split.pdf").addpages(pages_out_sorted1).write()

# Taken from example project in pdfrw. Puts two pages together into one
def fixpage(*pages):
    result = PageMerge() + (x for x in pages if x is not None)
    result[-1].x += result[0].w
    return result.render()

# Splits a page in two
def splitpage(page):
    # We define half the page
    for x in (0, 0.5):
        # We return (yield) a generator, which in turn generates a collection later
        yield PageMerge().add(page, viewrect=(x, 0, 0.5, 1)).render()

# Runs our program
if args.split:
    print_to_web(pages_in)
else:
    create_print_version(pages_in)
    create_web_version(pages_in)
    

#!/usr/bin/env python
from pdfrw import PdfReader, PdfWriter, PageMerge
import os
import argparse

# Parser so we can control everything from the command line (smaht)
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--force", action="store_true", help="Suppresses the need for the number of pages to be = 0 (mod 4)")     # If flag is used saves a true value
parser.add_argument("-s", "--split", action="store_true", help="Will split pages in two, ordering as if this was a print file")     # Flag for splitting a print version
parser.add_argument("-ins", "--insert", help="Inserts the pages given at the target page, pushes the page of that number forward")      # Flag to insert page
parser.add_argument("-i", "--index", help="Page number at which pages should be inserted")     # Where to insert pages
parser.add_argument("-rm", "--remove", action="store_const", const=int, default=[], help="Removes the pages given from the PDF specified")      # Flag to remove pages
parser.add_argument("rm_pages", nargs="*", metavar="R", type=int, help="A page to be removed")      # Pages to be removed as specified by user, nargs="*" used to set as optional and a list
parser.add_argument("input", help="Path to pages")      # Adds parameter to parser
parser.add_argument("output", help="Path to where you want the papers saved")
args = parser.parse_args()      # Collects our input in args

page_listings = os.listdir(args.input)      # Returns a list with the files in the directory

# Checking for errors with input

# Throws an exception if we don't force mod 4 != 0
if not (args.force or args.split or args.remove or args.input):
    nbr_of_pages = len(page_listings)
    if (nbr_of_pages % 4 != 0):     # If we don't have mod 4 == 0 we can't create a paper
        raise ValueError("Number of pages does not give mod 4 == 0; Then you can't create a (nice) paper version")

# Throws exception if we want to insert a page but have not specified an index
if (args.insert and not args.index) or (not args.insert and args.index):
    raise EnvironmentError("You must specify both path to pages to be inserted and index of where they should be inserted; Use both -ins and -i")

# End of errorchecking

# Help method to create a list of pages in the directory with path path. 
# Goes through each PDF file in directory and adds every page to the list.
def create_page_list(path):
    pages = []
    page_listings = os.listdir(path)
    pdf_readers = []

    # Puts out a PdfReader for each PDF document
    for listing in page_listings:
        pdf_readers.append(PdfReader(path + "\\" + listing))

    # Goes through the document for each reader and adds all pages for that reader
    for reader in pdf_readers:
        n = 0
        while True:
            pages.append(reader.getPage(n))
            try:
                reader.getPage(n + 1)   # Real shit programming to check if there is a next page
                n = n + 1
            except:
                break
    return pages

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

# Removes pages specified
def remove_pages(pages_in, page_numbers):
    pages_out = pages_in.copy()
    for n in page_numbers:
        del pages_out[n - 1]     # Our list index start at 0, but the user starts counting pages at 1
    PdfWriter(args.output + "\\removed.pdf").addpages(pages_out).write()

# Inserts pages at specified index
def insert_pages(pages_in, pages_to_be_inserted, index):
    true_index = index - 1      # Users uses page numbering, we use array index
    pages_out = pages_in.copy()
    pages_to_be_inserted.reverse()      # We are going to insert them in reverse order

    while len(pages_to_be_inserted) > 0:
        pages_out.insert(true_index, pages_to_be_inserted.pop(0))
    PdfWriter(args.output + "\\inserted.pdf").addpages(pages_out).write()

pages_in = create_page_list(args.input)     # Creates list of all pages that we take as input
    
# Runs our program
if args.split:
    print_to_web(pages_in)
elif args.remove:
    remove_pages(pages_in, args.rm_pages)
elif args.insert:
    pages_to_be_inserted = create_page_list(args.insert)
    insert_pages(pages_in, pages_to_be_inserted, args.ins_index)
else:
    create_print_version(pages_in)
    create_web_version(pages_in)

print("PDF created successfully! Grattis!")
    

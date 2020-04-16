#!/usr/bin/env python
from pdfrw import PdfReader, PdfWriter, PageMerge
import os
import argparse
# The class in our autoarticle.py file
from hehemaker.autoarticle import Autoarticle

# Parser so we can control everything from the command line (smaht)
parser = argparse.ArgumentParser()
# If flag is used saves a true value
parser.add_argument("-f", "--force", action="store_true",
                    help="Suppresses the need for the number of pages to be == 0 (mod 4)")
# Flag for splitting a print version
parser.add_argument("-s", "--split", action="store_true",
                    help="Will split pages in two, ordering as if this was a print file")
parser.add_argument("-ins", "--insert", type=str,
                    help="Inserts the pages given at the target directory/file into the input-paper, pushes the page of that number forward")      # Flag to insert page
# Where to insert pages
parser.add_argument("-x", "--index", type=int,
                    help="Page number at which pages should be inserted")
parser.add_argument("-rm", "--remove", nargs="+", type=int,
                    help="Removes the pages given from the PDF specified")      # Flag to remove pages
parser.add_argument("-g", "--get", nargs="+", type=int,
                    help="Outputs the pages given from the PDF specified")      # Flag to get pages
# Our input and output is the current directory by default
parser.add_argument("-i", "--input", default="./", type=str,
                    help="Path to pages, defaults to current directory. Can be a direct path to a file")
parser.add_argument("-o", "--output", default="./", type=str,
                    help="Path to where you want the papers saved, defaults to current directory. Can be a direct path to a file")
parser.add_argument("-aa", "--autoarticle", nargs="?", type=int, const="40",
                    help="Creates a new article in .txt format at the output based on the PDF(s) and .txt-documents in the input of this length (sentances). Defaults to 40. Will save extracted text from PDF(s) as a .txt file in output directory")    # Const är vad det får om man ej anger det

args = parser.parse_args()      # Collects our input in args

# Defining functions


def pagecount_is_legal(pages_in: list) -> bool:
    """Throws an ValueError exception if we don't force mod 4 != 0
    of the pages, or we use another flag that ignores this.

    Returns
    ------
    bool
        If the number of pages are legal,
        considering the flags being used
    """
    if not (args.force or args.split or args.insert or args.index or args.remove or args.get or args.autoarticle):   # Kontrollerar att vi inte försöker förbigå saker
        nbr_of_pages = len(pages_in)
        if (nbr_of_pages % 4 != 0):     # If we don't have mod 4 == 0 we can't create a paper
            raise ValueError(
                "Number of pages does not give mod 4 == 0; Then you can't create a (nice) paper version. Use -f to force past this.")


def create_page_list(path: str) -> list:
    """Returns a list of pages in the directory with path path. 
    Goes through each PDF file in the directory and adds every page of every file to the list.

    Parameters
    ----------
    path : str
        Path to file or directory of PDFs to be
        extracted as pages

    Returns
    -------
    list
        A list of Page objects
    """
    pages = []
    pdf_readers = []
    page_listings = []

    try:
        is_directory = os.path.isdir(path)
    except:
        exit(path + " could not be resolved as a file or directory. Exiting...")

    if is_directory:
        page_listings = os.listdir(path)
    elif not is_directory:
        page_listings.append(path)

    # We don't want to iterate over a string, creates a PdfReader for each PDF document
    for listing in list(page_listings):
        try:
            # We skip this listing if it's not an PDF
            if not listing.endswith(".pdf"):
                print("Skipping \"" + listing + "\", not a PDF...")
                continue    # We continue the loop without creating PdfReader
            if is_directory:
                pdf_readers.append(PdfReader(path + "/" + listing))
            else:
                pdf_readers.append(PdfReader(path))
        except Exception as e:  # Wow much error handeling...
            # Shitty error handling if we don't have a PDF
            print("Error: \"" + str(e) +
                  "\" encountered, skipping \"" + listing + "\"...")
            continue
            # Goes through the document for each reader and adds all pages from that reader
    for reader in list(pdf_readers):
        n = 0
        while True:
            pages.append(reader.getPage(n))
            try:
                # Real shit programming to check if there is a next page
                reader.getPage(n + 1)
                n = n + 1
            except:
                break
    return pages


def create_print_version(pages_in):
    """Puts together the pages in pages_in to a single PDF in
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

    write_pdf(pages_out, "print.pdf")

# Sök Diod


def create_web_version(pages_in):
    """Puts together the pages in pages_in to a single PDF in
    web-format
    """
    pages_in = pages_in.copy()
    pages_out = []

    # We put in the pages one after the other
    while len(pages_in) > 0:
        pages_out.append(pages_in.pop(0))

    write_pdf(pages_out, "web.pdf")


def print_to_web(pages_in):
    """Converts the pages in pages_in from print format to web format and
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

    # The content of the second list is added to the first
    pages_out_sorted1.extend(pages_out_sorted2)
    write_pdf(pages_out_sorted1, "split.pdf")


def fixpage(*pages):
    """ Taken from example project in pdfrw.
    Puts two pages together into one
    """
    result = PageMerge() + (x for x in pages if x is not None)
    result[-1].x += result[0].w
    return result.render()


def splitpage(page):
    """Splits a page in two
    """
    # We define half the page
    for x in (0, 0.5):
        # We return (yield) a generator, which in turn generates a collection later
        yield PageMerge().add(page, viewrect=(x, 0, 0.5, 1)).render()


def remove_pages(pages_in: list, page_numbers: list):
    """ Removes the pages with page_numbers from pages_in
    and creates PDF with result
    """
    pages_out = pages_in.copy()
    i = 0      # We need to keep track of how many pages we have removed
    page_numbers.sort()     # We need these numbers to be in order
    for n in page_numbers:
        # Our list index start at 0, but the user starts counting pages at 1. We also want to account for already removed pages
        index = n - (1 + i)
        if index > len(pages_out):      # We can no longer remove pages
            print("Pages >" + str(n) + " could not be removed, skipping...")
            break
        else:
            del pages_out[index]
            i -= -1
    write_pdf(pages_out, "removed.pdf")


def insert_pages(pages_in: list, pages_to_be_inserted: list, index: int):
    """ Inserts pages at specified index
    """
    true_index = index - 1      # Users uses page numbering, we use array index
    pages_out = pages_in.copy()
    pages_to_be_inserted.reverse()      # We are going to insert them in reverse order

    while len(pages_to_be_inserted) > 0:
        pages_out.insert(true_index, pages_to_be_inserted.pop(0))
    write_pdf(pages_out, "inserted.pdf")


def get_pages(pages_in: list, page_numbers: list):
    """ Creates a separate PDF file for each
    page as listed in page_numbers
    """
    if not os.path.isdir(args.output):
        exit("When using --get, output must be a directory. Exiting...")

    for nbr in page_numbers:
        nbr = nbr - 1       # pages_in starts indexing at 0, user at 1
        if (nbr < 0) or (nbr > len(pages_in) - 1):
            print(str(nbr + 1) + " is not a page, ignoring...")
            continue
        elif nbr + 1 < 10:      # We want a zero before page number
            PdfWriter(args.output + "/get_page_0" + str(nbr + 1) +
                      ".pdf").addpage(pages_in[nbr]).write()
        else:
            PdfWriter(args.output + "/get_page_" + str(nbr + 1) +
                      ".pdf").addpage(pages_in[nbr]).write()


def create_article(path: str, length: int):
    """ Creates a new article using Markov chains based on the PDF(s) and .txt(s)
    at path, and with length number of sentances

    Parameters
    ----------
    path : str
        Path to file or directory to be basis for new article
    length : int
        Number of sentances of the generated article
    """
    if not os.path.isdir(args.output):
        raise NotADirectoryError(
            "When using --autoarticle, --output must be a directory")

    paths = []

    if os.path.isdir(path):     # If we have a directory
        pdf_listings = os.listdir(path)    # A listing is a single PDF file

        for listing in pdf_listings:    # We need the full path to the PDF(s)
            file_path = path + "/" + listing
            paths.append(file_path)

        if len(paths) == 0:
            print("Cannot create article from empty directory")
            return
    elif os.path.isfile(path):
        paths = path

    aa = Autoarticle(paths)     # Creates a new Autoarticle object

    print("Converting PDF(s) to text (this can take a while)...")
    aa.convert_pdf_to_txt()
    text_from_pdf = aa.text     # We don't want to extract the text and then write it again

    print("Adding .txt files to model...")
    aa.extract_text_from_txt()

    if text_from_pdf:   # We don't create a new file if we haven't extracted any text
        print("Saving extracted text as .txt...")
        # Making sure we don't overwrite an old file
        path_to_extraction = args.output + "/extracted_text.txt"
        number = 1
        while os.path.exists(path_to_extraction):
            path_to_extraction = args.output + \
                "/extracted_text" + str(number) + ".txt"
            number = number + 1
        # Without the encoding this thing goes haywire. Also: Fulhack extraction thing :)
        text_document = open(path_to_extraction, "w+", encoding="utf-8")
        text_document.write(text_from_pdf)
        text_document.close()

    print("Creating new article...")
    try:
        new_article_text = aa.create_article(
            int(length))   # length should be parsed as int
    except ValueError as e:     # For example, we have no text
        exit("Error encountered: " + str(e) + "\n Exiting...")

    # Creates the txt file with the new article
    new_article_file = open(
        args.output + "/autoarticle.txt", "w+", encoding="utf-8")
    new_article_file.write(new_article_text)
    new_article_file.close()

    del aa  # Remove the damn object


def write_pdf(pages: list, default_name: str):
    """Writes pdf from pages, either to default name or to a specific path if one is defined
    in args.output

    Parameters
    ----------
    pages : list
        A list of Page objects
    default_name : str
        What the default name for this type of PDF should be,
        if args.output is not given
    """
    if os.path.isdir(args.output):
        # Where it should be -> which pages are added -> write
        PdfWriter(args.output + "/" + default_name).addpages(pages).write()
    else:
        if not args.output.endswith(".pdf"):    # File must be a PDF
            args.output = args.output + ".pdf"
        PdfWriter(args.output).addpages(pages).write()

# End of defining functions


# The code below is used to make sure installing via pip works
def main():
    # Throws exception if we want to insert a page but have not specified an index
    if (args.insert and not args.index) or (not args.insert and args.index):
        e = EnvironmentError(
            "You must specify both path to pages to be inserted and index of where they should be inserted; Use both -ins and -x")
        exit("Error encountered: " + str(e) + "\n Exiting...")

    pages_in = []
    if not args.autoarticle:
        # Creates list of all pages that we take as input
        pages_in = create_page_list(args.input)

    try:
        # Checks to see if we have a legal number of pages, or force past it
        pagecount_is_legal(pages_in)
    except ValueError as e:
        exit("Error encountered: " + str(e) + "\n Exiting...")

    if args.split:
        print_to_web(pages_in)
    elif args.remove:
        remove_pages(pages_in, args.remove)
    elif args.insert:
        pages_to_be_inserted = create_page_list(args.insert)
        insert_pages(pages_in, pages_to_be_inserted, args.index)
    elif args.get:
        get_pages(pages_in, args.get)
    elif args.autoarticle:
        try:
            create_article(args.input, args.autoarticle)
        except NotADirectoryError as e:
            exit("Error encountered: " + str(e) + "\n Exiting...")
    else:
        if not os.path.isdir(args.output):
            exit(
                "When using HeHE-maker in normal mode, --output must be a directory. Exiting...")
        create_print_version(pages_in)
        create_web_version(pages_in)

    if not args.autoarticle:
        print("PDF created successfully! Grattis!")
    else:
        print("Automatic article created successfully! Grattis!")


# If this code is run on its' own and is not imported, run the following (main())
if __name__ == "__main__":
    main()

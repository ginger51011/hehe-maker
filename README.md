# HeHE-maker
*For comprehensive guide in Swedish, as created for Redaktionen at E-sektionen, see `README.swe.md`*

**HeHE-maker** is a simple command line-tool to create a paper to be published in printed and/or web form. Simply create the pages you want, order them in an otherwise empty directory/folder (simply naming them 01.pdf, 02.pdf, 03.pdf etc. is enough) and let the script create printable versions, as well as web versions, for you! If more than one page happens to be in the same PDF-file, for example if an article has two pages in the same file, HeHE-maker will take care of this for you.

## Requirements
Requires Python 3.x and the `pdfrw` package to run. Simply install Python from [here](https://www.python.org/downloads/), run `python -v` to make sure everything was installed properly. If you don't let the installer create a PATH-variable, add `python` before anything else in your commands.

To install `pdfrw`, run `pip install pdfrw`.

## Running the program
After installing the requirements above, and cloning this repo, open the terminal and navigate to the folder with `hehemaker.py`. Simply use `hehemaker.py "<path to input>" "<path to output>"` and the script will create print.pdf and web.pdf at the specified path.

Note: You might have the write `python` before `hehemaker.py` on some systems.

### Further functions and flags
HeHE-maker can do much more to facilitate the publishing of a paper by using flags to set functions. These are written before the input and output paths. They are as follows:

* This list not helpful enough? Use `-h` or `--help`!
* To suppress the requirement for the number of pages to fit nicely on the print format, use `-f` or `--force`. (This is only necessary when running in normal mode, i.e. not using other flags)
* To convert from a printed version to a web version, use `-s` or `--split`.
* To remove one or more pages use `-rm` or `--remove` followed by the page number(s) to be removed. Example: To remove the first and last page of a 12 page file, use `hehemaker.py -rm 1 12 "<path to input>" "<path to output>"`
* To insert pages into an existing file, use `-ins` or `--insert` followed by the path to the pages to be inserted, and `-i` (or `--index`) followed by where the pages should be inserted. Example: An article saved in "C:\\Users\\Hacke\\..\\article" is to be inserted at page 3. Use `hehemaker.py -ins "C:\\Users\\Hacke\\..\\article" -i 3 "<path to input>" "<path to output>"`

### Further Examples
Little Timmy has an old printed version of a paper as a PDF file, `old.pdf`, but he wants to censor the article on pages 4-5 and replace it with a two-page ad. He saves `old.pdf` in a new empty folder/directory at the path `C:\Users\Timmy\old\`. He has his ad in an otherwise empty folder at path `C:\Users\Timmy\ad\`. 

He starts by creating a directory `C:\Users\Timmy\new\` and creates a web version by running `hehemaker.py -s "C:\\Users\\Timmy\\old" "C:\\Users\\Timmy\\new"`.

He deletes `old.pdf` and replaces it with `web.pdf`created in the `\new\`-directory and then runs `hehemaker.py -rm 4 5 "C:\\Users\\Timmy\\old" "C:\\Users\\Timmy\\new"`.

He deletes `web.pdf` and replaces it with `removed.pdf`created in the `\new\`-directory. He then inserts his ad by running `hehemaker.py -ins "C:\\Users\\Timmy\\ad" -i 4 "C:\\Users\\Timmy\\old" "C:\\Users\\Timmy\\new"`. 

He now wants the whole paper in a printable format on his desktop, so he finally runs `hehemaker.py "C:\\Users\\Timmy\\new" "C:\\Users\\Timmy\\Desktop"`.

## Why
Doing all this with large documents (12+ pages) becomes very tiresome.

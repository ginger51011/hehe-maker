# HeHE-maker

*For an (outdated) guide in Swedish, as created for Redaktionen at E-sektionen, see `README.swe.md`*

**HeHE-maker is now capable of writing its' own articles! Check out the -aa flag for more information**

**HeHE-maker** is a simple command line-tool to create a paper to be published in printed and/or web form. Simply create the pages you want, order them in an otherwise empty directory/folder (simply naming them 01.pdf, 02.pdf, 03.pdf etc. is enough) and let the script create printable versions, as well as web versions, for you! If more than one page happens to be in the same PDF-file, for example if an article has two pages in the same file, HeHE-maker will take care of this for you.

## Quickstart

This program is part if the Python Package Index (PyPi) and can easily be installed and run using `pip`. Start by installing Python 3.x from [here](https://www.python.org/downloads/), and run `python -v` (or, in some cases, `python3 -v`) in your console and make sure everything looks reasonable. Then run the following commands:

* `pip install hehe-maker`

**Alternatively**

* `pip3 install hehe-maker`

Done! You can now use HeHE-maker by typing `hehemaker` followed by arguments (according to "Running the program" below)!

To check for updates, run `pip install --upgrade hehe-maker`

## Running the program

**Update: Since version 1.3.13, HeHE-maker now supports direct paths; All functions can now be called on filepaths**

Simply use `hehemaker -i <path to input> -o <path to output>` (without `<>`) and the script will create print.pdf and web.pdf at the specified path. The path can either be full, like `C:\\User\\...\\example` or relative, or be omitted for HeHE-maker to default to the current directory. Omitting `-i`and/or `-o` will make them default to the current directory.

If you are on Windows and this fails, check to see if Python and Python/Scripts are in your PATH-variables (Swe: *Miljövariabler*). Some Linux requires that pip installs to a directory in the PATH variable.

## Further functions and flags

HeHE-maker can do much more to facilitate the publishing of a paper by using flags to set functions. They are as follows:

* This list not helpful enough? Use `-h` or `--help`!
* To specify input and output path, use `-i` and `-o` (or `--input` and `--output` respectively). For example, running `hehemaker -o "C:\\Users\\<some user>\\Desktop"` (note that quotes are optional) will assemble the pages in the current directory and output them to the desktop. These can be direct file paths, such as `~/somedir/example.pdf`, but this will not work when using the `--autoarticle` or `--get` options or when using in normal mode (i.e. to create web and print-versions).
* To suppress the requirement for the number of pages to fit nicely on the print format, use `-f` or `--force`. (This is only necessary when running in normal mode, i.e. not using other flags)
* To get only specific pages of PDF(s) in a directory, use `-g` or `--get` and specify which pages you want.
* To convert from a printed version to a web version, use `-s` or `--split`.
* To remove one or more pages use `-rm` or `--remove` followed by the page number(s) to be removed. Example: To remove the first and last page of a 12 page file, use `hehemaker -rm 1 12 -i <path to input> -o <path to output>`
* To insert pages into an existing file, use `-ins` or `--insert` followed by the path to the pages to be inserted, and `-x` (or `--index`) followed by where the pages should be inserted. Example: An article saved in "C:\\Users\\Hacke\\..\\article" is to be inserted at page 3. Use `hehemaker -ins C:\\Users\\Hacke\\..\\article -x 3 -i <path to input>" -o <path to output>`
* HeHE-maker can generate .txt files of new articles using Markov chains. Simply use `-aa` or `--autoarticle` (and specify the number of sentances wanted, defaults to 40) and HeHE-maker will use the PDF files at the input directory to create a new article using computer magic and save it at the output directory. Note that this works best with a lot of samples! This can take a while (but still faster than writing the thing yourself! If I were you I would also go through the text and remove unforseen syntax errors (I am just a man and this script is just a burning pile of garbage). HeHE-maker can also extract files in the `.txt` format, and will create a `.txt`-file when done extracting from PDF(s). This way, `-aa` can be used on this text file instead in the future, speeding up the process!

### Further Examples

#### Using relative paths (Recommended)

HeHE-maker is capable of using relative paths to find the directory/folder of your input/output. As default (i.e. no input and/or output is passed), HeHE-maker will set the current directory/folder as both input and/or output. For example, if all pages to a paper is saved in a folder at `~/Documents/HeHE`. If we position ourselves in that directory and run `hehemaker`, we will create `print.pdf` and `web.pdf` in that `~/Documents/HeHE`.

#### Little Casper

Little Casper is in charge of creating an informational pamphlet for a major event which may or may not be cancelled by a minor apocalypse. His minions are creating PDF pages with pretty designs in landscape mode, and now Little Casper wants to put these together in a printable format.

He starts by updating to the latest stable release of `hehe-maker` by running `pip3 install --upgrade hehe-maker`. He runs `hehemaker -h` to get helpful information.

He saves all pages in `~/somedir`. He first needs to split the landscape (A3) pages, as he wants to sort them. He runs `hehemaker -s -i ~/somedir/<somename>.pdf -o ~/somedir/<someothername>` to split each A3-page into two and save them in `~/somedir` with the name `<someothername>.pdf`. Since Little Casper is very smart and has a very good brain, he names them in a smart way. For example, the landscape page containing page 1 and 2 of the pamphlet is named `01.pdf`.

At some point, the pages being split might not be directly after eachother, for example the front page and the last page might be in the same file `~/somedir/frontandlast.pdf` despite being page 1 and 12. No problem! By running `hehemaker -g 1 -o ~/somedir/frontpage.pdf` Little Casper can save the frontpage as a pdf of its' own, and do the same thing to the last page.

After having done this, Little Casper moves all pages now neatly sorted to their own directory `~/pamphlet/`. All pages are listed in order in the directory, which he does by naming them by the first page in each pdf-file (i.e. `01.pdf`, `02.pdf`, ..., `XX.pdf`). By running `hehemaker -i ~/pamphlet -o ~/Documents`, he can now find a finished pamphlet in both web and printable format in his Documents-folder as `web.pdf` and `print.pdf`.

#### Little Timmy

**Little Timmy is a bit off his meds, and has not read the changelog. He can now use direct paths, for example `~./somedir/target.pdf` instead of making folders directly. This can have unforseen (or just boring) consequences together with making a paper, there you should continue to use directories**

Little Timmy has an old printed version of a paper as a PDF file, `old.pdf`, but he wants to censor the article on pages 4-5 and replace it with a two-page ad. He saves `old.pdf` in an otherwise empty directory `~./somedir/` and saves his ad in the (otherwise empty) directory `~./ad/`.

Timmy starts by creating a web version by switching directory to `~./somedir/` and running `hehemaker -s`. He then removes `old.pdf`; `~./somedir/` now only contains `split.pdf`.

He now deletes the unwanted article, in accordance with his local Supreme Leader's wishes, by running `hehemaker -rm 4 5`. He then deletes all evidence by removing the old `split.pdf`.

He now inserts the ad (probably for his beloved Supreme Leader) by running `hehemaker -ins ~./ad/ -x 4`, and deletes the old `removed.pdf`.

Little Timmy now wants the whole paper in a printable format on his desktop, so he finally runs `hehemaker -o C:\\Users\\TimmysMom\\Desktop`.

Good job Timmy!

## Why

Doing all this with large documents (12+ pages) becomes very tiresome.

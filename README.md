pandocket
=========

A python script that looks for special lines in a markdown file and uses those lines to convert, clean up, and insert content from URLs into the file for processing by pandoc

# Usage

Pandocket is basically a python wrapper for pandoc mashed together with BeautifulSoup. It looks through a markdown "input" file (currently hardcoded in the script) until it sees a stand-alone that begins with "http". It then uses information in that line to go to the URL, grab the content, and parse it using BeautifulSoup.

The trigger lines should look like this:

	http://www.example.com | div > class=content

Pandocket knows that everything to the left of this bar is the URL. Everything to the right of the bar will be information about the tag that wraps the specific content from the page that you want. The name on the left of `>` is the tag name, and the text on the right is one of that tag's attributes.

After "expanding" these trigger lines with the content from the specified URLs, pandocket creates three "output" files---a markdown (*.md) file, a PDF file, and an EPUB file---using pandoc.

The markdown file is produced so that the user can clean up any problems in the content grabbed from the web. The outputted markdown file, once manually cleaned, can either be processed at the command line using pandoc or passed back through pandocket as the new input file.

An example input file called `sources.txt` is included in this repository, together with its markdown output file `pandocket-output.md`.

# Known Issues

- If the HTML content grabbed from the web uses "span" tags to provide formatting like italics, pandoc will lose the formatting. Basically, if the HTML is not well-formed, you're on your own.
- PDF and EPUB output will fail if there are images in the HTML content, because it won't have local copies of the images. Best solution would probably be to delete images using BeautifulSoup.

# Dependencies

- [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)
- [yoavram](https://github.com/yoavram/pyandoc) fork of pyandoc
- [Pandoc](http://johnmacfarlane.et)
- *optional*: LaTeX for PDF output by pandoc

# TODO

A *ton*, beginning with a better README.md.

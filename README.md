pandocket
=========

A python script that looks for special lines in a markdown file and uses those lines to convert, clean up, and insert content from URLs into the file for processing by pandoc

# Basic Usage

Pandocket is a python wrapper for pandoc mashed together with BeautifulSoup. It looks through a markdown "input" file (specified at the command line) until it sees a stand-alone line that begins with "http". It then uses information in that line to go to the URL, grab the content, and parse it using BeautifulSoup.

The trigger lines should look like this:

	http://www.example.com | div > class=content

Pandocket knows that everything to the left of the first bar is the URL that you want to grab content from. To the right of the first bar you should place information about the tag that wraps the specific content from the page that you want. The name on the left of `>` is the tag name, and the text on the right is one of that tag's attributes. (If the content you want isn't contained within a tag that has attributes, you can also just put a tag name. For instance, you can be greedy about grabbing content by simply putting `body` in this space.)

After "expanding" these trigger lines with the content from the specified URLs, pandocket creates three "output" files by default---a markdown (*.md) file, a PDF file, and an EPUB file---using pandoc.

The markdown file is produced so that the user can clean up any problems in the content grabbed from the web. The outputted markdown file, once manually cleaned, can either be processed at the command line using pandoc or passed back through pandocket as the new input file.

An example input file called `sources.txt` is included in this repository, together with its markdown output file `pandocket-output.md`.

To run the program, give the source file first and then the desired basename for output files, followed by any options.

E.g.:

	pandocket.py sources.txt lincoln-docs --noimages --toc

# Options

## `-h`, `--help`

See a list of the main pyandocket options and positional arguments.

## `--mdonly`

The `--mdonly` option will suppress the EPUB and PDF output. Use this if you are using the main `pyandoc` project instead of the yoavram fork.

## `--noimages`

The `--noimages` option will strip all `<img>` tags from the HTML content. This is recommended if you are using PDF and EPUB output, since those outputs will usually fail if the content you are parsing has image links in it.

## Any pandoc options

You can supply any of pandoc's regular options at the command line so long as you use the longer "two-dash" form of the option. (E.g., `--standalone` instead of `-s`.)

## Additional user-defined filtering

Users who are familiar with beautifulsoup can create their own modules that add additional filtering to the HTML content. Create a file with your module that includes a function called `pandocket`. Then, on the trigger line in your source file, add a second bar at the end of the line, followed by your module's name.

For example, to remove the byline from posts on my old blog Mode for Caleb, I might create a file called `modeforcaleb.py` that contains this:

	# modeforcaleb.py
	def pandocket(soup):
		soup.find("div", class_="byline").decompose()
		return soup

Then I could include a trigger line like this in my source file:

	http://modeforcaleb.blogspot.com/2004/12/lives-of-douglass-part-i.html | div > class=blogPost | modeforcaleb

The only important thing here, from pandocket's perspective, is that the function be called `pandocket`.

# Known Issues

- If the HTML content grabbed from the web uses "span" tags to provide formatting like italics, pandoc will lose the formatting. Basically, if the HTML is not well-formed, you're on your own.

# Dependencies

- [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)
- [pyandoc](http://github.com/kennethreitz/pyandoc)
- [Pandoc](http://johnmacfarlane.et)
- *optional*: [yoavram](http://github.com/yoavram/pyandoc) fork of pyandoc for automatic PDF and EPUB output
- *optional*: LaTeX for PDF output by pandoc

# TODO

A *ton*, beginning with a better README.md.

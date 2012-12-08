#! /usr/bin/env python
# -*- coding: utf-8 -*-
# pandoc-webpage.py
# TODO: Preserve span formatting from original webpage
# TODO: Remove img tags with BeautifulSoup
# TODO: Make error handling easier to understand

import argparse
import urllib2
import pandoc
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument('filename', action='store', help='Name of input file to process')
parser.add_argument('outname', action='store', help='Basename for output files')
parser.add_argument('--mdonly', action='store_true', help='Output markdown only, suppress EPUB and PDF output')
parser.add_argument('--noimages', action='store_true', help='Remove image tags from webpage (recommended for PDF and EPUB output)')
sysargs = parser.parse_args()

# Open the input file and empty the output file
input = open(sysargs.filename, "r").read().splitlines()
open(sysargs.outname + ".md","w").close()

for line in input:
 
 	if line.startswith("http"):

		# Get information from line about website to be parsed
		# Help provided by http://stackoverflow.com/questions/13537829/
		# vars = line.split(' | ')
		if line.count('|') == 1:
			url, args = line.split (' | ', 1)
			user = None
		elif line.count('|') == 2:
			url, args, user = line.split (' | ', 2)
		args = args.split(' >')
		tag = args[0]
		params = dict([param.strip().split('=') for param in args[1:]])

		# Open specified URL and use BeautifulSoup to get specified section
		html = urllib2.urlopen(url).read()
	 	soup = BeautifulSoup(html)
 		html_section = soup.find(tag, **params)

		if user is not None:
			user = __import__(user)	
			html_section = user.pandocket(html_section)

		if (sysargs.noimages):
			for image in html_section.find_all(name='img'):
				image.decompose()

		doc = pandoc.Document()
		doc.html = str(html_section)
		html_md = doc.markdown

 		# Write to output file, getting rid of any literal linebreaks
 		f = open(sysargs.outname + ".md","a").write(html_md.replace("\\\n","\n"))

	elif len(line) == 0:

		# Convert blank lines in input file to newlines in output file
		f = open(sysargs.outname + ".md","a").write("\n")

	else:

		# Pass regular lines from input file to output file
		f = open(sysargs.outname + ".md","a").write(line + "\n")

# Call on pandoc to convert markdown to PDF and EPUB
# Using yoavram fork of pyandoc

if not (sysargs.mdonly):
	fulldoc = pandoc.Document()
	fulldoc.add_argument("standalone")
	fulldoc.add_argument("toc")
	fulldoc.markdown = open(sysargs.outname + ".md","r").read()
	fulldoc.to_file(sysargs.outname + '.pdf')
	fulldoc.to_file(sysargs.outname + '.epub')

# Infinity Army Printer

Combination of Python script and LaTeX templates that downloads Infinity Army data and puts it in a ready to compile LaTeX file. Not officially supported by Corvus Belli! Feel free to point out errors

## Usage

Will spit out a bunch of .tex files in a directory of your choice:

    main.py <output Dir>
In addition a **logo** folder will be made in the output directory where downloaded faction and trooper logos will be saved to.
Optional Arguments:

 - -ci : specify a directory to look for json files in instead of downloading from JSON. For offline use or custom data.*
 - -co : specify a directory to store .json files that are downloaded, for future use in -ci*
 - -t : runs pdflatex on output files*
*: Experimental, not tested yet

The LaTeX templates depend on three subdirs in the same directory to compile:
 - icons 
 - logo 
 - sty
	 - InfinityFT.sty
	 - InfinityOptions.sty
	 - InfinityPrinter.sty
 - *factionList.tex*
 Where factionList.tex is where your output TeX files should be

## Dependencies

### Python
You'll need to install these - all should be available in pip
 - pyratemp (template engine)
 - requests (for wgets)
 - resvg_py (for converting svg to png)

### LaTeX (pdflatex)
Besides the usual suspects:
 - tikz 
 - xparse 
 - ifthen 
 - xkeyval
 -  listofitems 
 - pgffor 
 - hyphenat 
 - silence 
 - array
 - etoolbox     
 - tabularray

I am NOT very technical with LaTeX so there are some weird design decisions in the templates and some of these packages may be redundant or not the best choices.

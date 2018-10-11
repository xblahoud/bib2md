# bib2md
bib2md uses tex4ht and pandoc to convert LaTeX files that include bibliography processed by BibLaTeX into Markdown. It allows users that are familiar with BibLaTeX that want use its power to create markdown files with citations and bibliography lists.

The core consists of the bibliography and citation style (`md.bbx, md.cbx`) and the tex4ht configuration file `md.cfg`.
* The citation style `md.cbx` defines a `\mdcite` that does create a citation suitable to used inline and avoids cite-indices (numbers or keys). The citation uses hyperlinks to the paper (file, doi, or url) if available.

* The bibliography style provides drivers for article, book, inproceedings and thesis entries that use simple entry formatting, again with hyperlinks.

* The `md.cfg` configures tex4ht and BibLaTeX to use unordered lists for the `\printbibliography` command and lightweight formatting for `\emph` and `strong`.

## Requirements
* tex4ht package with XeLaTeX and Biber (tested with TeX Live 2017)
* pandoc (tested with `pandoc 1.19.2.4`)

## Usage
The basic scenario is that you have a `.tex` file that uses some `.bib` file. Having the files `md.*` accessible in your system (for example in your working directory), you can use the following commands to convert a file `foo.tex` into a `.md` file with reasonable bibliography formatting.
```
# Process the bibliography with biber
xelatex foo.tex
biber foo
xelatex foo.tex

# Create a foo.html using tex4ht with the bib2md config file
htxelatex foo.tex md.cfg " -cunihtf -utf8"

# convert the html into markdown using pandoc
pandoc -t markdown foo.html | sed 's/\[\]{#page.1}\[\]{#X0-}//' > foo.md
```

## Advanced use
The power of the package can be used to combine the simplicity of Markdown and power of BibLaTeX. You can write most of your text in Markdown and the bibliography-intense parts in LaTeX. You then convert the `.tex` files into `.md` and finally merge all the `.md` files together by `pandoc`. You can take this README as an example. It was created by the [Makefile](Makefile) and that joins `README.header.md` and files from the [example_use](example_use) directory.

The directory contains the file `cite.tex` that uses the `\mdcite` command and the file `full_ref.tex` that lists all publications from `mypub.bib` using the `\printbibliography` command. You can also check the directory for an example `Makefile` to perform the conversion to `md` files.

### Example of `\mdcite` and bibliography listing
(README.header.md ends here)

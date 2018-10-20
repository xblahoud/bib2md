bib2md
======

bib2md uses tex4ht and pandoc to convert LaTeX files that include
bibliography processed by BibLaTeX into Markdown. It allows users that
are familiar with BibLaTeX that want use its power to create markdown
files with citations and bibliography lists.

The core consists of the bibliography and citation style
(`md.bbx, md.cbx`) and the tex4ht configuration file `md.cfg`. \* The
citation style `md.cbx` defines a `\mdcite` that does create a citation
suitable to used inline and avoids cite-indices (numbers or keys). The
citation uses hyperlinks to the paper (file, doi, or url) if available.

-   The bibliography style provides drivers for article, book,
    inproceedings and thesis entries that use simple entry formatting,
    again with hyperlinks.

-   The `md.cfg` configures tex4ht and BibLaTeX to use unordered lists
    for the `\printbibliography` command and lightweight formatting for
    `\emph` and `strong`.

Requirements
------------

-   tex4ht package with XeLaTeX and Biber (tested with TeX Live 2017)
-   pandoc (tested with `pandoc 1.19.2.4`)

Usage
-----

The basic scenario is that you have a `.tex` file that uses some `.bib`
file. Having the files `md.*` accessible in your system (for example in
your working directory), you can use the following commands to convert a
file `foo.tex` into a `.md` file with reasonable bibliography
formatting.

    # Process the bibliography with biber
    xelatex foo.tex
    biber foo
    xelatex foo.tex

    # Create a foo.html using tex4ht with the bib2md config file
    htxelatex foo.tex md.cfg " -cunihtf -utf8"

    # convert the html into markdown using pandoc
    pandoc -t markdown foo.html | sed 's/\[\]{#page.1}\[\]{#X0-}//' > foo.md

Customization
-------------

The citation command `\mdcite` can be easily extended by redefining the
macro `fincite` that allows you to add anything after the citation. The
bibliography entries can be extended in the standard BibLaTeX way -- by
redefining the `finentry` macro.

### The `md-notes-short-conf` style

The style uses the hooks above to add link to file with the user's
notes. It currectly expects the filename to be stored in the
`annotation` field. This is subject to change.

The next feature of this style that it prefers the `eventtitle` to
`booktitle` for the inproceedings entry types. This allows us to specify
the conferences abbreviations in the bibliography.

Advanced use
------------

The power of the package can be used to combine the simplicity of
Markdown and power of BibLaTeX. You can write most of your text in
Markdown and the bibliography-intense parts in LaTeX. You then convert
the `.tex` files into `.md` and finally merge all the `.md` files
together by `pandoc`. You can take this README as an example. It was
created by the [Makefile](Makefile) and that joins `README.header.md`
and files from the [example\_use](example_use) directory.

The directory contains the file `cite.tex` that uses the `\mdcite`
command and the file `full_ref.tex` that lists all publications from
`mypub.bib` using the `\printbibliography` command. You can also check
the directory for an example `Makefile` to perform the conversion to
`md` files.

### Example of `\mdcite` and bibliography listing

(README.header.md ends here)

We can write some text here and then cite some our work like this for
example **Blahoudek et al.** (2017): *[Seminator: A Tool for
Semi-Determinization of
Omega-Automata](https://easychair.org/publications/paper/340360)*. and
we may try cite multiple papers in one command **Babiak et al.** (2013):
*[Eﬀective Translation of LTL to Deterministic Rabin Automata: Beyond
the (F, G)-Fragment](http://dx.doi.org/10.1007/978-3-319-02444-8_4)*;
**Babiak et al.** (2015): *[The Hanoi Omega-Automata
Format](http://dx.doi.org/10.1007/978-3-319-21690-4_31)*.

-   *Tomáš Babiak, František Blahoudek, Alexandre Duret-Lutz, Joachim
    Klein, Jan Křetínský, David Müller, David Parker, and Jan Strejček*
    (2015).\
    **[The Hanoi Omega-Automata
    Format](http://dx.doi.org/10.1007/978-3-319-21690-4_31)**. In
    *Proceedings of the 27th International Conference on Computer Aided
    Veriﬁcation (CAV’15)*. Lecture Notes in Computer Science
    (vol. 9206), part I. Springer, pp. 479–486. DOI:
    [10.1007/978-3-319-21690-4˙31](http://dx.doi.org/10.1007/978-3-319-21690-4_31).
-   *Tomáš Babiak, František Blahoudek, Mojmír Křetínský, and Jan
    Strejček* (2013).\
    **[Eﬀective Translation of LTL to Deterministic Rabin Automata:
    Beyond the (F,
    G)-Fragment](http://dx.doi.org/10.1007/978-3-319-02444-8_4)**. In
    *Proceedings of the 11th International Symposium on Automated
    Technology for Veriﬁcation and Analysis (ATVA’13)*. Lecture Notes in
    Computer Science (vol. 8172). Springer, pp. 24–39. DOI:
    [10.1007/978-3-319-02444-8˙4](http://dx.doi.org/10.1007/978-3-319-02444-8_4).
-   *František Blahoudek, Alexandre Duret-Lutz, Mikuláš Klokočka, Mojmír
    Křetínský, and Jan Strejček* (2017).\
    **[Seminator: A Tool for Semi-Determinization of
    Omega-Automata](https://easychair.org/publications/paper/340360)**.
    In *Proceedings of the 21st International Conference on Logic for
    Programming, Artiﬁcial Intelligence and Reasoning (LPAR-21)*. EPiC
    Series in Computing (vol. 46). EasyChair, pp. 356–367. URL:
    <https://easychair.org/publications/paper/340360>.
-   *František Blahoudek, Alexandre Duret-Lutz, Mojmír Křetínský, and
    Jan Strejček* (2014).\
    **[Is there a Best Büchi Automaton for Explicit Model
    Checking?](http://dx.doi.org/10.1145/2632362.2632377)** In
    *Proceedings of 21st International SPIN Symposium on Model Checking
    of Software (SPIN’14)*. ACM, pp. 68–76. DOI:
    [10.1145/2632362.2632377](http://dx.doi.org/10.1145/2632362.2632377).
-   *František Blahoudek, Alexandre Duret-Lutz, Vojtěch Rujbr, and Jan
    Strejček* (2015).\
    **[On Reﬁnement of Büchi Automata for Explicit Model
    Checking](http://dx.doi.org/10.1007/978-3-319-23404-5_6)**. In
    *Proceedings of 22nd International SPIN Symposium on Model Checking
    of Software (SPIN’15)*. Lecture Notes in Computer Science
    (vol. 9232). Springer, pp. 66–83. DOI:
    [10.1007/978-3-319-23404-5˙6](http://dx.doi.org/10.1007/978-3-319-23404-5_6).
-   *František Blahoudek, Matthias Heizmann, Sven Schewe, Jan Strejček,
    and Ming-Hsien Tsai* (2016).\
    **[Complementing Semi-deterministic Büchi
    Automata](http://dx.doi.org/10.1007/978-3-662-49674-9_49)**. In
    *Proceedings of the 22nd International Conference on Tools and
    Algorithms for the Construction and Analysis of Systems (TACAS’16)*.
    Lecture Notes in Computer Science (vol. 9636). Springer, pp.
    770–787. DOI:
    [10.1007/978-3-662-49674-9˙49](http://dx.doi.org/10.1007/978-3-662-49674-9_49).
-   *František Blahoudek, Mojmír Křetínský, and Jan Strejček* (2013).\
    **[Comparison of LTL to Deterministic Rabin Automata
    Translators](http://dx.doi.org/10.1007/978-3-642-45221-5_12)**. In
    *Proceedings of the 19th International Conference on Logic for
    Programming, Artiﬁcial Intelligence, and Reasoning (LPAR-19)*.
    Lecture Notes in Computer Science (vol. 8312). Springer, pp.
    164–172. DOI:
    [10.1007/978-3-642-45221-5˙12](http://dx.doi.org/10.1007/978-3-642-45221-5_12).


default: all

%.pdf : %.tex *.bib md.*bx
	xelatex $(patsubst %.pdf,%.tex,$@) 
	biber $(patsubst %.pdf,%,$@) 
	xelatex $(patsubst %.pdf,%.tex,$@)

%.html : %.pdf md.cfg
	htxelatex $(patsubst %.html,%.tex,$@) md.cfg " -cunihtf -utf8"

### Removes silly link anchor produced by tex4ht for the firs entry
%.md : %.html
	pandoc -t markdown $< | sed 's/\[\]{#page.1}\[\]{#X0-}//' > $@

clean_mess:
	latexmk -CA
	rm -f *.4* *.bbl *.css *.html *.idv *.lg *.run.xml *.tmp *.xref *.xdv

clean_md:
	rm -f full_ref.md cite.md

clean: clean_md clean_mess

full_ref: full_ref.md
cite: cite.md

all: full_ref cite
	make clean_mess

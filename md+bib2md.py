# coding: utf-8

import subprocess

md_file = 'test_mdcite.md'
f_out = 'bib2md.tex'
bib_style = 'md' # or md-notes-short-conf
print_biblio = True # `\printbibliography` will be added
bibliography = ['mypub.bib'] # list of files with bibliography entries

pandoc_options = [
    '--to=latex',
    '--standalone',
    '--template=template.bib2md',
    '--biblatex',
    '-V','biblatexoptions="backend=biber"',
    '-V','biblio-style={}'.format(bib_style),
    '-o',f_out,
    md_file,
]

pandoc_options.extend(['--bibliography='+b for b in bibliography])

if print_biblio:
    pandoc_options.append('-V print-biblio')

run_args = ['pandoc'] + pandoc_options
subprocess.run(run_args)



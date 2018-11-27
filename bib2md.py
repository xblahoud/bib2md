# coding: utf-8

import subprocess
import argparse
import tempfile as tf
import re
import shutil
import os

def is_local(path):
    '''Decides whether given argument is installed or local.

    Returns a pair (local, last) where local is the boolean
    answer and last is the last part of the path (e.g filename).'''
    local = False
    if path.startswith('.') or path.startswith('/'):
        local = True
    last = path.split('/')[-1]
    return local, last

def md2tex(md_file, bibliography,
           out_file='bib2md.tex',
           print_biblio=True, bib_style='md',
           template='bib2md.latex',
           verbose=False):
    pandoc_options = [
      '--to=latex',
      '--from=markdown',
      '--standalone',
      '--template={}'.format(template),
      '--biblatex',
      '-V','biblatexoptions=backend=biber',
      '-V','biblio-style={}'.format(bib_style),
      '-o',out_file,
      md_file,
    ]

    pandoc_options.extend(['--bibliography='+b for b in bibliography])

    if print_biblio:
        pandoc_options.extend(['-V','print-biblio'])

    if verbose:
        print(' '.join(['pandoc'] + pandoc_options))

    run_args = ['pandoc'] + pandoc_options
    subprocess.run(run_args)

def extract_cite_cmds(infile):
    '''Searches `infile` for TeX cite commands and returns
    set of triples `(full_cmd, cite type, cite key).`
    '''
    content = infile.read()
    # locate each citation record and store them in a set of tuples:
    # (full string, cite command, key)
    p = re.compile(r'(\\([a-z]*cite)\{([^}]+)\})')
    m = p.findall(content)
    return set(m)

def generete_tex(cites, build_dir, bibliography,
                 print_biblio=True, bib_style='md',
                 template='bib2md.latex',verbose=False):
    '''Generate texfiles for conversion to md for each cite.

    For each cite in `cites`, generate the corresponding TeX file
    `build_dir/type.key.tex` that contains the full_cmd of the cite
    using the specified Pandoc `template`.

    Parameters
    ==========
    `bibliography` : list of Strings
        filenames with bibliography entries to be used
        in the further processing.
    `bib_style`: String
        name of biblatex style
    '''
    if build_dir is None:
        build_dir = '.'
    # create files for each different citation record
    for cmd, cite, key in cites:
        inname = '{}/{}.{}.source.md'.format(build_dir,cite,key)
        texname = '{}/{}.{}.tex'.format(build_dir,cite,key)
        result = '{}/{}.{}.md'.format(build_dir,cite,key)
        with open(inname,'w') as md_f:
            print(cmd,file=md_f)
        md2tex(inname,bibliography,
               out_file=texname,print_biblio=False)

def prepare_build_dir(build_dir, bibliography, cites,
                      bib_style='md',
                      template='bib2md.latex',
                      htlatex_cfg='./md.cfg'): ## TODO Update this to install location!
    '''Copies the necessary files into `build_dir`.'''
    for b in bibliography:
        shutil.copy(b, build_dir)
    if is_local(bib_style)[0]:
        shutil.copy(bib_style+'.bbx',build_dir)
        shutil.copy(bib_style+'.cbx',build_dir)
        if os.path.exists(bib_style+'.dbx'):
            shutil.copy(bib_style+'.dbx',build_dir)
    for f in [template, htlatex_cfg]:
        if is_local(f):
            shutil.copy(f, build_dir)

    ### TODO: Make a function
    pure_biblio = [is_local(b)[1] for b in bibliography]
    make_template = '''default: all

%.pdf : %.tex {biblio_str} {bib_style}.*bx
	xelatex $(patsubst %.pdf,%.tex,$@)
	biber $(patsubst %.pdf,%,$@)
	xelatex $(patsubst %.pdf,%.tex,$@)

%.html : %.pdf {htlatex_cfg}
	htxelatex $(patsubst %.html,%.tex,$@) {htlatex_cfg} " -cunihtf -utf8"

### Removes silly link anchor produced by tex4ht for the firs entry
%.md : %.html
	pandoc -f html+tex_math_dollars -t markdown $< | sed 's/\[\]{{#page.1}}\[\]{{#X0-}}//' > $@

clean_mess:
	latexmk -CA
	rm -f *.4* *.bbl *.css *.html *.idv *.lg *.run.xml *.tmp *.xref *.xdv

all: {md_files}
'''
    makefile = make_template.format(
        biblio_str=' '.join(pure_biblio),
        bib_style=is_local(bib_style)[1],
        htlatex_cfg=is_local(htlatex_cfg)[1],
        md_files=' '.join(['{}.{}.md'.format(cite,key) for _, cite, key in cites]))
    print(makefile, file=open('{}/Makefile'.format(build_dir),'w'))


def main():
    ## TODO: Update arguments (add build_dir, open file directly by argparse)
    ## TODO: Add htlatex_cfg arg
    ## TODO: Make some class (and clear funtion arguments after)
    parser = argparse.ArgumentParser(description='''
    Converts Markdown files to `.tex` file with the BIB file
    specified as a bibliography source. The result is intended
    to be used by the bib2md package.''')
    parser.add_argument('infile',
                        help='the Markdown file to be converted')
    parser.add_argument('-b', '--bib',
                        action='append', required=True,
                        help = '''add .bib file as a bibliography source
                               (required >= 1)''')
    parser.add_argument('-o', '--output-file',
                        dest='outfile', default='bib2md.tex',
                        help='''filename of the .tex output
                             (default: bib2md.tex)''')
    parser.add_argument('-p', '--print',
                        action='store_true',
                        help='''adds \\printbibliography
                             (disabled by default)''')
    parser.add_argument('-s', '--style', default='md',
                        help='biblatex style (default: md)')
    parser.add_argument('-t', '--template', default='bib2md',
                        help='pandoc template (default: bib2md)')
    parser.add_argument('-v','--verbose', action='store_true',
                        help='show the pandoc command')

    args = parser.parse_args()

    md_file = args.infile
    out_file = args.outfile
    bibliography = args.bib
    print_biblio = args.print
    bib_style = args.style
    template = args.template

    tf.tempdir = '.'
    build_dir_h = tf.TemporaryDirectory(prefix='b2md_')
    build_dir = build_dir_h.name
    tf.tempdir = build_dir

    infile = open(md_file,'r')
    cites = extract_cite_cmds(infile)
    ## Remove
    htlatex_cfg = './md.cfg'

    pure_biblio = [is_local(b)[1] for b in bibliography]
    generete_tex(cites, build_dir,
                 pure_biblio, bib_style=bib_style,
                 print_biblio = print_biblio,
                 template = template)
    prepare_build_dir(build_dir, bibliography, cites, bib_style,
                      template, htlatex_cfg)

    ## REMOVE, for testing purpsoses only
    subprocess.run(['make','-C{}'.format(build_dir)])
    for _, cite, key in cites:
        shutil.copy('{}/{}.{}.md'.format(build_dir,cite,key),'.')


if __name__ == "__main__":
    main()
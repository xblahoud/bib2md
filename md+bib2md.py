# coding: utf-8

import subprocess
import argparse

def md2tex(md_file, bibliography,
           out_file='bib2md.tex',
           print_biblio=True, bib_style='md',
           template='template.bib2md',
           verbose=False):
    pandoc_options = [
      '--to=latex',
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


def main():
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

    md2tex(md_file, bibliography, out_file,
           print_biblio, bib_style, template,
           args.verbose)


if __name__ == "__main__":
    main()
# coding: utf-8
# TODO: change local defaults to installed ones in tex2md.__init__

import subprocess
import argparse
import tempfile as tf
import re
import shutil
import os

class tex2md:

    '''Class that helps us convert TeX files into markdown
    files while resoving references by biber and biblatex.

    The conversion happens in a temporary directory that is destroyed
    after obtaining the resulting file. If you wish to keep the build
    directory, set conv_args.[build_dir] to some existing directory.

    The class uses the following pipeline:

    1. xelatex + biber (tex -> pdf)
    2. htxelatex from the ht4tex package (pdf -> html)
    3. pandoc (html -> md)

    Required parameters
    -------------------
    infile: String filename
        name of the `.tex` file to be converted
    bibliography: String or list of Strings
        files with bibliography entries to be used for the conversion

    Optional parameters
    -------------------
    outfile: String filename
        Name of desired output. If not specified change the extension
        of `infile` into `md`.
    bib_args: dict
        Various configuration filenames that allow to modify the
        conversion. If you use some non-preinstalled files (or styles),
        specify their path and prepend with './' if in the current
        directory. The understood keys and defaults are:
            * bib_style  : md     # biblatex style (without extensions)
            * htlatex_cfg : md.cfg # config file for htlatex
            * build_dir  : a random temporary directory
    '''

    def __init__(self, infile, bibliography, outfile=None, conv_args=None):

        if not os.path.exists(infile):
            raise FileNotFoundError('infile: `{}` cannot be found'.format(infile))
        self.infile = infile

        if isinstance(bibliography,str):
            bibliography = [bibliography]
        if not isinstance(bibliography, list):
            raise TypeError('Expected list of strings for bibliography')
        self.bibliography = bibliography

        if outfile is None:
            outfile = os.path.splitext(infile)[0] + '.md'
        self.outfile_p = outfile
        self.outfile_n = os.path.split(outfile)[1]

        if conv_args is None:
            conv_args = dict()
        for key, default in [
                ('bib_style', './md'),
                ('htlatex_cfg', './md.cfg')
                ]:
            if not key in conv_args:
                conv_args[key] = default
        if not 'build_dir' in conv_args:
            bd = make_tmp_dir()
            self.bd_h = bd[1]
            conv_args['build_dir'] = bd[0]
        self.build_dir = bd[0]
        self.conv_args = conv_args


    ## What about infile? I can copy it there but it clashes with the
    ## cites-approach
    def prepare_build_dir(self, copy_infile=True):
        '''Copies the necessary files into `build_dir`.

        copy_infile: boolean (default ``True``)
            also copy the input file into the build directory
        '''

        build_dir = self.conv_args['build_dir']
        bib_style = self.conv_args['bib_style']

        if copy_infile:
            shutil.copy(self.infile, '{}/{}.tex'.format(build_dir,
                        os.path.splitext(self.outfile_n)[0]))
        for b in self.bibliography:
            shutil.copy(b, build_dir)
        if is_local(bib_style)[0]:
            shutil.copy(bib_style+'.bbx',build_dir)
            shutil.copy(bib_style+'.cbx',build_dir)
            if os.path.exists(bib_style+'.dbx'):
                shutil.copy(bib_style+'.dbx',build_dir)
        for f in [self.conv_args['htlatex_cfg']]:
            if is_local(f):
                shutil.copy(f, build_dir)

    def convert(self):
        '''Prepare and execute the conversion.'''
        self.prepare_build_dir()
        self.prepare_make()
        subprocess.run(['make','-C',self.build_dir])
        shutil.copy('{}/{}'.format(self.build_dir,self.outfile_n),
                     self.outfile_p)

    def prepare_make(self, all_files=None):
        '''Prepare makefile for current job and store it in `build_dir`
        
        all_files: String or list of Strings
            files we want to generate
        
        '''
        build_dir = self.build_dir

        if all_files is None:
            all_files = [self.outfile_n]
        ### TODO: Make a function
        pure_biblio = [is_local(b)[1] for b in self.bibliography]
        args = self.conv_args
        make_template = '''default: all

%.pdf : %.tex {biblio_str} {bib_style}.*bx
\txelatex $(patsubst %.pdf,%.tex,$@)
\tbiber $(patsubst %.pdf,%,$@)
\txelatex $(patsubst %.pdf,%.tex,$@)

%.html : %.pdf {htlatex_cfg}
\thtxelatex $(patsubst %.html,%.tex,$@) {htlatex_cfg} " -cunihtf -utf8"

### Removes silly link anchor produced by tex4ht for the firs entry
%.md : %.html
\tpandoc -f html+tex_math_dollars -t markdown $< | sed 's/\[\]{{#page.1}}\[\]{{#X0-}}//' > $@

clean_mess:
\tlatexmk -CA
\trm -f *.4* *.bbl *.css *.html *.idv *.lg *.run.xml *.tmp *.xref *.xdv

all: {md_files}
'''
        makefile = make_template.format(
            biblio_str=' '.join(pure_biblio),
            bib_style=is_local(args['bib_style'])[1],
            htlatex_cfg=is_local(args['htlatex_cfg'])[1],
            md_files=' '.join(all_files))
        print(makefile, file=open('{}/Makefile'.format(build_dir),'w'))


def make_tmp_dir(prefix='b2m_'):
    tf.tempdir = '.'
    build_dir_h = tf.TemporaryDirectory(prefix='b2md_')
    build_dir = build_dir_h.name
    tf.tempdir = build_dir
    return build_dir, build_dir_h

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


def main():
    ## TODO: Update arguments (open file directly by argparse)
    ## TODO: Add htlatex_cfg arg
    ## TODO: Make some class (and clear funtion arguments after)
    ## TODO: Makefile can be general for all jobs
    parser = argparse.ArgumentParser(description='''
    Converts Markdown files to `.tex` file with the BIB file
    specified as a bibliography source. The result is intended
    to be used by the bib2md package.
    
    If using a local config files (e.g. for --style, --htlatex-cfg, -t),
    prefix them with `./`.''')
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
    parser.add_argument('-d', '--build-dir', default=None,
                        help='''A custom directory to be used for building.
                             Use the -o option to control the directory of
                             output.
                             (default: a random directory that will be
                             destroyed after building)''')
    parser.add_argument('-p', '--print',
                        action='store_true',
                        help='''adds \\printbibliography
                             (disabled by default)''')
    parser.add_argument('-s', '--style', default='md',
                        help='biblatex style (default: md)')
    parser.add_argument('--htlatex-cfg', default='md.cfg',
                        help='htlatex config file')
    parser.add_argument('-t', '--template', default='bib2md',
                        help='pandoc template (default: bib2md)')
    parser.add_argument('-v','--verbose', action='store_true',
                        help='show the pandoc command')

    args = parser.parse_args()

    conv_args = dict()
    conv_args['bib_style'] = args.style
    conv_args['build_dir'] = args.build_dir
    conv_args['htlatex_cfg'] = args.htlatex_cfg

    out_file = args.outfile
    bibliography = args.bib
    
    # Remove
    print_biblio = args.print
    template = args.template
    
    convertor = tex2md(args.infile, bibliography,out_file)
    convertor.convert()

    #build_dir, bd_h = make_tmp_dir()

    #infile = open(md_file,'r')
    #cites = extract_cite_cmds(infile)
    ## Remove
    #htlatex_cfg = './md.cfg'

    #pure_biblio = [is_local(b)[1] for b in bibliography]
    #generete_tex(cites, build_dir,
    #             pure_biblio, bib_style=bib_style,
    #             print_biblio = print_biblio,
    #             template = template)
    #prepare_build_dir(build_dir, bibliography, cites, bib_style,
    #                  template, htlatex_cfg)

    ## REMOVE, for testing purpsoses only
    #subprocess.run(['make','-C{}'.format(build_dir)])
    #for _, cite, key in cites:
    #    shutil.copy('{}/{}.{}.md'.format(build_dir,cite,key),'.')


if __name__ == "__main__":
    main()
#!/usr/bin/python3
import bib2md
import os

infile = 'test_subst.source.md'
outfile = 'test_subst.md'
if os.path.exists(outfile):
    os.remove(outfile)

c = bib2md.cite_replacer(infile, 'mypub.bib', outfile)
c.convert_cites()
c.replace_cite_cmds()

print('file {} should be created'.format(outfile))

if not os.path.exists(outfile):
    raise FileNotFoundError(outfile)

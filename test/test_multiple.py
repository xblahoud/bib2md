#!/usr/bin/python3
import bib2md
import os

outfiles = ['cite.md','cite2.md','out_cite.md','out_cite2.md']
for f in outfiles:
    if os.path.exists(f):
        os.remove(f)

c = bib2md.tex2md(['cite.tex','cite2.tex'],'mypub.bib')
c.prepare_conversion()
c.convert()

c = bib2md.tex2md(['cite.tex','cite2.tex'],'mypub.bib',
                  ['out_cite.md','out_cite2.md'])
c.prepare_conversion()
c.convert()

try:
    c = bib2md.tex2md(['cite.tex','cite2.tex'],'mypub.bib','cite3.md')
    raise Exception('different lengths given, should be detected')
except ValueError:
    pass

print('''4 files should be created:
    cite.md
    cite2.md
    out_cite.md
    out_cite2.md
''')

for f in outfiles:
    if not os.path.exists(f):
        raise FileNotFoundError(f)

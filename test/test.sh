rm *cite.*.*.*.md
python3 bib2md.py -b mypub.bib -s ./md -t ./bib2md.latex test_mdcite.md
echo
echo
echo 'should create i3 files:
cite.babiak.15.cav.md
mdcite.babiak.15.cav.md
mdcite.blahoudek.17.lpar.md'
echo 
echo
set -u
ls *.*.*.md

OUTF=test_res.md
INF=cite.tex
rm -f $OUTF
python3 bib2md.py -b mypub.bib -o $OUTF $INF
echo
echo should create $OUTF:
echo
set -u
ls *.md

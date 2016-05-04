# 2sm-ccdss-review-data

## Building

### Watch PDFs

    fswatch studies/*.pdf | xargs -I '{}' sh -c 'python extract2.py {} tmp/$(basename {} .pdf).yml'
    
### Build tables

    watch -n0 --beep --color 'fswatch --one-event tmp/* extract3.py | xargs -I{} -n1 ipython extract3.py tmp/*.yml'
    
### Build document

    fswatch --one-per-batch {,sections/}*.tex data/tmp | xargs -n1 pdflatex bachelor_thesis.tex

## Helpful during extraction

    watch --color --no-title -n0 'fswatch -1 tmp/* view.py | xargs -I{} -n1 python view.py tmp/Dexter2001.yml tmp/Murray2004.yml | tail -n+3 | awk \'/1/ {print "\033[32m" $0 "\033[39m"} /0/ {print "\033[0m" $0 "\033[39m"}\''

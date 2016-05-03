# 2sm-ccdss-review-data

## Building

### Watch PDFs

    fswatch studies/*.pdf | xargs -I '{}' sh -c 'python extract2.py {} tmp/$(basename {} .pdf).yml'
    
### Build tables

    watch -n0 --beep --color 'fswatch --one-event tmp/* extract3.py | xargs -I{} -n1 ipython extract3.py tmp/*.yml'
    
### Build document

    fswatch --one-per-batch {,sections/}*.tex data/tmp | xargs -n1 pdflatex bachelor_thesis.tex

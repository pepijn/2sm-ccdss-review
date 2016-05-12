# 2sm-ccdss-review-data

## Building

### Watch PDFs

    fswatch studies/*.pdf | xargs -I '{}' sh -c 'python extract_annotations.py {} tmp/$(basename {} .pdf).yml'
    
### Build tables

    watch -n0 --beep --color 'fswatch --one-event tmp/* create_tables.py | xargs -I{} -n1 ipython create_tables.py tmp/*.yml'
    
### Build document

    fswatch --one-per-batch {,sections/}*.tex tmp | xargs -n1 pdflatex bachelor_thesis.tex

## Helpful during extraction

    fswatch -o tmp/* view.py | xargs -I'{}' -n1 sh -c 'clear && python view.py tmp/Dexter2001.yml tmp/Murray2004.yml | awk \'/ 1 \w{3} / {print "\033[32m\033[1m" $0 "\033[39m"} / 0 \w{3} / {print "\033[0m\033[0m" $0 "\033[39m"}\''

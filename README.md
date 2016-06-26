# Annotation Attribute Extractor [![DOI](https://zenodo.org/badge/22943/pepijn/annotation-attribute-extractor.svg)](https://zenodo.org/badge/latestdoi/22943/pepijn/annotation-attribute-extractor)


Helpful for reproducible qualitative systematic reviews.

## Example usage

    fswatch studies/*.pdf | xargs -I '{}' sh -c 'python extract_annotations.py {} tmp/$(basename {} .pdf).yml'

## Requirements

### python-poppler-qt4

    pip install -e git+https://github.com/wbsoft/python-poppler-qt4@576edd3438b760ddb113044b6602e91abd914b38#egg=python-poppler-qt4

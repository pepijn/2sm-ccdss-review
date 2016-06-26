# Annotation attribute extractor

Helpful for qualitative systematic reviews.

## Example usage

    fswatch studies/*.pdf | xargs -I '{}' sh -c 'python extract_annotations.py {} tmp/$(basename {} .pdf).yml'

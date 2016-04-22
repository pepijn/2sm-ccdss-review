set -euxo pipefail

touch "$2"
python2 extract2.py "$1" < "$2" | python2 summarize2.py

set -euxo pipefail

touch "$2"
TMP=$(gmktemp --suffix .org)
python2 extract2.py "$1" < "$2" > $TMP
$EDITOR $TMP
python2 save.py < $TMP > "$2"

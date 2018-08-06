#!/bin/bash
# vim: set expandtab tabstop=4 shiftwidth=4:

./bpd_dot.py $1 $2 | unflatten -l 10 -c 99 -f > $3.dot && dot -Tpng $3.dot -o $3.png
#./bpd_dot.py $1 $2 > $3.dot && dot -Tpng $3.dot -o $3.png

echo
ls -l $3.png
echo "If everything went well, see $3.png"

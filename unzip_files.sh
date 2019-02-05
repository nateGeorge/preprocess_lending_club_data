# create directories if don't exist
if [ ! -d "accept" ]; then
  mkdir accept
fi

if [ ! -d "reject" ]; then
  mkdir reject
fi

# move zip files if present
# tricky to do:
# http://www.ducea.com/2009/03/05/bash-tips-if-e-wildcard-file-check-too-many-arguments/
files=$(ls Loan* 2> /dev/null | wc -l)
if [ "$files" != "0" ]; then
    for f in Loan*; do mv $f accept/; done
    cd accept
    for f in *.zip; do unzip $f; rm $f; done
else
    echo "No accept files present"
fi

files=$(ls Reject* 2> /dev/null | wc -l)
if [ "$files" != "0" ]; then
    for f in Reject*; do mv $f reject/; done
    cd ../reject
    for f in *.zip; do unzip $f; rm $f; done
else
    echo "No reject files present"
fi

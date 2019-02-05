# create directories if don't exist
if [ ! -d "accept" ]; then
  mkdir accept
fi

if [ ! -d "reject" ]; then
  mkdir reject
fi

# move zip files if present
if [ -e "Loan*" ]; then
    for f in Loan*; do mv $f accept/; done
    cd accept
    for f in *.zip; do unzip $f; rm $f; done
else
    echo "No accept files present"
fi

if [ -e "Reject*" ]; then
    for f in Reject*; do mv $f reject/; done
    cd ../reject
    for f in *.zip; do unzip $f; rm $f; done
else
    echo "No reject files present"
fi

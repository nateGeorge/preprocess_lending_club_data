mkdir accept
mkdir reject
for f in Reject*; do mv $f reject/; done
for f in Loan*; do mv $f accept/; done
cd accept
for f in *.zip; do unzip $f; rm $f; done
cd ../reject
for f in *.zip; do unzip $f; rm $f; done

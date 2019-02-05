# preprocess_lending_club_data
Pre-processes lending club loan data and concatenates into one large file.
This was made for publishing the dataset on [Kaggle](http://www.kaggle.com).  The Kaggle dataset/kernels are [here](https://www.kaggle.com/wordsforthewise/lending-club).

# Instructions for use
This was all done on Ubuntu 16.0.2.  Other operating systems may or may not work.


1. First, download all data from [here](https://www.lendingclub.com/info/download-data.action) then move it to the main directory of the cloned repo.  In the bash shell, run `unzip_files.sh`.  You may need to do
`sudo chmod a+x unzip_files.sh`
first to make the file executable.

2. Next, make sure the last few commented lines have the right end date (update it to 2018, etc if necessary), and run the `concat_data.py` file:
`python3 concat_data.py`
This will take quite a long time to write the file.  Reading it isn't too bad though.

This was made for python3, although I think it should work in python2 (untested).

## Notes
The linebreaks are LF (unix/linux) and there is a line with a link at the top (thus the `skiprows=True` and header=1 in pd.read_csv())

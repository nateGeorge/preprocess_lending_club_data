# preprocess_lending_club_data
Currently, lendingclub has changed their downloads and policy.  They now only have the accepted loans -- rejected loans were removed sometime in 2019.  They also have a scary copyright notice when you go to download the data.

Pre-processes lending club loan data and concatenates into one large file.
This was made for publishing the dataset on [Kaggle](http://www.kaggle.com).  The Kaggle dataset/kernels are [here](https://www.kaggle.com/wordsforthewise/lending-club).

## Quickstart
`python scrape_data.py`

# Instructions for use
This was all done on Ubuntu 16.0.2.  Other operating systems may or may not work.

# Download data
There is now a `scrape_data.py` file which can be used to scrape all the data from LendingClub's site.  You will need to update the `FILEPATH`, add a few environment variables (`lendingclub_uname` and `lendingclub_pass`), as well as create a Firefox profile so that the data is downloaded in to the repo directory.  Then you should be able to run the `scrape_data.py` file, and it will download data as well as create the fully merged csv.gz files in the full_data folder.

## Old way to download

1. First, download all data from [here](https://www.lendingclub.com/info/download-data.action) then move it to the main directory of the cloned repo.  In the bash shell, run `unzip_files.sh`.  You may need to do
`sudo chmod a+x unzip_files.sh`
first to make the file executable.

2. Next, make sure the last few commented lines have the right end date (update it to 2018, etc if necessary), and run the `concat_data.py` file:
`python3 concat_data.py`
This will take quite a long time to write the file.  Reading it isn't too bad though.

## Notes
This was made for Python3, although I think it may work in Python2 (untested).

The linebreaks are LF (unix/linux) and there is a line with a link at the top (thus the `skiprows=True` and header=1 in pd.read_csv())

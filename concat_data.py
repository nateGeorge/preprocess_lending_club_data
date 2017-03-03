'''
To get/unzip all the data:
first I downloaded from
https://www.lendingclub.com/info/download-data.action
then, in the bash shell:
mkdir accept
mkdir reject
for f in Reject*; do mv $f reject/; done
for f in Loan*; do mv $f accept/; done
cd accept
for f in *.zip; do unzip $f; rm $f; done
cd reject
for f in *.zip; do unzip $f; rm $f; done

The linebreaks are LF (unix/linux)
and there is a line with a link at the top (thus the skiprows and header=1
in pd.read_csv())
'''

import pandas as pd
import numpy as np
from glob import iglob
import feather as ft
import re

def make_large_df(path='accept/', years=None):
    """
    Reads .csvs and concatenates into one large dataframe, then writes back to
    csv.

    Parameters:
    -----------
    path: string
        path to csv files
    years: list of ints


    Returns:
    -----------
    full_df: pandas dataframe
        full dataframe of all data from csvs
    """
    if years is not None:
        years = [str(y) for y in years]

    dfs = []
    files = []
    for f in iglob(path + '*.csv'):
        # only use files with specified years if present
        skip = True
        if years is not None:
            if not any([y in f for y in years]):
                print 'file', f, 'doesn\'t have any relevant years in it'
                continue

        print 'reading file:', f
        temp_df = pd.read_csv(f, skiprows=0, header=1)
        if 'accept' in path:
            print 'dropping'
            temp_df.dropna(thresh=30, inplace=True)
            # conversion necessary to save memory and write to feather/hdf5 format
            temp_df['id'] = temp_df['id'].astype('int64')

        dfs.append(temp_df)
        files.append(f)

    # check to make sure all columns are consistent
    cols = None
    for f, df in zip(files, dfs):
        if cols is None:
            cols = df.columns
        else:
            if set(cols) != set(df.columns):
                print f

    full_df = None
    for df in dfs:
        if full_df is None:
            full_df = df
        else:
            full_df = full_df.append(df)

    return full_df


def convert_pct(x):
    """
    Converts string with % to a float, handles 'None's.
    """
    if x is None or pd.isnull(x):
        return None

    return float(re.sub('%', '', x))


if __name__ == "__main__":
    # this makes a dataframe with all csvs
    accept_df = make_large_df(path='accept/')
    reject_df = make_large_df(path='reject/')
    # I really don't think anyone's going to use the url...
    accept_df.drop('url', axis=1, inplace=True)
    # remove % and convert to float (numeric)
    accept_df['int_rate'] = accept_df['int_rate'].apply(lambda x: float(re.sub('%', '', x)))
    accept_df['revol_util'] = accept_df['revol_util'].apply(lambda x: convert_pct(x))
    accept_df.reset_index(inplace=True, drop=True)
    reject_df.reset_index(inplace=True, drop=True)

    # to check out info do this:
    # accept_df.info(verbose=True, null_counts=True)
    # reject_df.info(verbose=True, null_counts=True)

    # doesn't save any memory so abandoned this
    # ft.write_dataframe(accept_df, 'accepted_loans_2007-2016.ft')
    # ft.write_dataframe(reject_df, 'rejected_loans_2007-2016.ft')

    # files are too big to upload to kaggle
    # accept_df.to_csv('accepted_2007_to_2016.csv', index=False)
    # reject_df.to_csv('rejected_2007_to_2016.csv', index=False)

    # doesn't save any memory
    # reject_df.to_hdf('rejected_loans_2007-2016.h5', 'rejected_loans_2007-2016', complevel=9, mode='w')
    # also doesn't save any memory
    # reject_df.to_pickle('rejected_loans_2007-2016.pk')
    # reject_df.to_msgpack('test.msg')

    # takes a LOOOONG time.  many minutes
    accept_df.to_csv('full_data/accepted_2007_to_2016.csv.gz', index=False, compression='gzip')
    reject_df.to_csv('full_data/rejected_2007_to_2016.csv.gz', index=False, compression='gzip')

    # makes a 2012-2016 dataframe for accepted, 2013-2016 for rejected
    # accept_df = make_large_df(path='accept/', years=[2016])
    # reject_df = make_large_df(path='reject/', years=[2016])
    # print 'writing csvs...'
    # accept_df.to_csv('2016_data/LoanStats_2016.csv', index=False)
    # reject_df.to_csv('2016_data/RejectStats_2016.csv', index=False)

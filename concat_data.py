from __future__ import print_function
import pandas as pd
import numpy as np
from glob import iglob, glob
import feather as ft
import re
import os

def make_large_df(path='accept/', years=None):
    """
    Reads .csvs and concatenates into one large dataframe, then writes back to
    csv.

    Parameters:
    -----------
    path: string; path to csv files
    years: list of ints


    Returns:
    -----------
    full_df: pandas dataframe; full dataframe of all data from csvs
    """
    if years is not None:
        years = [str(y) for y in years]

    dfs = []
    files = []
    for f in iglob(path + '*.csv'):
        # only use files with specified years if present
        if years is not None:
            if not any([y in f for y in years]):
                print('file', f, 'doesn\'t have any relevant years in it')
                continue

        print('reading file:', f)
        temp_df = pd.read_csv(f, skiprows=0, header=1, low_memory=False)

        dfs.append(temp_df)
        files.append(f)

    # check to make sure all columns are consistent
    cols = None
    for f, df in zip(files, dfs):
        if cols is None:
            cols = df.columns
        else:
            if set(cols) != set(df.columns):
                print('columns in file', f, 'do not match other files!')
                print('mismatched columns:', set(cols).difference(set(df.columns)))

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


def create_full_csv_files():
    """
    creates full csv files from individual files
    """
    print('even on a fast computer, this takes 10+ minutes...')
    # this makes a dataframe with all csvs
    accept_df = make_large_df(path='accept/')
    reject_df = make_large_df(path='reject/')
    # I really don't think anyone's going to use the url...
    # but will leave it in for completeness
    # accept_df.drop('url', axis=1, inplace=True)
    # remove % and convert to float (numeric)
    accept_df['int_rate'] = accept_df['int_rate'].apply(lambda x: convert_pct(x))
    accept_df['revol_util'] = accept_df['revol_util'].apply(lambda x: convert_pct(x))
    accept_df.reset_index(inplace=True, drop=True)
    reject_df.reset_index(inplace=True, drop=True)

    # to check out info do this:
    # accept_df.info(verbose=True, null_counts=True)
    # reject_df.info(verbose=True, null_counts=True)

    # takes a LOOOONG time.  many minutes
    if not os.path.exists('full_data'):
        os.mkdir('full_data')

    latest_yr_qtr = get_latest_year_qtr()
    print('writing accepted file...')
    accept_df.to_csv('full_data/accepted_2007_to_{}.csv.gz'.format(latest_yr_qtr), index=False, compression='gzip')
    print('writing rejected file...')
    reject_df.to_csv('full_data/rejected_2007_to_{}.csv.gz'.format(latest_yr_qtr), index=False, compression='gzip')

    # makes a 2012-2016 dataframe for accepted, 2013-2016 for rejected
    # accept_df = make_large_df(path='accept/', years=[2016])
    # reject_df = make_large_df(path='reject/', years=[2016])
    # print 'writing csvs...'
    # accept_df.to_csv('2016_data/LoanStats_2016.csv', index=False)
    # reject_df.to_csv('2016_data/RejectStats_2016.csv', index=False)


def get_latest_year_qtr():
    """
    Gets latest year and quarter from files for naming combined csv.
    Should be latest via OS timestamp, but this is more robust
    just in case something is weird.
    """
    files = glob('accept/' + '*.csv')
    yr_qtr = [fn.split('_')[-1].split('.')[0] for fn in files]
    # add year to qtr and take largest
    sums = []
    for y in yr_qtr:
        # skip early years
        if y == 'securev1':
            sums.append(0)
            continue

        sums.append(int(y[:4]) + int(y[-1]))

    latest_idx = np.argmax(sums)
    return yr_qtr[latest_idx]


if __name__ == "__main__":
    create_full_csv_files()

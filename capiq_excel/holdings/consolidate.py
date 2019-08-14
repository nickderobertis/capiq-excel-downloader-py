
def sum_by_id_date(df, id_var, date_var, keep_cols='all'):

    if keep_cols == 'all':
        keep_cols = df.columns

    return df[keep_cols].groupby([id_var, date_var]).sum()

if __name__ == '__main__':
    import pandas as pd
    import argparse

    from dataconfig.paths import capiq_path
    from dataconfig.variables import variable_display_names as vd
    from capiq.holdings.config import insider_keep_cols, institutional_keep_cols

    parser = argparse.ArgumentParser(description='Consolidate individual holdings into a number of shares per id per time period')
    parser.add_argument('-i', '--insider', default=False, action='store_true')

    args = parser.parse_args()

    if args.insider:
        print('Consolodating insider holdings')
        keep_cols = insider_keep_cols
        file = capiq_path(r'capiq insider holdings data.csv')
        outfile = capiq_path(r'capiq insider shares consolidated.csv')
    else:  # institutional holdings
        print('Consolodating institutional holdings')
        keep_cols = institutional_keep_cols
        file = capiq_path(r'capiq institutional holdings data.csv')
        outfile = capiq_path(r'capiq institutional shares consolidated.csv')

    df = pd.read_csv(file, encoding='utf8')

    print(f'Got {len(df)} rows to work with.')

    consol_df = sum_by_id_date(df, vd.cqid, vd.date, keep_cols=keep_cols)
    consol_df.to_csv(outfile)
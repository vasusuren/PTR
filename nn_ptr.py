import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
import json

def gen_data():
    inx = pd.date_range('01/01/2015',end='31/12/2015')
    col = range(48)
    df_temp = pd.DataFrame(np.random.rand(365,48), index=inx, columns=col)
    return df_temp


def extract_weekdays(df):
    inx = df.index
    wd = [i.weekday() for i in inx]
    df['WD'] = wd
    df = df.loc[df['WD']<5,:]
    del df['WD']
    return df

def dist_calc(df, per):
    df_dist = (df_temp.diff(per) ** 2).sum(axis=1)
    return df_dist

def nn_dates(df_temp_wd):
    df1 = pd.DataFrame(cdist(df_temp_wd, df_temp_wd), index=df_temp_wd.index, columns=df_temp_wd.index)
    dct = {}
    for row in range(df1.shape[0]):
        df2 = df1.iloc[row - last_n_days:row + 1, row]
        ls = np.argsort(df2).values
        try:
            ls = df2.iloc[ls].index[1:nn + 1]
            dct[str(df1.index[row])] = [str(i) for i in ls]
        except IndexError:
            pass
    return dct

def write_json(dct,filename):
    with open(filename, 'w') as fw:
        ab = json.dumps(dct)
        json.dump(ab,fw)

if __name__ == '__main__':
    df_temp = gen_data()
    df_cons = gen_data()
    last_n_days=10
    nn = 3
    df_temp_wd = extract_weekdays(df_temp)
    df_cons_wd = extract_weekdays(df_cons)
    # df_dist = pd.DataFrame(None, index=df_temp_wd.index, columns = range(periods))
    # for period in range(periods):
    #     df_dist[period] = dist_calc(df_temp_wd, period)
    # df_nn = df_dist.apply(np.argsort, 1).iloc[:,1:nn+1]
    dct = nn_dates(df_temp_wd)
    write_json(dct,r'./similar_dates.json')
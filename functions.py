import pandas as pd


def nans(df):
    nans = pd.DataFrame(df.isnull().sum(), columns=['num_nans'])
    nans.reset_index(inplace=True)
    nans['%_nans'] = nans['num_nans'] / len(df)
    return nans[nans['num_nans'] != 0]


def drop_nans(df, val):
    resume = nans(df)
    var_to_drop = list(resume['index'][resume['%_nans'] >= val])
    df = df.drop(var_to_drop, axis=1)
    return df


def nans_row_index(df):
    out_index = []
    for i in df.columns:
        mec = list(df[i][df[i].isnull()==True].index)
        for ii in mec:
            out_index.append(ii)

    out_index = list(dict.fromkeys(out_index))
    return out_index


def nans_per_row(df):
    out_index = []
    for i in df.columns:
        mec = list(df[i][df[i].isnull()==True].index)
        for ii in mec:
            out_index.append(ii)

    nans_p_row = {}
    for r in out_index:
        nans_p_row.update({r: out_index.count(r)})
    nans_p_row = pd.DataFrame(nans_p_row, index=['NaNs_Ammount']).T
    return nans_p_row.sort_values(by=['NaNs_Ammount'], ascending=False)


def representative(df, val):
    result = {}
    rep = []
    for i in df:
        result.update({i: df[i].value_counts()/len(df)})

    for key in result:
        for cc, i in enumerate(result[key]):
            if i<=val:
                rep.append([key, result[key].keys()[cc], result[key][cc]])
                
    rep = pd.DataFrame(rep)
    rep.columns = ['var', 'value', '%']
    return rep
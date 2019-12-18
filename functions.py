import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
    features = ['var', 'value', '%']
    rep.columns = features
    resumen = rep[['var', '%']].groupby('var').count()
    rep['count'] = rep['var'].apply(lambda x: resumen.loc[x, '%'])
    return rep[features][rep['count'] != 1], rep[features][rep['count'] == 1]


def m_histograma(df, col, sz=(30,10), clr='teal'):
    features = list(df.columns)
    rows = len(features) // col
    residuo = len(features) % col

    fig, ax = plt.subplots(rows, col, figsize=sz)
    i=0
    for r in range(rows):
        for c in range(col):
            sns.distplot(df[features[i]], color=clr, ax=ax[r, c])
            i+=1
    
    if residuo != 0:
        if residuo == 1:
            return sns.distplot(df[features[-1]], color=clr)
        if residuo > 1:
            fig, ax = plt.subplots(nrows=1, ncols=residuo, figsize=(sz[0], sz[1]//residuo))
            i = -1
            for c in range(residuo):
                sns.distplot(df[features[i]] , color=clr, ax=ax[c])
                i -= 1

                
def m_countplot(df, col, sz=(30,10), clr='Paired'):
    features = list(df.columns)
    rows = len(features) // col
    residuo = len(features) % col

    fig, ax = plt.subplots(rows, col, figsize=sz)
    i=0
    for r in range(rows):
        for c in range(col):
            sns.countplot(df[features[i]], palette=clr, ax=ax[r, c])
            i+=1
    
    if residuo != 0:
        if residuo == 1:
            return sns.countplot(df[features[-1]], palette=clr)
        if residuo > 1:
            fig, ax = plt.subplots(nrows=1, ncols=residuo, figsize=(sz[0], sz[1]//residuo))
            i = -1
            for c in range(residuo):
                sns.countplot(df[features[i]] , palette=clr, ax=ax[c])
                i -= 1

    
def m_scatterplot(df, col, var, sz=(30,10), clr='teal'):
    features = list(df.columns)
    features.remove(var)
    rows = len(features) // col
    residuo = len(features) % col

    fig, ax = plt.subplots(rows, col, figsize=sz)
    i=0
    for r in range(rows):
        for c in range(col):
            sns.scatterplot(x=df[features[i]], y=df[var], color=clr, ax=ax[r, c])
            i+=1
    
    if residuo != 0:
        if residuo == 1:
            return sns.scatterplot(x=df[features[-1]], y=df[var], color=clr)
        if residuo > 1:
            fig, ax = plt.subplots(nrows=1, ncols=residuo, figsize=(sz[0], sz[1]//residuo))
            i = -1
            for c in range(residuo):
                sns.scatterplot(x=df[features[i]], y=df[var], color=clr, ax=ax[c])
                i -= 1
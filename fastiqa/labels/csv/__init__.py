from .. import *
from .vis import *
# from .distplot import *
"""
# %%
from fastiqa.labels.csv import *; IqaDataFrame(CLIVE).split().save()
from fastiqa.labels.csv import *; IqaDataFrame(KonIQ).split().save()

# %%
from fastiqa.labels.csv import *;
IqaDataFrame(FLIVE).clean_tags().save()
IqaDataFrame(FLIVE).df['tags'].unique()
# tags problem, combination
# %%
# %%
from fastiqa.labels.csv import *; IqaDataFrame(FLIVE640).clean_tags().save()
# %%
df.index
df.sort_values(by=['SROCC'])
np.intersect1d(df.index, ['resnet101', 'resnet34', 'resnet50'])


import plotly.offline as py
py.init_notebook_mode(connected=False)


each file independent is better
"""

import numpy as np

def keep_tags(ds, tags):
    s = set(map(str, tags))

    def filter_tags(x):
        if isinstance(x, list):
            res = set(x).intersection(s)
            return ' '.join(res) if res is not '' else np.nan
        else:
            return x

    return ds.str.strip().str.split(' ').apply(filter_tags)


class IqaDataFrame(IqaData):
    def clean_tags(self):
        df = self.df

        if 'tags' in df.columns:
            df = df.drop(columns=['tags'])

        # add tags
        df_tags = pd.read_csv(self.path/'labels_image_attri.csv')
        df = df.merge(df_tags, how = 'left', left_on=self.fn_col, right_on='name')

        # clean tags
        df['tags'] = keep_tags(df['tags'], ['blurry', 'ue', 'oe', 'grainy'])
        df['tags'] = df['tags'].str.strip().replace('', np.nan)
        df['tags'] = df['tags'].fillna('good')
        # df['tags'].unique()
        self.df = df
        return self

    def sort(self, decimals=0):
        if self.img_raw_size is None: # no fixed sized
            self.df['num_pix'] = self.df[self.size_cols[0]] * self.df[self.size_cols[1]]
            self.df['size'] = self.df[self.size_col[0]].astype(int).round(decimals).astype(str) + 'x' + \
                              self.df[self.size_col[1]].astype(int).round(decimals).astype(str)
            self.df = self.df.sort_values(by=['num_pix'], ascending=False)

    def split(self, valid_pct=0.2, seed=0):
        np.random.seed(seed)
        self.df['is_valid'] = np.random.rand(len(self.df)) < valid_pct
        return self

    def save(self):
        self.df.to_csv(self.path/self.csv_labels, index=False)

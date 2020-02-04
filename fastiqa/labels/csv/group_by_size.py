# size.py is too confusing, rename the file to group_by_size.py
# class name Counter renamed to GroupBySize
# size_cnt renamed to size_counts num_images_in_same_size sz_cnt

"""
# %%
# GroupBySize(CLIVE)
%matplotlib inline
from fastiqa.csv.group_by_size import *
from fastiqa.labels import *
GroupBySize(FLIVE).summary()
# - 2952 sizes have less than 10 images (6350 images in total) (16.72%)
# 10 images (6908 images in total) (18.19%)
# size_cnt and then get tail 6896
# %%
"""

from . import IqaData, cached_property
import pandas as pd


def split_2k(self):
    df = pd.read_csv(self.path / super().csv_labels)
    valid = (df.width_image <= 640) & (df.height_image <= 640)
    df[valid].to_csv(self.path / self.csv_labels, index=False)

def create_csv_labels(label):
    df100 = []
    # 8k is sampled from validation set
    first_group = label(img_size=(375,500))
    df = IqaData(first_group, filter=lambda x: x.is_valid).df.sample(n=100, random_state=0)
    df100.append(df)

    size_counts = GroupBySize(label).size_counts
    df_size_gt_100 = size_counts[size_counts >= 100]

    # The first group is 8k
    for idx in df_size_gt_100.index.tolist()[1:]:
        h, w = idx.split('x')
        h, w = int(h), int(w)
        df = label(img_size=(h,w)).df.sample(n=100, random_state=0)
        df100.append(df)

    return pd.concat(df100, ignore_index=True, sort=False)


class GroupBySize(IqaData):
    decimals = 0
    suffix='_image'

    @cached_property
    def size_counts(self):
        return self.df['size' + self.suffix].value_counts()


    def summary(self, decimals=0):
        if decimals != self.decimals:
            del self.__dict__['size_counts']
        print(f'{len(self.size_counts)} groups, {len(self.df)} images in total')
        print(f'- {self.size_counts[self.size_counts == 1].sum()} sizes only have 1 image')

        df_size_geq_10 = self.size_counts[self.size_counts >= 10]
        df_size_leq_10 = self.size_counts[self.size_counts <= 11]
        df_size_geq_100 = self.size_counts[self.size_counts >= 100]

        n = df_size_geq_10.sum()
        N = len(self.df)
        print(f'- {len(df_size_geq_10)} sizes have more than 10 images ({n} images in total) ({n * 100 / N:.2f}%)')
        n = df_size_geq_100.sum()
        print(f'- {len(df_size_geq_100)} sizes have more than 100 images ({n} images in total) ({n * 100 / N:.2f}%)')

        n = df_size_leq_10.sum()
        print(f'- {len(df_size_leq_10)} sizes have less than 10 images ({n} images in total) ({n * 100 / N:.2f}%)')

        print('Top 30 sets:')

        return self.size_counts.head(n=30)

    # add a column about size cnt: size_image_cnt
    def add_size_counts(self):
        if 'size' + self.suffix + '_cnt' not in self.df.columns:
            self.df = pd.merge(df, self.size_counts.to_frame(), how='left',
                      left_on='size' + suffix,
                      right_index=True, suffixes=('', '_cnt'))

from . import IqaDataBunch
from fastai.vision import MSELossFlat

"""
IM2MOS
Input:  data_cls = ImageList
Output: label_cls = FloatList


# %%
%matplotlib inline
from fastiqa.bunches import *
# %%
Im2MOS(CLIVE)
Im2MOS(FLIVE640)
Patch1toMOS(FLIVE_2k, batch_size=1)

# %% for debugging
from fastiqa.bunches import *; Im2MOS(CLIVE).get_data()
"""

class Im2MOS(IqaDataBunch):
    _data = None
    label_col_idx = 0  # only one output
    loss_func = MSELossFlat()

    def get_data(self):
        data = self.get_list()
        data = self.get_split(data)
        data = self.get_label(data)
        data = self.get_augment(data)
        data = self.get_bunch(data)
        return data

    def get_list(self):
        return self.data_cls.from_df(self.df, self.path, suffix=self.fn_suffix, cols=self.fn_col,
                                     folder=self.folder)

    def get_split(self, data):
        if self.valid_pct is None:
            data = data.split_from_df(col='is_valid')
        else:
            if self.valid_pct == 1:  # TODO ignore_empty=True
                print('all samples are in the validation set!')
                data = data.split_by_valid_func(lambda x: True)  # All valid
                data.train = data.valid # train set cannot be empty
            elif self.valid_pct == 0:
                print('all samples are in the training set!')
                data = data.split_none()
            else: # 0 < self.valid_pct < 1
                print('We suggest using a fixed split with a fixed random seed')
                data = data.split_by_rand_pct(valid_pct=self.valid_pct, seed=2019)
        return data

    def get_label(self, data):
        return data.label_from_df(cols=self.label_cols[self.label_col_idx], label_cls=self.label_cls)

    def get_augment(self, data):
        return data if self.img_tfm_size is None else data.transform(size=self.img_tfm_size)

    def get_bunch(self, data, **kwargs):
        return data.databunch(bs=self.batch_size, val_bs=self.val_bs, **kwargs)


# These properties will overwrite label properties
class Patch1toMOS(Im2MOS):
    size_col = ['height_patch_1', 'width_patch_1']
    label_cols = 'mos_patch_1',
    fn_col = 'name_patch'
    fn_suffix = '_patch_1.jpg'
    csv_labels = 'labels_image_3patch.csv'
    # batch_size = 1
    abbr = 'Patch 1'


class Patch2toMOS(Im2MOS):
    size_col = ['height_patch_2', 'width_patch_2']
    label_cols = 'mos_patch_2',
    fn_col = 'name_patch'
    fn_suffix = '_patch_2.jpg'
    csv_labels = 'labels_image_3patch.csv'
    # batch_size = 1
    abbr = 'Patch 2'


class Patch3toMOS(Im2MOS):
    size_col = ['height_patch_3', 'width_patch_3']
    label_cols = 'mos_patch_3',
    fn_col = 'name_patch'
    fn_suffix = '_patch_3.jpg'
    csv_labels = 'labels_image_3patch.csv'
    # batch_size = 1
    abbr = 'Patch 3'

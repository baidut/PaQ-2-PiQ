
from fastai.vision import *
from ...label import IqaData, cached_property

# from fastai.vision.data import *
# from fastai.datasets import * # URLs
# from fastai.core import * # URLs

# TODO

'''
remove unnecessary properties: no_tfms = True
remove get_data(self, size) size
instead, use
data.df = data.df[]

databunch_type update the df after loading

Im2MOS(CLIVE, batch.....
'''


class IqaDataBunch(IqaData):
    batch_size = 64 # 16
    # num_workers = 16
    label_cls = FloatList
    data_cls = ImageList
    device = torch.device('cuda')

    name = None

    def __getattr__(self, k: str):
        # print(f'__getattr__: {k}')
        try:
            return getattr(self.label, k)
        except AttributeError:
            return getattr(self.data, k)

    @cached_property
    def data(self):
        print(f'loading data...{self.name}')
        data = self.get_data()
        print(f'DONE loading data {self.name}')
        return data

    def get_data(self):
        return NotImplementedError

    def reset(self, **kwargs):
        self.label._df = None
        self._data = None
        self.__dict__.update(kwargs)
        return self

    def _repr_html_(self):
        self.data.show_batch(rows=2, ds_type=DatasetType.Valid)
        print(self.data.__str__())
        return

    def show(self, fn):
        # TODO not found?
        # locate the image
        ds = self.df[self.df[self.fn_col] == fn]
        try: idx = int(ds.index[0])
        except IndexError: print('Not found!'); return

        # put selected sample on the top of the dataframe
        self.df.loc[0, :] = self.df.iloc[idx]
        self.df.loc[0, 'is_valid'] = True

        # avoid loading the whole database
        self.df = self.df.iloc[:self.batch_size]

        # backup the data
        data = self._data

        # reload the database
        self._data = None
        self.show_batch(ds_type=DatasetType.Single)
        self.reset(_data = data)
        return ds.T # otherwise won't show all columns

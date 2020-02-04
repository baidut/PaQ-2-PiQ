from fastai.vision import *
from fastai.data_block import _maybe_squeeze
from . import Im2MOS

"""
# %%
from fastiqa.all import *; Im2Tags(FLIVE640).data
# %%
"""

class NanLabelImageList(ImageList):
    def label_from_df(self, cols:IntsOrStrs=1, label_cls:Callable=None, **kwargs):
        "Label `self.items` from the values in `cols` in `self.inner_df`."
        labels = self.inner_df.iloc[:,df_names_to_idx(cols, self.inner_df)]
        # Commented line:##
        #assert labels.isna().sum().sum() == 0, f"You have NaN values in column(s) {cols} of your dataframe, please fix it."
        ####################
        if is_listy(cols) and len(cols) > 1 and (label_cls is None or label_cls == MultiCategoryList):
            new_kwargs,label_cls = dict(one_hot=True, classes= cols),MultiCategoryList
            kwargs = {**new_kwargs, **kwargs}
        return self._label_from_list(_maybe_squeeze(labels), label_cls=label_cls, **kwargs)


class Im2Tags(Im2MOS):
    data_cls = NanLabelImageList
    label_cols = 'tags',
    label_cls = MultiCategoryList
    label_delim = ' '

    def get_label(self, data):
        return data.label_from_df(cols=self.label_cols[self.label_col_idx],
        label_cls=self.label_cls,
        label_delim=self.label_delim)
